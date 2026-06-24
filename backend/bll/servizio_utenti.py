from uuid import UUID
from datetime import datetime, timezone
import httpx
from supabase import create_client
from supabase.lib.client_options import SyncClientOptions
from supabase_auth.errors import AuthApiError
from config import supabase, SUPABASE_URL, SUPABASE_KEY, _verify
from dal.attore_repository import AttoreRepository, AttoreNonTrovatoException
from bll.notifica_service import NotificaService


def _client_per_richiesta():
    """Client Supabase fresco per sign_in — isola la sessione utente dal singleton admin."""
    opts = None if _verify else SyncClientOptions(httpx_client=httpx.Client(verify=False))
    return create_client(SUPABASE_URL, SUPABASE_KEY, options=opts)


class CredenzialNonValideException(Exception):
    pass


class AccountBloccatoException(Exception):
    pass


class AccountSospesoException(Exception):
    pass


class EmailGiaRegistrataException(Exception):
    pass


class ServizioAuthException(Exception):
    pass


class ServizioUtenti:

    def __init__(self) -> None:
        self._repo = AttoreRepository()

    # [IF-UT.17]
    def registra_account(self, email: str, password: str, nome: str, cognome: str) -> dict:
        try:
            resp = supabase.auth.admin.create_user(
                {"email": email, "password": password, "email_confirm": True}
            )
        except AuthApiError as e:
            if e.status == 422 and any(k in str(e).lower() for k in ("already", "registered", "exists", "taken")):
                raise EmailGiaRegistrataException("Email già registrata")
            raise ServizioAuthException(str(e))
        except Exception as e:
            raise ServizioAuthException(str(e))

        user_id = UUID(resp.user.id)
        try:
            self._repo.crea_utente(user_id, nome, cognome, consenso_privacy=True)
        except Exception as exc:
            try:
                supabase.auth.admin.delete_user(str(user_id))
            except Exception:
                pass
            raise ServizioAuthException(f"Errore durante la registrazione: {exc}") from exc

        try:
            sign_in = _client_per_richiesta().auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if sign_in.session is None:
                raise ServizioAuthException("Sessione non ottenuta dopo la registrazione")
            access_token = sign_in.session.access_token
        except ServizioAuthException:
            raise
        except Exception as exc:
            raise ServizioAuthException(f"Registrazione completata ma accesso fallito: {exc}") from exc
        return {
            "access_token": access_token,
            "ruolo": "UT",
            "profilo": {
                "id": str(user_id),
                "nome": nome,
                "cognome": cognome,
                "email": email,
                "sospeso": False,
            },
        }

    # [IF-UT.18 / IF-OP.16 / IF-AP.07]
    def autentica_account(self, email: str, password: str) -> dict:
        if self._repo.conta_tentativi_falliti(email) >= self._repo.max_tentativi():
            raise AccountBloccatoException("Account bloccato per troppi tentativi falliti")

        try:
            resp = _client_per_richiesta().auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if resp.session is None or resp.user is None:
                raise CredenzialNonValideException("Credenziali non valide")
            access_token = resp.session.access_token
            user_id = UUID(resp.user.id)
        except CredenzialNonValideException:
            raise
        except Exception:
            self._repo.registra_tentativo(email, riuscito=False)
            raise CredenzialNonValideException("Credenziali non valide")

        try:
            profilo, ruolo = self._repo.trova_per_id(user_id)
        except AttoreNonTrovatoException:
            raise CredenzialNonValideException("Credenziali non valide")

        if ruolo == "UT" and profilo.sospeso:
            if profilo.sospensione_fine and profilo.sospensione_fine <= datetime.now(timezone.utc):
                self._repo.riattiva(profilo.id)
                profilo.sospeso = False
                profilo.motivazione_sospensione = None
                profilo.sospensione_fine = None
            else:
                messaggio = "Account sospeso"
                if profilo.motivazione_sospensione:
                    messaggio += f": {profilo.motivazione_sospensione}"
                if profilo.sospensione_fine:
                    messaggio += f". Tempo rimanente: {self._formatta_tempo_residuo(profilo.sospensione_fine)}"
                raise AccountSospesoException(messaggio)

        self._repo.registra_tentativo(email, riuscito=True)

        return {
            "access_token": access_token,
            "ruolo": ruolo,
            "profilo": self._build_profilo(profilo, ruolo, email),
        }

    # [IF-UT.17 / IF-UT.18 — variante OAuth]
    def accedi_oauth(self, token: str, user_id: UUID, email: str, payload: dict, consenso_privacy: bool = False) -> dict:
        """Find-or-create per utenti OAuth. Se non esiste in attori, crea come UT."""
        try:
            profilo, ruolo = self._repo.trova_per_id(user_id)
        except AttoreNonTrovatoException:
            user_meta = payload.get("user_metadata", {})
            full_name = (
                user_meta.get("full_name")
                or user_meta.get("name")
                or email.split("@")[0]
            )
            parts = full_name.strip().split(" ", 1)
            nome = parts[0]
            cognome = parts[1] if len(parts) > 1 else ""
            # [IIN-2 / GDPR art. 7] Registra il consenso raccolto nel callback OAuth
            self._repo.crea_utente(user_id, nome, cognome, consenso_privacy=consenso_privacy)
            profilo, ruolo = self._repo.trova_per_id(user_id)

        return {
            "access_token": token,
            "ruolo": ruolo,
            "profilo": self._build_profilo(profilo, ruolo, email),
        }

    def profilo_corrente(self, utente_id: UUID, email: str) -> dict:
        profilo, ruolo = self._repo.trova_per_id(utente_id)
        return {"ruolo": ruolo, "profilo": self._build_profilo(profilo, ruolo, email)}

    def modifica_dati_account(self, utente_id: UUID, nome: str, cognome: str) -> dict:
        if not nome or not nome.strip():
            raise ValueError("Il nome è obbligatorio")
        if not cognome or not cognome.strip():
            raise ValueError("Il cognome è obbligatorio")
        self._repo.aggiorna_utente(utente_id, nome.strip(), cognome.strip())
        profilo, _ = self._repo.trova_per_id(utente_id)
        return {"nome": profilo.nome, "cognome": profilo.cognome}

    # ── GDPR ──────────────────────────────────────────────────────────────────

    def esporta_dati(self, utente_id: UUID, email: str) -> dict:
        """Raccoglie tutti i dati personali (art. 20 GDPR — portabilità)."""
        dati = self._repo.esporta_dati_utente(utente_id)
        dati["profilo"]["email"] = email
        return dati

    def cancella_account(self, utente_id: UUID) -> None:
        """Elimina l'account dall'auth provider e i dati personali (art. 17 GDPR — diritto all'oblio)."""
        # Prima elimina da auth.users (Supabase), poi il record locale viene
        # eliminato in cascata tramite FK ON DELETE CASCADE (007_gdpr_cascade.sql).
        # Se la cascade non è attiva, l'eliminazione locale è gestita da elimina_utente().
        try:
            supabase.auth.admin.delete_user(str(utente_id))
        except Exception as e:
            raise ServizioAuthException(f"Impossibile eliminare l'account: {e}") from e
        # Tentativo di eliminazione esplicita (no-op se la cascade è già attiva)
        try:
            self._repo.elimina_utente(utente_id)
        except Exception:
            pass

    # [IF-OP.09] ──────────────────────────────────────────────────────────────

    def get_utenti(self) -> list[dict]:
        return self._repo.lista_utenti()

    def get_dettaglio_utente(self, utente_id: UUID) -> dict:
        return self._repo.trova_utente_per_id(utente_id)

    def sospendi_account(self, utente_id: UUID, motivazione: str, durata_giorni: int) -> None:
        if not motivazione or not motivazione.strip():
            raise ValueError("La motivazione della sospensione è obbligatoria")
        if durata_giorni < 1:
            raise ValueError("La durata della sospensione deve essere almeno 1 giorno")
        self._repo.sospendi(utente_id, motivazione, durata_giorni)
        NotificaService().notifica(
            utente_id,
            f"Il tuo account è stato sospeso per {durata_giorni} giorni. Motivo: {motivazione}",
        )

    @staticmethod
    def _formatta_tempo_residuo(fine: datetime) -> str:
        """Formatta il tempo che manca alla fine della sospensione (giorni/ore/minuti)."""
        delta = fine - datetime.now(timezone.utc)
        secondi_totali = int(delta.total_seconds())
        if secondi_totali <= 0:
            return "meno di un minuto"
        giorni, resto = divmod(secondi_totali, 86400)
        ore, resto = divmod(resto, 3600)
        minuti = resto // 60
        parti = []
        if giorni:
            parti.append(f"{giorni} giorno" if giorni == 1 else f"{giorni} giorni")
        if ore:
            parti.append(f"{ore} ora" if ore == 1 else f"{ore} ore")
        if minuti and not giorni:
            parti.append(f"{minuti} minuto" if minuti == 1 else f"{minuti} minuti")
        if not parti:
            return "meno di un minuto"
        return " e ".join(parti)

    def _build_profilo(self, profilo, ruolo: str, email: str) -> dict:
        base = {"id": str(profilo.id), "nome": profilo.nome, "email": email}
        if ruolo == "UT":
            base["cognome"] = profilo.cognome
            base["sospeso"] = profilo.sospeso
        return base

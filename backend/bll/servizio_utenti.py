from uuid import UUID
from supabase_auth.errors import AuthApiError
from config import supabase
from dal.attore_repository import AttoreRepository, AttoreNonTrovatoException


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
            # Supabase admin API returns 403 "User not allowed" when the email already exists
            if e.status == 403 or any(k in str(e).lower() for k in ("already", "registered", "exists", "taken")):
                raise EmailGiaRegistrataException("Email già registrata")
            raise ServizioAuthException(str(e))
        except Exception as e:
            raise ServizioAuthException(str(e))

        user_id = UUID(resp.user.id)
        try:
            self._repo.crea_utente(user_id, nome, cognome)
        except Exception as exc:
            try:
                supabase.auth.admin.delete_user(str(user_id))
            except Exception:
                pass
            raise ServizioAuthException(f"Errore durante la registrazione: {exc}") from exc

        try:
            sign_in = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if sign_in.session is None:
                raise ServizioAuthException("Sessione non ottenuta dopo la registrazione")
            access_token = sign_in.session.access_token
        except ServizioAuthException:
            raise
        except Exception as exc:
            raise ServizioAuthException(f"Registrazione completata ma accesso fallito: {exc}") from exc
        finally:
            # Evita che la sessione utente sovrascriva il client service-role
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
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
        if self._repo.conta_tentativi_falliti(email) >= 5:
            raise AccountBloccatoException("Account bloccato per troppi tentativi falliti")

        try:
            resp = supabase.auth.sign_in_with_password(
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
        finally:
            # Evita che la sessione utente sovrascriva il client service-role
            try:
                supabase.auth.sign_out()
            except Exception:
                pass

        try:
            profilo, ruolo = self._repo.trova_per_id(user_id)
        except AttoreNonTrovatoException:
            raise CredenzialNonValideException("Credenziali non valide")

        if ruolo == "UT" and profilo.sospeso:
            raise AccountSospesoException("Account sospeso")

        self._repo.registra_tentativo(email, riuscito=True)

        return {
            "access_token": access_token,
            "ruolo": ruolo,
            "profilo": self._build_profilo(profilo, ruolo, email),
        }

    def profilo_corrente(self, utente_id: UUID, email: str) -> dict:
        profilo, ruolo = self._repo.trova_per_id(utente_id)
        return {"ruolo": ruolo, "profilo": self._build_profilo(profilo, ruolo, email)}

    def _build_profilo(self, profilo, ruolo: str, email: str) -> dict:
        base = {"id": str(profilo.id), "nome": profilo.nome, "email": email}
        if ruolo == "UT":
            base["cognome"] = profilo.cognome
            base["sospeso"] = profilo.sospeso
        return base

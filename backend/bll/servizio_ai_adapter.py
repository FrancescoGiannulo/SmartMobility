import json
import os
import logging
import httpx
from groq import Groq

logger = logging.getLogger(__name__)


def _ssl_funziona() -> bool:
    try:
        httpx.get("https://api.groq.com", timeout=5)
        return True
    except Exception:
        return False

SYSTEM_PROMPT = """\
Sei l'assistente AI di Smart Mobility, un sistema di sharing (bike, car, e-scooter) per il Comune di Zootropolis.
Analizzi i dati di utilizzo di un utente e generi suggerimenti personalizzati per migliorare la sua esperienza.

Rispondi SOLO con un array JSON valido. Ogni elemento deve avere:
- "tipo": uno tra "risparmio", "percorso", "abbonamento", "orario", "mezzo", "generale"
- "testo": il suggerimento in italiano, breve e utile (max 2 frasi)
- "dati_contesto": oggetto con dati rilevanti usati per generare il suggerimento

Genera da 1 a 5 suggerimenti basati sui dati forniti.
Se i dati sono insufficienti, rispondi con un array vuoto: []
Non aggiungere testo fuori dall'array JSON.\
"""


class ServizioAIAdapter:
    """[IF-UT.14] Adapter per il servizio AI esterno (Groq + Llama)."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            http_client = None
            if not _ssl_funziona():
                http_client = httpx.Client(verify=False)
                logger.info("SSL Groq: verifica disabilitata (rete universitaria)")
            self._client = Groq(api_key=api_key, http_client=http_client)
        else:
            self._client = None
        self._model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def valuta_sufficienza_dati(self, dati: dict) -> bool:
        n_corse = len(dati.get("corse", []))
        return n_corse >= 1

    def genera_suggerimenti(self, dati: dict) -> list[dict]:
        if self._client is None:
            logger.warning("GROQ_API_KEY non configurata — suggerimenti disabilitati")
            return []

        if not self.valuta_sufficienza_dati(dati):
            return []

        prompt_utente = json.dumps(dati, ensure_ascii=False, default=str)

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_utente},
                ],
                temperature=0.7,
                max_tokens=1024,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "[]"
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "suggerimenti" in parsed:
                parsed = parsed["suggerimenti"]
            if not isinstance(parsed, list):
                return []
            return [
                s for s in parsed
                if isinstance(s, dict) and "tipo" in s and "testo" in s
            ]
        except Exception:
            logger.exception("Errore chiamata Groq")
            return []

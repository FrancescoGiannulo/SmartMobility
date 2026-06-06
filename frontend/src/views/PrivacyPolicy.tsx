import { useNavigate } from 'react-router-dom'
import './PrivacyPolicy.css'

export default function PrivacyPolicy() {
  const navigate = useNavigate()

  return (
    <div className="privacy-container">
      <div className="privacy-card">
        <button className="privacy-back" onClick={() => navigate(-1)} aria-label="Torna indietro">
          ← Indietro
        </button>

        <header className="privacy-header">
          <span className="privacy-logo">🚲</span>
          <h1>Privacy Policy</h1>
          <p className="privacy-updated">Ultimo aggiornamento: giugno 2026</p>
        </header>

        <section className="privacy-sezione">
          <h2>1. Titolare del Trattamento</h2>
          <p>
            Il Titolare del Trattamento dei dati personali è <strong>Smart Mobility S.r.l.</strong>
            (di seguito «Titolare»), raggiungibile all'indirizzo:{' '}
            <a href="mailto:privacy@smartmobility.it">privacy@smartmobility.it</a>.
          </p>
        </section>

        <section className="privacy-sezione">
          <h2>2. Dati raccolti e finalità del trattamento</h2>
          <table className="privacy-tabella">
            <thead>
              <tr>
                <th>Dato</th>
                <th>Finalità</th>
                <th>Base giuridica</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Nome, cognome, email</td>
                <td>Identificazione e gestione account</td>
                <td>Contratto (art. 6(1)(b) GDPR)</td>
              </tr>
              <tr>
                <td>Posizione GPS durante la corsa</td>
                <td>Erogazione del servizio di sharing</td>
                <td>Contratto (art. 6(1)(b) GDPR)</td>
              </tr>
              <tr>
                <td>Storico corse e pagamenti</td>
                <td>Fatturazione e storico personale</td>
                <td>Contratto (art. 6(1)(b) GDPR)</td>
              </tr>
              <tr>
                <td>Dati di navigazione (log)</td>
                <td>Sicurezza del sistema e antifrode</td>
                <td>Legittimo interesse (art. 6(1)(f) GDPR)</td>
              </tr>
              <tr>
                <td>Consenso privacy e timestamp</td>
                <td>Adempimento obbligo GDPR</td>
                <td>Obbligo legale (art. 6(1)(c) GDPR)</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section className="privacy-sezione">
          <h2>3. Comunicazione dei dati a terzi</h2>
          <p>
            I dati personali possono essere comunicati a soggetti terzi unicamente nelle seguenti ipotesi:
          </p>
          <ul>
            <li><strong>Supabase Inc.</strong> — fornitore di servizi di autenticazione e database cloud (Data Processor ai sensi dell'art. 28 GDPR).</li>
            <li><strong>Provider di pagamento</strong> — per l'elaborazione delle transazioni relative alle corse.</li>
            <li><strong>Autorità competenti</strong> — in caso di obbligo di legge.</li>
          </ul>
          <p>I dati non vengono ceduti né venduti a terzi per finalità di marketing.</p>
        </section>

        <section className="privacy-sezione">
          <h2>4. Trasferimento fuori dall'UE</h2>
          <p>
            Alcuni fornitori (es. Supabase) trattano i dati in paesi extra-UE. Il trasferimento avviene
            nel rispetto delle garanzie previste dagli artt. 44–49 GDPR (decisioni di adeguatezza,
            clausole contrattuali tipo della Commissione Europea).
          </p>
        </section>

        <section className="privacy-sezione">
          <h2>5. Tempi di conservazione</h2>
          <ul>
            <li><strong>Dati account e profilo:</strong> fino alla cancellazione dell'account da parte dell'utente.</li>
            <li><strong>Storico corse e pagamenti:</strong> 10 anni per adempimenti fiscali (art. 2220 c.c.).</li>
            <li><strong>Log di sicurezza:</strong> 90 giorni, poi eliminati automaticamente.</li>
          </ul>
        </section>

        <section className="privacy-sezione">
          <h2>6. Diritti dell'interessato</h2>
          <p>
            Ai sensi degli artt. 15–22 del GDPR, l'utente ha il diritto di:
          </p>
          <div className="privacy-diritti">
            {[
              { art: 'Art. 15', titolo: 'Accesso', desc: 'Richiedere una copia dei dati trattati.' },
              { art: 'Art. 16', titolo: 'Rettifica', desc: 'Correggere i dati inesatti.' },
              { art: 'Art. 17', titolo: 'Cancellazione (oblio)', desc: 'Richiedere l\'eliminazione di tutti i dati personali.' },
              { art: 'Art. 18', titolo: 'Limitazione', desc: 'Limitare il trattamento in determinate circostanze.' },
              { art: 'Art. 20', titolo: 'Portabilità', desc: 'Ricevere i dati in formato strutturato (JSON).' },
              { art: 'Art. 21', titolo: 'Opposizione', desc: 'Opporsi al trattamento basato su legittimo interesse.' },
            ].map(d => (
              <div key={d.art} className="privacy-diritto-card">
                <span className="privacy-diritto-art">{d.art}</span>
                <strong>{d.titolo}</strong>
                <p>{d.desc}</p>
              </div>
            ))}
          </div>
          <p>
            Puoi esercitare i diritti di accesso, portabilità e cancellazione direttamente dalla sezione{' '}
            <strong>Il mio profilo → Privacy e dati personali</strong> dell'applicazione, oppure
            inviando una richiesta a{' '}
            <a href="mailto:privacy@smartmobility.it">privacy@smartmobility.it</a>.
          </p>
          <p>
            Hai inoltre il diritto di proporre reclamo all'<strong>Autorità Garante per la protezione
            dei dati personali</strong> (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener noreferrer">www.garanteprivacy.it</a>).
          </p>
        </section>

        <section className="privacy-sezione">
          <h2>7. Sicurezza dei dati</h2>
          <p>
            Tutte le comunicazioni tra client e server sono cifrate mediante protocollo HTTPS/TLS.
            I token di autenticazione (JWT) sono firmati e hanno durata limitata. Il sistema adotta
            un meccanismo di blocco automatico dell'account dopo tentativi di accesso falliti
            consecutivi, configurabile dall'operatore (IIN-2).
          </p>
        </section>
      </div>
    </div>
  )
}

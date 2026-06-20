"""
Script per convertire documenti Word (.docx) in Markdown (.md).
TUTORIAL VELOCE:
Questo script richiede sempre il file di input da convertire.
Apri il terminale e usa uno dei seguenti comandi:
1. Per convertire un file (il file .md verrà salvato nella stessa cartella del file originale):
   python3 convert_docx_to_md.py "/percorso/del/tuo/file.docx"
2. Per convertire un file e scegliere dove salvare il file .md finale:
   python3 convert_docx_to_md.py "/percorso/del/tuo/file.docx" -o "percorso/di/destinazione.md"
Requisito: Assicurati di avere `pandoc` installato (es. tramite `brew install pandoc`).
"""
import subprocess
import sys
import os
import argparse
def convert_docx_to_md(docx_path, output_md_path):
    if not os.path.exists(docx_path):
        print(f"Errore: Il file '{docx_path}' non esiste.")
        sys.exit(1)
        
    print(f"Conversione di '{docx_path}' in corso...")
    try:
        # Usiamo pandoc per mantenere uno stile coerente con gli altri .md (GitHub Flavored Markdown)
        subprocess.run([
            "pandoc", 
            docx_path, 
            "-f", "docx", 
            "-t", "gfm", 
            "--wrap=none",
            "-o", output_md_path
        ], check=True)
        print(f"Successo! Il file è stato salvato in '{output_md_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la conversione con pandoc: {e}")
        print("Assicurati di avere pandoc installato nel tuo sistema.")
    except FileNotFoundError:
        print("Pandoc non trovato nel sistema. Assicurati che sia installato (es: brew install pandoc).")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converti un file Word (.docx) in Markdown (.md)")
    parser.add_argument("input_file", help="Percorso del file .docx da convertire (Obbligatorio)")
    parser.add_argument("-o", "--output", help="Percorso del file .md di destinazione (Opzionale)")
    
    args = parser.parse_args()
    
    input_path = args.input_file
    output_path = args.output
    
    # Se non è specificato l'output, salva lo stesso file sostituendo l'estensione in .md
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".md"
    
    convert_docx_to_md(input_path, output_path)

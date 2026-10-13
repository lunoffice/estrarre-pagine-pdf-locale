import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def leggi_numero(testo):
    try:
        return int(testo)
    except ValueError:
        raise ValueError(f"'{testo}' non è un numero di pagina") from None


def parse_pagine(elenco, totale):
    """Trasforma '1,3,5-7' in indici da 0: [0, 2, 4, 5, 6]."""
    indici = []
    for parte in elenco.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            da, a = parte.split("-", 1)
            inizio, fine = leggi_numero(da), leggi_numero(a)
        else:
            inizio = fine = leggi_numero(parte)
        if inizio > fine:
            raise ValueError(f"intervallo invertito: '{parte}'")
        if inizio < 1 or fine > totale:
            raise ValueError(f"'{parte}' è fuori range: il PDF ha {totale} pagine")
        indici.extend(range(inizio - 1, fine))
    if not indici:
        raise ValueError("nessuna pagina indicata")
    return indici


def salva(writer, destinazione):
    if destinazione.exists():
        sys.exit(f"Errore: {destinazione} esiste già. Scegli un'altra cartella con -o.")
    with open(destinazione, "wb") as f:
        writer.write(f)
    print(f"Creato: {destinazione}")


def main():
    ap = argparse.ArgumentParser(description="Estrae pagine da un PDF, in locale.")
    ap.add_argument("input", type=Path, help="il PDF di partenza")
    ap.add_argument("-p", "--pagine", required=True,
                    help="pagine da estrarre, contate da 1: per esempio 1,3,5-7")
    ap.add_argument("--unisci", action="store_true",
                    help="un solo file con tutte le pagine scelte")
    ap.add_argument("-o", "--output-dir", type=Path, default=Path("estratte"),
                    help="cartella di destinazione (default: estratte)")
    args = ap.parse_args()

    if not args.input.is_file():
        sys.exit(f"Errore: non trovo il file {args.input}")
    try:
        reader = PdfReader(args.input)
    except PdfReadError as e:
        sys.exit(f"Errore: il PDF non si legge ({e})")
    if reader.is_encrypted:
        sys.exit("Errore: il PDF è protetto da password. Lo script non lo apre.")
    try:
        indici = parse_pagine(args.pagine, len(reader.pages))
    except ValueError as e:
        sys.exit(f"Errore: {e}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.unisci:
        writer = PdfWriter()
        for i in indici:
            writer.add_page(reader.pages[i])
        salva(writer, args.output_dir / f"{args.input.stem}_estratte.pdf")
    else:
        for i in indici:
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            salva(writer, args.output_dir / f"pagina_{i + 1:03d}.pdf")


if __name__ == "__main__":
    main()

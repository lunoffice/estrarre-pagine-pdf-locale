# Estrarre le singole pagine da un PDF (locale)

Script Python **offline** che estrae una o più pagine da un PDF con [`pypdf`](https://pypi.org/project/pypdf/), senza caricare documenti su siti web.

Allineato alla guida Lab di ai riparo:

**[Estrarre le singole pagine da un PDF senza siti web](https://airiparo.it/lab/estrarre-pagine-pdf-locale/)**

## Caratteristiche

- Estrazione locale: dopo l’installazione di `pypdf` lo script **non** apre connessioni di rete
- Pagine contate da 1, con virgole e intervalli inclusivi: `1,3,5-7`
- Un file per pagina (`pagina_004.pdf`) oppure un solo file con `--unisci`
- Non sovrascrive file esistenti; il PDF di partenza non viene modificato
- Si ferma sui PDF protetti da password (non aggira cifratura)
- Licenza **MIT**

## Requisiti

- Python **3.9+** (testato con Python 3.12)
- Dipendenza: `pypdf` (nel `venv` del progetto)
- Windows, macOS o Linux

## Installazione

### Opzione 1 — Clona il repository

```bash
git clone https://github.com/lunoffice/estrarre-pagine-pdf-locale.git
cd estrarre-pagine-pdf-locale
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python -m pip install pypdf
```

### Opzione 2 — Solo lo script

Scarica `estrai_pagine.py` da questo repository oppure dalla scheda download su ai riparo (stesso SHA-256):

[Download verificato su ai riparo](https://airiparo.it/lab/estrarre-pagine-pdf-locale/)

## Uso

```bash
# una pagina sola
python estrai_pagine.py fascicolo.pdf -p 4

# un intervallo in un solo file
python estrai_pagine.py fascicolo.pdf -p 5-7 --unisci

# tutte le pagine, una per file, in una cartella a scelta
python estrai_pagine.py fascicolo.pdf -p 1-8 -o singole
```

Su macOS/Linux, se serve: `python3 estrai_pagine.py …`.

### Esempio di output

```text
Creato: estratte/pagina_004.pdf
```

## Opzioni della CLI

| Flag | Effetto | Default |
| --- | --- | --- |
| `input` (posizionale) | PDF di partenza (solo lettura) | — |
| `-p` / `--pagine` | Pagine da estrarre, contate da 1 (`1,3,5-7`) | obbligatorio |
| `--unisci` | Un solo file `nome_estratte.pdf`, nell’ordine scritto | un file per pagina |
| `-o` / `--output-dir` | Cartella di destinazione | `estratte` |
| `-h` / `--help` | Aiuto nativo | — |

## Note di privacy e sicurezza

- Non caricare contratti, referti o documenti d’identità su siti che dividono PDF.
- Lo script usa la posizione fisica della pagina nel file, non il numero stampato sul foglio.
- Estrarre ≠ oscurare o rimuovere metadati: il contenuto delle pagine resta identico.

## Checksum

Lo SHA-256 di `estrai_pagine.py` è pubblicato nella scheda download della guida Lab (deve coincidere con il file di questo repository).

## Licenza

MIT — Copyright (c) 2026 Alex Lunalbi (ai riparo)

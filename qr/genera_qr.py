"""Genera un QR (SVG) per ogni pagina e oggetto + elenco_url.csv.
Uso:  pip install qrcode
      python3 qr/genera_qr.py https://NOMEUTENTE.github.io/regia-dogana
Gli indirizzi derivano dai NOMI DEI FILE in _pagine e _oggetti: non rinominarli dopo la stampa."""
import sys, csv, pathlib
import qrcode, qrcode.image.svg
base = sys.argv[1].rstrip("/")
radice = pathlib.Path(__file__).resolve().parent.parent
uscita = radice / "qr" / "codici"; uscita.mkdir(exist_ok=True)
righe = []
for cartella, prefisso in (("_pagine", "pagine"), ("_oggetti", "oggetti")):
    for f in sorted((radice / cartella).glob("*.md")):
        url = f"{base}/{prefisso}/{f.stem}/"
        qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage,
                    error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4
                    ).save(str(uscita / f"{prefisso}-{f.stem}.svg"))
        righe.append((prefisso, f.stem, url))
with open(radice / "qr" / "elenco_url.csv", "w", newline="", encoding="utf-8") as c:
    w = csv.writer(c); w.writerow(["tipo", "nome_file", "url"]); w.writerows(righe)
print(len(righe), "QR creati in", uscita)

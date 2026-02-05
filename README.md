# NumericalMethods

Web aplikacija za numericku interpolaciju tackama, sa vizualizacijom i poredjenjem metoda u realnom vremenu.

<img width="1901" height="917" alt="image" src="https://github.com/user-attachments/assets/3a7feff2-612a-41eb-b8dd-14988fb487e7" />


## Pregled

Ovaj projekat je Flask web aplikacija koja omogucava unos skupa tacaka i izracunavanje interpolacije vise metoda. Rezultat je interaktivni graf (Plotly) uz prikaz osnovnih informacija o izabranoj metodi i mogucnost izvoza podataka.

## Kljucne funkcionalnosti

- Unos i uredjivanje tacaka (dodavanje, brisanje, sortiranje)
- Lagrangeova interpolacija
- Barycentric Lagrange interpolacija
- Newtonova interpolacija (podijeljene razlike)
- Linearna interpolacija
- Kubni spline (natural cubic)
- Poredjenje svih metoda na test tacki
- Izvoz tacaka u CSV
- Generisanje Python koda za plot
- Export grafa kao slike

## Tehnologije

- Python 3
- Flask 2.3.3
- Plotly (CDN)
- HTML/CSS/JS (front-end)

## Pokretanje lokalno

1. Kreiraj virtualno okruzenje (preporuceno):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instaliraj zavisnosti:

```bash
pip install -r requirements.txt
```

3. Pokreni aplikaciju:

```bash
python run.py
```

4. Otvori u browseru:

```text
http://localhost:5000
```


Napomena: Potrebne su minimum 2 tacke.

## Struktura projekta

- `app.py` - glavni Flask server i API
- `run.py` - jednostavan entrypoint
- `methods/` - implementacije interpolacionih metoda
- `templates/index.html` - UI i logika u browseru
- `static/style.css` - stilovi
- `requirements.txt` - zavisnosti

## Metode (kratko)

- Lagrange: polinom stepena n-1 kroz sve tacke
- Barycentric: numericki stabilnija varijanta Lagrangea
- Newton: polinom sa podijeljenim razlikama
- Linearna: segmentna interpolacija
- Spline: natural cubic spline (C2 kontinuitet)


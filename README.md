# PusherLux – authenticity records

Permanent online records for PusherLux bags. Each bag gets a page at
`pusherlux.github.io/<number>` (for example `pusherlux.github.io/038`) with
photos, the assessment and a downloadable PDF. The QR code on the hang tag
points to that address, so a buyer can check the bag years later.

## Struktur

| Mappe | Indhold |
|---|---|
| `records/` | Én fil pr. taske (`038.json`) med alle oplysninger og teksten til rapporten |
| `photos/<nr>/` | Redigerede billeder af tasken |
| `pdf/` | De færdige PDF-rapporter |
| `qr/` | QR-koder til hang tags (SVG og PNG) |
| `assets/` | Logo, skrifttype (EB Garamond, OFL-licens) og ikon |
| `docs/` | Den færdige hjemmeside, som GitHub Pages viser |

## Ny taske

1. Tilføj `records/<nr>.json` (kopier en eksisterende som skabelon) og billederne i `photos/<nr>/`.
2. Kør `python3 build.py`, derefter `python3 make_pdf.py <nr>`, og til sidst `python3 build.py` igen, så PDF'en kommer med i `docs/`.
3. Commit og push til `main`. GitHub Pages opdaterer siden automatisk efter et minut eller to.

Nummerering fortsætter fra lagerarket: #001–#036 har Canva-rapporter, #037 og frem ligger her.

## Hosting

GitHub Pages, gratis: Settings → Pages → Deploy from a branch → `main` / `docs`.
Repositoriet skal være offentligt og hedde `pusherlux.github.io`.

Siderne har `noindex`, så de ikke dukker op i Google-søgninger. De findes via QR-koden eller opslag på forsiden.

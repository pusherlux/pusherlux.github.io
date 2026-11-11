# PusherLux – authenticity records

Permanent online records for PusherLux bags. Each bag gets a page at
`pusherlux.com/<number>` (for example `pusherlux.com/038`) with photos, the
assessment and a downloadable PDF. The QR code on the hang tag points to that
address, so a buyer can check the bag years later.

## Struktur

| Mappe | Indhold |
|---|---|
| `records/` | Én fil pr. taske (`038.json`) med alle oplysninger og teksten til rapporten |
| `photos/<nr>/` | Redigerede billeder af tasken |
| `pdf/` | De færdige PDF-rapporter |
| `qr/` | QR-koder til hang tags (SVG og PNG) |
| `assets/` | Logo, skrifttype (EB Garamond, OFL-licens) og ikon |
| `dist/` | Den færdige hjemmeside, som Cloudflare viser |

## Ny taske

1. Tilføj `records/<nr>.json` (kopier en eksisterende som skabelon) og billederne i `photos/<nr>/`.
2. Kør `python3 build.py`, derefter `python3 make_pdf.py <nr>`, og til sidst `python3 build.py` igen, så PDF'en kommer med i `dist/`.
3. Commit og push. Cloudflare opdaterer siden automatisk.

Nummerering fortsætter fra lagerarket: #001–#036 har Canva-rapporter, #037 og frem ligger her.

## Cloudflare Pages

- Framework preset: None
- Build command: (tom)
- Build output directory: `dist`
- Custom domain: `pusherlux.com`

Siderne har `noindex`, så de ikke dukker op i Google-søgninger. De kan kun findes via QR-koden eller opslag på forsiden.

"""Build the PusherLux authenticity record site.

    python3 build.py            -> writes the website to docs/ (served by GitHub Pages)
    python3 build.py --preview  -> also writes preview/<id>/ (flat, self-contained)

Each bag is one file in records/<id>.json plus its photos in photos/<id>/.
PDFs are made separately with make_pdf.py (needs Playwright) and live in pdf/.
"""
import html
import json
import os
import shutil
import sys
from datetime import date

import qrcode
import qrcode.image.svg

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://pusherlux.github.io"
SHOP = "PusherLux"
EMAIL = "pusherlux@gmail.com"
ROMAN = ["i.", "ii.", "iii.", "iv.", "v.", "vi.", "vii.", "viii.", "ix.", "x."]

e = html.escape


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def load_records():
    recs = []
    for name in sorted(os.listdir(os.path.join(ROOT, "records"))):
        if name.endswith(".json"):
            with open(os.path.join(ROOT, "records", name), encoding="utf-8") as f:
                recs.append(json.load(f))
    return recs


def logo_svg(name="pusherlux-name-black.svg"):
    with open(os.path.join(ROOT, "assets", "logo", name), encoding="utf-8") as f:
        svg = f.read().strip()
    return svg.replace("<svg ", '<svg role="img" aria-label="PusherLux" ', 1)


def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=0,
                      error_correction=qrcode.constants.ERROR_CORRECT_M)
    return img.to_string(encoding="unicode")


FONT_CSS = """
@font-face{font-family:"EB Garamond";src:url("{a}fonts/EBGaramond-Regular.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"EB Garamond";src:url("{a}fonts/EBGaramond-Medium.woff2") format("woff2");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:"EB Garamond";src:url("{a}fonts/EBGaramond-Italic.woff2") format("woff2");font-weight:400;font-style:italic;font-display:swap}
"""

PAGE_CSS = """
:root{--ink:#111;--muted:#595959;--rule:#dcdcdc;--paper:#fff;--tint:#f4f3f1}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"EB Garamond",Garamond,Georgia,serif;font-size:18px;line-height:1.5;font-variant-numeric:lining-nums}
img{display:block;max-width:100%}
a{color:var(--ink)}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 24px;padding:22px 0 16px;border-bottom:1px solid var(--ink)}
header.top .logo svg{height:30px;width:auto}
.kicker{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.hero{display:flex;flex-wrap:wrap;gap:40px 64px;align-items:flex-start;margin-top:40px}
.hero figure{margin:0;flex:1 1 420px;min-width:0}
.hero figure img{width:100%;aspect-ratio:4/5;object-fit:cover;background:var(--tint)}
.hero .info{flex:1 1 360px;min-width:0;display:flex;flex-direction:column;gap:20px}
h1{margin:0;font-weight:400;font-size:clamp(34px,4.4vw,50px);line-height:1.06;text-wrap:balance}
.sub{margin:0;font-style:italic;font-size:19px;color:var(--muted)}
.verdict{border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:14px 0}
.verdict strong{display:block;font-weight:400;font-size:20px}
.verdict span{font-size:16px;color:var(--muted)}
dl.specs{margin:0}
dl.specs div{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid var(--rule)}
dl.specs dt{font-size:16px;color:var(--muted);flex:none}
dl.specs dd{margin:0;font-size:17px;text-align:right}
section.block{margin-top:72px}
h2{margin:0 0 12px;font-weight:400;font-size:28px}
.examined{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));column-gap:56px}
.examined article{display:flex;gap:16px;padding:16px 0;border-top:1px solid var(--rule)}
.examined .num{font-style:italic;font-size:16px;color:var(--muted);width:26px;flex:none}
.examined h3{margin:0 0 4px;font-size:18px;font-weight:500}
.examined p{margin:0;font-size:17px;color:#333}
ul.condition{margin:0;padding:0;list-style:none;columns:2 300px;column-gap:56px}
ul.condition li{break-inside:avoid;padding:10px 0;border-top:1px solid var(--rule);font-size:17px}
.grade{font-size:17px;color:var(--muted);margin:0 0 12px}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px}
.gallery figure{margin:0}
.gallery a{display:block}
.gallery img{width:100%;aspect-ratio:1/1;object-fit:cover;background:var(--tint)}
.gallery figcaption{font-style:italic;font-size:15px;color:var(--muted);margin-top:6px}
.two{display:flex;flex-wrap:wrap;gap:40px 64px}
.two>div{flex:1 1 340px;min-width:0}
ol.check{margin:0;padding-left:22px;font-size:18px}
ol.check li{margin-bottom:8px}
.about{font-size:17px;color:#333;margin:0}
.actions{margin-top:48px;display:flex;flex-wrap:wrap;gap:12px}
.button{display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border:1px solid var(--ink);text-decoration:none;font-size:14px;letter-spacing:.14em;text-transform:uppercase}
.button:hover{background:var(--ink);color:#fff}
footer.bottom{margin-top:72px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 32px;padding:24px 0 48px;border-top:1px solid var(--ink);font-size:16px;color:var(--muted)}
footer.bottom .logo svg{height:20px;width:auto}
@media (max-width:640px){
  body{font-size:17px}
  .hero{margin-top:24px;gap:28px}
  section.block{margin-top:52px}
  dl.specs div{flex-direction:column;gap:2px}
  dl.specs dd{text-align:left}
}
"""


def record_page(r, asset_root, photo_root, pdf_href):
    rid = r["id"]
    url = f"{SITE}/{rid}"
    specs = "\n".join(
        f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in r["details"])
    examined = "\n".join(
        f'<article><span class="num">{ROMAN[i]}</span><div><h3>{e(x["title"])}</h3>'
        f'<p>{e(x["text"])}</p></div></article>' for i, x in enumerate(r["examined"]))
    condition = "\n".join(f"<li>{e(c)}</li>" for c in r["condition"])
    grade = dict(r["details"]).get("Condition", "")
    gallery = "\n".join(
        f'<figure><a href="{photo_root}{e(f)}"><img src="{photo_root}{e(f)}" alt="{e(c)}" loading="lazy"></a>'
        f'<figcaption>{e(c)}</figcaption></figure>' for f, c in r["photos"])
    hero_alt = f'{r["title"]}, photographed at inspection'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{SHOP} · Authenticity record № {rid} · {e(r["title"])}</title>
<meta name="description" content="Authenticity record № {rid}: {e(r["title"])}. {e(r["verdict"])}. Inspected by {SHOP}.">
<link rel="icon" href="{asset_root}favicon.png">
<style>{FONT_CSS.replace("{a}", asset_root)}{PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
<a class="logo" href="{SITE}/" aria-label="PusherLux home">{logo_svg()}</a>
<div class="kicker">Authenticity record</div>
</header>

<main>
<section class="hero">
<figure><img src="{photo_root}{e(r["hero"])}" alt="{e(hero_alt)}"></figure>
<div class="info">
<div class="kicker">Record № {rid}</div>
<h1>{e(r["title"])}</h1>
<p class="sub">{e(r["subtitle"])}</p>
<div class="verdict"><strong>{e(r["verdict"])}.</strong><span>Independently inspected by {SHOP} on {nice_date(r["inspected"])}.</span></div>
<dl class="specs">
{specs}
</dl>
</div>
</section>

<section class="block">
<h2>What was examined</h2>
<div class="examined">
{examined}
</div>
</section>

<section class="block">
<h2>Condition</h2>
<p class="grade">{e(grade)}. Described as seen on {nice_date(r["inspected"])}.</p>
<ul class="condition">
{condition}
</ul>
</section>

<section class="block">
<h2>Photographs</h2>
<div class="gallery">
{gallery}
</div>
</section>

<section class="block two">
<div>
<h2>Is this record yours?</h2>
<ol class="check">
<li>The number on your tag reads № {rid}.</li>
<li>The code and the photographs on this page match your bag.</li>
<li>The address in your browser is {SITE.replace("https://", "")}/{rid}, as printed on the tag.</li>
</ol>
</div>
<div>
<h2>About this assessment</h2>
<p class="about">An independent opinion by {SHOP}, based on physical inspection of the item, its serial or date code, materials, stitching, hardware and construction, compared with documented authentic examples. {SHOP} is not affiliated with or endorsed by {e(r["brand"])}. This record describes the item as it was on the inspection date and is not a guarantee issued by the brand.</p>
</div>
</section>

<div class="actions"><a class="button" href="{pdf_href}" download>Download PDF</a></div>
</main>

<footer class="bottom">
<div><a class="logo" href="{SITE}/" aria-label="PusherLux home">{logo_svg()}</a><div style="margin-top:8px"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div style="align-self:flex-end">Record issued {nice_date(r["issued"])}. Permanent record at {url.replace("https://", "")}</div>
</footer>
</div>
</body>
</html>
"""


PRINT_CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#111;font-family:"EB Garamond",Garamond,Georgia,serif;font-variant-numeric:lining-nums;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:794px;height:1123px;padding:52px 60px 44px;display:flex;flex-direction:column;gap:20px;overflow:hidden;page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.head{display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid #111}
.head svg{height:24px;width:auto}
.k{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#595959}
h1{margin:0;font-weight:400;font-size:38px;line-height:1.08}
.sub{margin:6px 0 0;font-style:italic;font-size:17px;color:#595959}
.verdict{border-top:1px solid #111;border-bottom:1px solid #111;padding:11px 0;display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.verdict strong{font-weight:400;font-size:19px}
.verdict span{font-size:14px;color:#595959}
.main{display:flex;gap:32px;flex:1;min-height:0}
.main .col{flex:1;display:flex;flex-direction:column;gap:20px}
.hero{width:290px;flex:none}
.hero img{width:290px;height:362px;object-fit:cover}
dl{margin:0}
dl div{display:flex;justify-content:space-between;gap:14px;padding:6px 0;border-bottom:1px solid #d4d4d4}
dt{font-size:14px;color:#595959;flex:none}
dd{margin:0;font-size:15px;text-align:right}
h2{margin:0 0 4px;font-size:12px;font-weight:400;letter-spacing:.16em;text-transform:uppercase;color:#595959}
.verify{display:flex;gap:14px;align-items:center;margin-top:auto}
.verify svg{width:92px;height:92px;flex:none}
.verify .t{font-size:14px;line-height:1.45}
.ex div{display:flex;gap:12px;padding:6px 0;border-bottom:1px solid #d4d4d4;font-size:13.5px;line-height:1.4}
.ex .n{font-style:italic;color:#595959;width:24px;flex:none}
.ex b{font-weight:500}
.ex .x{color:#3a3a3a}
.cond li{font-size:14px;padding:4px 0}
.cond{margin:0;padding-left:18px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.grid figure{margin:0}
.grid figcaption{font-style:italic;font-size:12px;color:#595959;margin-bottom:4px}
.grid img{width:100%;height:122px;object-fit:cover}
.foot{display:flex;gap:28px;padding-top:14px;border-top:1px solid #111;margin-top:auto;align-items:flex-end}
.foot p{margin:0;flex:1;font-size:12.5px;line-height:1.5;color:#333}
.sig{width:190px;flex:none;font-size:13px}
.sig .line{height:34px;border-bottom:1px solid #111;margin-bottom:5px}
"""


def print_page(r, asset_root, photo_root):
    rid = r["id"]
    url = f"{SITE}/{rid}"
    specs = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in r["details"])
    ex = "".join(
        f'<div><span class="n">{ROMAN[i]}</span><span><b>{e(x["title"])}.</b> <span class="x">{e(x["text"])}</span></span></div>'
        for i, x in enumerate(r["examined"]))
    cond = "".join(f"<li>{e(c)}</li>" for c in r["condition"])
    caps = dict(r["photos"])
    grid = "".join(
        f'<figure><figcaption>{e(caps.get(f, ""))}</figcaption><img src="{photo_root}{e(f)}" alt=""></figure>'
        for f in r["pdf_photos"])
    grade = dict(r["details"]).get("Condition", "")
    head = f'<div class="head">{logo_svg()}<span class="k">Authenticity record № {rid}</span></div>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{SHOP} record {rid}</title>
<style>{FONT_CSS.replace("{a}", asset_root)}{PRINT_CSS}</style></head>
<body>
<section class="page">
{head}
<div><h1>{e(r["title"])}</h1><p class="sub">{e(r["subtitle"])}</p></div>
<div class="verdict"><strong>{e(r["verdict"])}.</strong><span>Inspected by {SHOP}, {nice_date(r["inspected"])}</span></div>
<div class="main">
<div class="col">
<div><h2>Item details</h2><dl>{specs}</dl></div>
<div class="verify">{qr_svg(url)}<div class="t"><span class="k">Verify online</span><br>{url.replace("https://", "")}<br>{EMAIL}</div></div>
</div>
<div class="hero"><img src="{photo_root}{e(r["hero"])}" alt=""></div>
</div>
</section>
<section class="page">
{head}
<div class="ex"><h2>What was examined</h2>{ex}</div>
<div><h2>Condition: {e(grade)}</h2><ul class="cond">{cond}</ul></div>
<div class="grid">{grid}</div>
<div class="foot">
<p>An independent opinion by {SHOP}, based on physical inspection of the item, its serial or date code, materials, stitching, hardware and construction. {SHOP} is not affiliated with or endorsed by {e(r["brand"])}. This record describes the item as it was on {nice_date(r["inspected"])} and is not a guarantee issued by the brand. Issued {nice_date(r["issued"])}.</p>
<div class="sig"><div class="line"></div>{SHOP}<br><span style="color:#595959">{EMAIL}</span></div>
</div>
</section>
</body></html>
"""


def landing_page(asset_root):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SHOP}</title><link rel="icon" href="{asset_root}favicon.png">
<style>{FONT_CSS.replace("{a}", asset_root)}{PAGE_CSS}
.center{{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;text-align:center;padding:40px 20px}}
.center svg{{width:min(520px,86vw);height:auto}}
form{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}}
input{{font:inherit;font-size:18px;padding:10px 14px;border:1px solid #111;width:180px}}
button{{font:inherit;font-size:14px;letter-spacing:.14em;text-transform:uppercase;padding:0 22px;min-height:48px;border:1px solid #111;background:#111;color:#fff;cursor:pointer}}
</style></head>
<body><main class="center">
{logo_svg("pusherlux-logo-black.svg")}
<p style="margin:12px 0 0;font-size:19px">Look up an authenticity record</p>
<form onsubmit="var n=this.n.value.replace(/\\D/g,'');if(n){{location.href='/'+n.padStart(3,'0');}}return false;">
<label for="n" class="kicker" style="align-self:center">Record №</label>
<input id="n" name="n" inputmode="numeric" placeholder="038" autocomplete="off">
<button type="submit">Open</button>
</form>
<p style="margin:0;color:#595959"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</main></body></html>
"""


def not_found_page(asset_root):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Record not found · {SHOP}</title>
<style>{FONT_CSS.replace("{a}", asset_root)}{PAGE_CSS}</style></head>
<body><main class="wrap" style="padding:80px 20px;text-align:center">
<h1>Record not found</h1>
<p class="sub" style="margin-top:12px">Check the number on your tag, or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p style="margin-top:28px"><a class="button" href="/">Look up a record</a></p>
</main></body></html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def copy_tree(src, dst):
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build(preview=False):
    recs = load_records()
    dist = os.path.join(ROOT, "docs")
    if os.path.isdir(dist):
        shutil.rmtree(dist)
    copy_tree(os.path.join(ROOT, "assets"), os.path.join(dist, "assets"))
    write(os.path.join(dist, "index.html"), landing_page("/assets/"))
    write(os.path.join(dist, "404.html"), not_found_page("/assets/"))
    write(os.path.join(dist, ".nojekyll"), "")
    for r in recs:
        rid = r["id"]
        out = os.path.join(dist, rid)
        copy_tree(os.path.join(ROOT, "photos", rid), os.path.join(out, "photos"))
        pdf_name = f"PusherLux-{rid}.pdf"
        pdf_src = os.path.join(ROOT, "pdf", pdf_name)
        if os.path.exists(pdf_src):
            shutil.copy(pdf_src, os.path.join(out, pdf_name))
        write(os.path.join(out, "index.html"), record_page(r, "/assets/", f"/{rid}/photos/", f"/{rid}/{pdf_name}"))
        # print layout, used by make_pdf.py
        write(os.path.join(ROOT, "build", "print", rid, "print.html"),
              print_page(r, "../../../assets/", f"../../../photos/{rid}/"))
        # QR code for the hang tag
        write(os.path.join(ROOT, "qr", f"{rid}.svg"), qr_svg(f"{SITE}/{rid}"))
        if preview:
            # one flat folder for previewing before the domain is live: <id>.html side by side
            write(os.path.join(ROOT, "preview", f"{rid}.html"),
                  record_page(r, "assets/", f"photos/{rid}/", f"pdf/{pdf_name}"))
    print(f"Built {len(recs)} records into docs/")


if __name__ == "__main__":
    build(preview="--preview" in sys.argv)

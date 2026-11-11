"""Render pdf/PusherLux-<id>.pdf for every record (run build.py first).

    python3 make_pdf.py          -> all records
    python3 make_pdf.py 038 039  -> only these
"""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))


def main(ids):
    os.makedirs(os.path.join(ROOT, "pdf"), exist_ok=True)
    base = os.path.join(ROOT, "build", "print")
    ids = ids or sorted(os.listdir(base))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for rid in ids:
            src = os.path.join(base, rid, "print.html")
            page.goto("file://" + src)
            page.evaluate("document.fonts.ready")
            page.wait_for_load_state("networkidle")
            out = os.path.join(ROOT, "pdf", f"PusherLux-{rid}.pdf")
            page.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
            print("wrote", os.path.relpath(out, ROOT))
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1:])

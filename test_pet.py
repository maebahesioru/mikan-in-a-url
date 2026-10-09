"""Test the petting (click directly on the cat's current x)."""
from pathlib import Path
from playwright.sync_api import sync_playwright


def log(*a):
    print(*a, flush=True)


uri = Path('/home/maebahesioru/ダウンロード/sushi_money_research/実行/240_hackclub/shrink/mikan_uri.txt').read_text(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = b.contexts[0]
    pg = ctx.new_page()
    pg.on('dialog', lambda d: d.accept())
    pg.set_viewport_size({"width": 800, "height": 600})
    pg.goto(uri, timeout=90000, wait_until='commit')
    pg.wait_for_timeout(3000)
    # read the cat's x from the app's globals
    x = pg.evaluate("() => x")
    log('cat x =', x)
    pg.mouse.click(int(x), 530)
    pg.wait_for_timeout(400)
    pg.screenshot(path='/tmp/shrink_pet.png')
    log('pet screenshot taken')
    pg.close()

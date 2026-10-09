"""Test the shrink data-URI app in the browser."""
from pathlib import Path
from playwright.sync_api import sync_playwright


def log(*a):
    print(*a, flush=True)


uri = Path('/home/maebahesioru/ダウンロード/sushi_money_research/実行/240_hackclub/shrink/mikan_uri.txt').read_text(encoding='utf-8')
log('uri len:', len(uri.encode('utf-8')))

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = b.contexts[0]
    pg = ctx.new_page()
    pg.on('dialog', lambda d: d.accept())
    pg.set_viewport_size({"width": 800, "height": 600})
    pg.goto(uri, timeout=90000, wait_until='commit')
    pg.wait_for_timeout(4000)
    log('title:', pg.title())
    # screenshot 1 (walking)
    pg.screenshot(path='/tmp/shrink_test1.png')
    # click the cat (bottom center-ish)
    pg.mouse.click(400, 530)
    pg.wait_for_timeout(700)
    pg.screenshot(path='/tmp/shrink_test2.png')
    # wait more (walking + hearts)
    pg.wait_for_timeout(1500)
    pg.screenshot(path='/tmp/shrink_test3.png')
    log('screenshots taken')
    # console errors?
    pg2 = pg
    pg.close()

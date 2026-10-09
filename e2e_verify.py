"""E2E verification of the submitted data URI: self-contained + interactivity + rendering.

Checks:
1. loads with zero external requests (the whole app = the data URI itself)
2. no console errors
3. the cat's pixels = actually drawn on the canvas (non-background colors present)
4. click on the cat = blush/hearts state (p parameter becomes > 0)
5. saves fresh screenshots for the repo
"""
from pathlib import Path
from playwright.sync_api import sync_playwright


def log(*a, **k):
    print(*a, **k)


uri = Path('/home/maebahesioru/ダウンロード/sushi_money_research/実行/240_hackclub/shrink/mikan_uri.txt').read_text(encoding='utf-8')
log('URI bytes:', len(uri.encode('utf-8')))

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = b.contexts[0]
    pg = ctx.new_page()
    pg.on('dialog', lambda d: d.accept())
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    reqs = []
    pg.on('request', lambda r: reqs.append(r.url))

    pg.set_viewport_size({"width": 800, "height": 600})
    pg.goto(uri, timeout=90000, wait_until='load')
    pg.wait_for_timeout(2500)

    log('1) title:', pg.title())
    external = [u for u in reqs if not u.startswith('data:')]
    log('2) external requests:', len(external), external[:3])
    log('3) console errors:', len(errs), errs[:3])

    # 4) canvas pixels: count orange-ish pixels (the cat)
    r = pg.evaluate("""() => {
        const c = document.getElementById('c');
        const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
        let orange = 0, dark = 0;
        for (let i = 0; i < d.length; i += 16) {
            const r = d[i], g = d[i+1], bl = d[i+2];
            if (r > 200 && g > 120 && g < 200 && bl < 130) orange++;
            if (r < 40 && g < 40 && bl < 60) dark++;
        }
        return { orange, dark, total: d.length / 16 };
    }""")
    log('4) pixels:', r)

    # 5) click the cat
    x = pg.evaluate("() => x")
    pg.mouse.click(int(x), 530)
    pg.wait_for_timeout(300)
    pval = pg.evaluate("() => p")
    log('5) petting: p =', pval, '(> 0 = blush active)')
    pg.screenshot(path='/tmp/shrink_final.png')

    # fresh screenshots
    pg.wait_for_timeout(2500)
    pg.screenshot(path=str(Path('/home/maebahesioru/ダウンロード/sushi_money_research/実行/240_hackclub/shrink/repo_screenshot.png')))

    ok = (len(external) == 0 and len(errs) == 0 and r['orange'] > 30 and pval > 0)
    log('VERDICT:', 'ALL PASS ✓' if ok else 'FAIL')
    pg.close()

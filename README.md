# Mikan in a URL 🐱

A tiny web app that fits in a single `data:text/html` URI — **2,927 bytes** (limit: 3,072).

Mikan the pixel cat walks around her tiny stage. Click her and she stops,
blushes, and hearts float up. That's it. That's the app.

Built for [Shrink](https://shrink.hackclub.com/) (Sep 29 – Oct 13).

## How to run it

Open `mikan_uri.txt` contents as a URL in your browser — the whole app IS the URL.

Or regenerate:
```bash
python3 build_app.py   # builds mikan_app.html + mikan_uri.txt + prints byte count
```

## Files

- `build_app.py` — builds the app + encodes the data URI (with assertions)
- `mikan_app.html` — readable source of the app
- `mikan_uri.txt` — the one-line data URI (the actual submission)
- `test_app.py` / `test_pet.py` — Playwright tests: loads the URI, clicks the cat, screenshots

## Design notes

- Everything is procedural: the cat is drawn with canvas `fillRect`s, the "mrrp!"
  and hearts are plain canvas text. No assets, no network, no hosting.
- Walk cycle: she wanders, pauses, flips at the edges. Click = `p=90` frames of
  blush + hearts (7 particles with velocity/alpha).
- Escaping: the URI percent-encodes `#`, `%`, `?`, `&`, quotes and spaces —
  keeping those raw would break the fragment/query parsing of the data URI
  (found the hard way: the first build silently truncated at a CSS `#`).

## Byte budget

```
app bytes:      2,344
data-URI bytes: 2,927 / 3,072
```

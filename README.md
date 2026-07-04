# Ordinary — First Dance

A private, passkey‑gated practice tool for learning the first‑dance choreography to
**"Ordinary" (Alex Warren)**, broken into 21 gapless, bar‑synced video clips with
coaching cues, a seamless play‑through player, a beat metronome, and a notes log.

**Live:** https://tnguyen2791.github.io/ordinary-first-dance/ · **Passkey:** `onemoretime`

> Personal study material derived from a public tutorial demo (Dance From Home) and the
> song audio. Not for redistribution. The passkey gates the page; the clips live in this
> public repo, so treat the link as semi‑private.

## Features
- **21 gapless clips**, each cut on a musical bar line — played in order they reconstruct
  the whole 2:29 video with no gaps.
- **Seamless play‑through** ("Play all" / "Play queued") that plays time‑ranges of one
  continuous file, so consecutive phrases have zero gap.
- **Bar labels** from the audio's real beat grid (112.34 BPM, 1 bar = 2.136 s).
- **Beat metronome** at half‑tempo (~56 BPM) with a visual beat pulse. A fixed latency
  shift of **‑220 ms** is baked in (`LAT` in `src/build_html.py`); users can fine‑tune with
  the − / + nudge (saved per‑browser).
- **Coaching cue on every scene**, plus signature‑move notes (the reach + two lifts).
- **Section quick‑queue menu** (wide screens) + Clear.
- **Progress checkboxes** and a **timestamped notes log** (Save button) — both persist in
  the browser and export/import as `.json` (restore) or `.md` (readable).

## Repo layout
```
index.html          # the deployed page (generated — do not hand‑edit)
clips/              # m01..m21.mp4 (the 21 phrase clips) + full.mp4 (continuous player)
src/
  build_html.py     # generator: reads segments.json + posters/, writes ../index.html
  segments.json     # the 21 segments: timings, bars, titles, roles, lyrics, captions
  posters/          # m01..m21.jpg poster frames (embedded as base64 into index.html)
  beat-analysis/    # how the 112 BPM beat grid was derived from the audio
REBUILD.md          # how to regenerate clips from the source video (rarely needed)
```

## Rebuild the page (after editing text, coaching, bars, passkey, metronome shift…)
```sh
cd Ordinary-First-Dance
python3 src/build_html.py      # regenerates ./index.html from src/
git add index.html src && git commit -m "…" && git push   # Pages redeploys in ~1 min
```
Common edits, all in `src/build_html.py`: `PASSWORD` (passkey), `PNOTE` (coaching cues),
`TAGLINE`, `LAT` (metronome latency shift), CSS/JS. Segment timings/labels live in
`src/segments.json`.

Regenerating the **clips** themselves (only if boundaries change) is documented in
`REBUILD.md` — needs the source video via `yt-dlp` + `ffmpeg`.

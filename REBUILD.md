# Regenerating the clips (only if segment boundaries change)

The 21 clips in `clips/` and `clips/full.mp4` are derived from the source demo video.
The page itself (`index.html`) does **not** need the source video — it only needs
`src/segments.json` + `src/posters/`. You only need the steps below if you change the
segment boundaries in `src/segments.json`.

## 1. Get the source video
```sh
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]/best" --merge-output-format mp4 \
  -o video.mp4 "https://www.youtube.com/watch?v=Wmb2wO5oBP8"
```

## 2. (Optional) re‑derive the beat grid
```sh
ffmpeg -v error -i video.mp4 -ac 1 -ar 22050 -f f32le - | python3 src/beat-analysis/phase.py
```
Result used by the project: **112.34 BPM**, 1 bar = 2.136 s, first downbeat ≈ 0.549 s.
Boundaries in `segments.json` are all placed on downbeats.

## 3. Cut the gapless clips (segment muxer = no gaps/overlaps by construction)
Boundaries are the internal `start`/`end` values from `segments.json` (drop 0 and the end):
```sh
BND="9.10,17.65,26.19,30.46,34.74,43.28,51.83,60.37,64.64,68.92,77.46,86.00,94.55,103.09,111.64,118.05,122.32,126.59,130.86,135.14"
ffmpeg -y -i video.mp4 -force_key_frames "$BND" \
  -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -vf "scale=960:-2" \
  -f segment -segment_times "$BND" -reset_timestamps 1 clips/seg%02d.mp4
# rename seg00->m01, seg01->m02, … (1-based, zero-padded)
```

## 4. Continuous file for the seamless player + posters
```sh
ffmpeg -y -i video.mp4 -force_key_frames "$BND" -c:v libx264 -preset veryfast -crf 21 \
  -pix_fmt yuv420p -c:a aac -b:a 160k -vf "scale=960:-2" -movflags +faststart clips/full.mp4
# posters: one frame per segment start (+0.25s), scaled 960 wide, into src/posters/mNN.jpg
```

## 5. Rebuild the page and deploy
```sh
python3 src/build_html.py
git add -A && git commit -m "regen clips" && git push
```

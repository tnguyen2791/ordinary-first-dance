import sys, numpy as np
raw = sys.stdin.buffer.read()
x = np.frombuffer(raw, dtype=np.float32)
sr, hop, win = 22050, 512, 1024
if len(x) < win: sys.exit("no audio")
n = 1 + (len(x)-win)//hop
w = np.hanning(win).astype(np.float32)
S = np.empty((n, win//2+1), np.float32)
for i in range(n):
    S[i] = np.abs(np.fft.rfft(x[i*hop:i*hop+win]*w))
fps = sr/hop
# full-band spectral flux
d = np.diff(S, axis=0); d[d<0]=0
flux = np.zeros(n); flux[1:] = d.sum(axis=1)
flux = np.maximum(flux-np.median(flux), 0)
# bass flux (for downbeat) bins <~160Hz
kmax = int(160*win/sr)+1
db = d[:, 1:kmax].sum(axis=1); bass = np.zeros(n); bass[1:]=db
bass = np.maximum(bass-np.median(bass),0)
# tempo via autocorrelation of flux, search 95-128 BPM
ac = np.correlate(flux, flux, 'full')[n-1:]
def lag(bpm): return 60.0/bpm*fps
best=None
for bpm in np.arange(95,128,0.05):
    L=lag(bpm); l0=int(L); fr=L-l0
    if l0+1>=len(ac): continue
    v=ac[l0]*(1-fr)+ac[l0+1]*fr
    if best is None or v>best[1]: best=(bpm,v)
bpm=best[0]; P=lag(bpm); Pi=int(round(P))
# beat phase: maximize summed flux on grid
phis=np.arange(Pi)
sc=[flux[p::Pi].sum() for p in phis]
phi=int(phis[int(np.argmax(sc))])
beats=np.arange(phi, n, P)  # fractional beat frames
# downbeat: of 4 beat-classes, which has max bass energy
bt=np.round(beats).astype(int); bt=bt[bt<n]
grp=[bass[bt[k::4]].sum() for k in range(4)]
db0=int(np.argmax(grp))
downbeats=beats[db0::4]
t0=downbeats[0]/fps
barlen=4*P/fps
print(f"BPM={bpm:.2f}  beat={60/bpm*1000:.1f}ms  P={P:.2f}fr  phi={phi}  downbeat_class={db0}")
print(f"t0(first downbeat)={t0:.3f}s  barlen={barlen:.3f}s  total={len(x)/sr:.2f}s")
nb=int((len(x)/sr - t0)/barlen)+1
print(f"bars in track (from t0): ~{nb}")
# print first 12 downbeat times
dt=[f"{d/fps:.2f}" for d in downbeats[:12]]
print("first downbeats:", ", ".join(dt))
# save grid
np.save("beatgrid_downbeats.npy", downbeats/fps)
import json
json.dump({"bpm":bpm,"t0":t0,"barlen":barlen,"beat_period_s":P/fps,
           "downbeats":[float(d/fps) for d in downbeats]}, open("beatgrid.json","w"))

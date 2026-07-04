import sys, numpy as np
raw=sys.stdin.buffer.read(); x=np.frombuffer(raw,np.float32)
sr,hop,win=22050,256,1024
n=1+(len(x)-win)//hop
w=np.hanning(win).astype(np.float32)
S=np.empty((n,win//2+1),np.float32)
for i in range(n): S[i]=np.abs(np.fft.rfft(x[i*hop:i*hop+win]*w))
fps=sr/hop
d=np.diff(S,axis=0); d[d<0]=0
flux=np.zeros(n); flux[1:]=d.sum(axis=1); flux=np.maximum(flux-np.median(flux),0)
kmax=int(160*win/sr)+1
bass=np.zeros(n); bass[1:]=d[:,1:kmax].sum(axis=1); bass=np.maximum(bass-np.median(bass),0)
# precise tempo near 112 via autocorrelation of flux
ac=np.correlate(flux,flux,'full')[n-1:]
def lag(bpm): return 60.0/bpm*fps
best=None
for bpm in np.arange(108,117,0.02):
    L=lag(bpm); l0=int(L); fr=L-l0
    if l0+1<len(ac):
        v=ac[l0]*(1-fr)+ac[l0+1]*fr
        if best is None or v>best[1]: best=(bpm,v)
bpm=best[0]; P=lag(bpm)
# fine phase: for offset phi in [0,P) sample flux (interp) at phi+k*P, maximize
ks=np.arange(0,int((n-1-0)/P))
def score(phi, env):
    t=phi+ks*P; t=t[t< n-1]
    i0=t.astype(int); fr=t-i0
    return (env[i0]*(1-fr)+env[np.minimum(i0+1,n-1)]*fr).sum()
phis=np.arange(0,P,0.05)
sc=[score(p,flux) for p in phis]
beat_phi=phis[int(np.argmax(sc))]
beat_t=beat_phi/fps
beat_s=P/fps
# downbeat: test 4 beat-classes, pick the one with max BASS energy on its beats
def classscore(c, env):
    t=beat_phi + (c+4*np.arange(0,int((n-1-beat_phi)/(4*P))))*P
    t=t[t<n-1]; i0=t.astype(int); fr=t-i0
    return (env[i0]*(1-fr)+env[np.minimum(i0+1,n-1)]*fr).sum()
cls=[classscore(c,bass) for c in range(4)]
db=int(np.argmax(cls))
down_t=(beat_phi+db*P)/fps
print(f"tempo={bpm:.2f} BPM  beat={beat_s*1000:.1f} ms  P={P:.2f} fr")
print(f"first BEAT  at {beat_t:.3f}s")
print(f"first DOWNBEAT at {down_t:.3f}s   (prev grid used 0.557s)")
# print a few downbeat times
dts=[round((beat_phi+db*P+4*P*k)/fps,3) for k in range(8)]
print("downbeats:", dts)
# also first 8 beats
bts=[round((beat_phi+P*k)/fps,3) for k in range(8)]
print("beats    :", bts)

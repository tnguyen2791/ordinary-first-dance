import subprocess, numpy as np, sys
START, DUR, FPS = 9.0, 16.0, 25   # sway section, clear weight-shifts
W,H=80,45
raw=subprocess.run(["ffmpeg","-v","error","-ss",str(START),"-t",str(DUR),"-i","video.mp4",
   "-vf",f"fps={FPS},scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
f=np.frombuffer(raw,np.uint8).astype(np.float32)
n=len(f)//(W*H); f=f[:n*W*H].reshape(n,H,W)
low=f[:,H//2:,:]                      # lower half (legs/feet)
mot=np.abs(np.diff(low,axis=0)).reshape(n-1,-1).sum(1)
mot=mot/ mot.max()
t=START+np.arange(1,n)/FPS
# smooth
k=np.hanning(5); k/=k.sum(); ms=np.convolve(mot,k,'same')
# audio grid
BEAT=60/112.34; b0=0.015                         # full-tempo beats
beats=[b0+i*BEAT for i in range(int(START/BEAT), int((START+DUR)/BEAT)+1)]
beats=[b for b in beats if START<b<START+DUR]
# for each audio beat, is it near a motion MIN (plant) or MAX (moving)?
def val(tt):
    i=int(round((tt-t[0])*FPS)); i=max(0,min(len(ms)-1,i)); return ms[i]
# local min/max detection
mins=[t[i] for i in range(2,len(ms)-2) if ms[i]<=ms[i-1] and ms[i]<=ms[i+1] and ms[i]<0.5]
print("motion MINIMA (feet settled) times:", [round(x,2) for x in mins][:16])
print("audio beat grid times            :", [round(x,2) for x in beats][:16])
# offset: nearest motion-min to each audio beat
offs=[]
for b in beats:
    if mins:
        d=min(mins,key=lambda m:abs(m-b)); offs.append(d-b)
offs=np.array(offs)
print(f"median(min - beat) offset = {np.median(offs)*1000:+.0f} ms  (spread {offs.std()*1000:.0f} ms)")
print("=> if ~0, audio beats already on the plant; if ~±267ms, they're a half-beat off (on the 'up').")

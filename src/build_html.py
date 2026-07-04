#!/usr/bin/env python3
import json, base64, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
# Output to the repo root (parent of this src/ dir), or override with ORD_DEST.
DEST = os.environ.get("ORD_DEST") or os.path.dirname(HERE)
seg = json.load(open(os.path.join(HERE, "segments.json")))["segments"]

# coaching cue for EVERY scene (signature three refined w/ advisor input)
PNOTE = {
    "01": "Walk in on the music, eyes on each other from the first step. Don't rush to center — the entrance sets the whole tone.",
    "02": "Build the frame: her left hand on his shoulder, his right on her shoulder blade. Firm but soft; settle your weight before you move.",
    "03": "Sway from the hips, knees soft, weight rolling foot to foot. Stay chest-to-chest with level heads — no bobbing.",
    "04": "He gives a clear, stable raised hand; she keeps her own balance and spots the turn, finishing square to him.",
    "05": "Commit to the shape — arms long, chin up, let the gown do the talking. Hold it a beat so the camera catches it.",
    "06": "Come back together softly, no bump. Rebuild the frame and breathe the phrase — this is the intimate reset.",
    "07": "Small turns from the standing leg, don't muscle them. Keep the box compact so you stay centered on the floor.",
    "08": "Travel on the strong beats with the gown sweeping; he leads the direction, she trusts the rotation. Smooth, not fast.",
    "09": "Gather your momentum and aim it toward the open line coming next — think 'wind up' before the reach.",
    "10": "Commit weight into the counterbalance and breathe out on the extension; eyes reach past your fingertips, not down.",
    "11": "Draw her in on one smooth pull, then step out side-by-side — match stride length so you travel as one.",
    "12": "Keep one hand connected as you circle, eye contact the whole way. The turn is calm — let the music carry it.",
    "13": "Breathing room: soft knees, easy steps, connected through the fingertips. Save energy — the lift is coming.",
    "14": "Close the distance deliberately; arrive at center with weight settled and frames ready. Set your feet for the build.",
    "15": "Play the give-and-take — he offers, she answers. Keep arms toned, not stiff, so the lead reads clearly.",
    "16": "Lift from the legs, not the back; Follow holds frame and spots the window — trust over tension.",
    "17": "Lower her with control all the way down — no drop. Land into an embrace and share one breath before moving on.",
    "18": "Big arms, open chest, chins up — present to the room like you mean it. Enjoy this 'we did it' beat.",
    "19": "He sends, she spins with a clean spot and returns on balance. Keep it light and airy, setting up the finale.",
    "20": "This is the photo — sustain the height, chins up, breathe together; land soft and hold the gaze.",
    "21": "Settle into the last embrace and HOLD — don't break early. Let the music resolve; that stillness is the picture.",
}
TAGLINE = ("From a first tentative touch to a soaring lift and back to a quiet embrace — "
           "two people spend the song finding, testing, and finally choosing each other.")

# passkey for the public link (client-side gate). Change PASSWORD and rebuild to rotate it.
PASSWORD = "onemoretime"
PASS_B64 = base64.b64encode(PASSWORD.encode()).decode()

def mmss(t):
    return f"{int(t//60)}:{int(round(t%60)):02d}"

def esc(s):
    return html.escape(s, quote=True)

def b64poster(pid):
    p = os.path.join(HERE, "posters", f"m{pid}.jpg")
    return base64.b64encode(open(p, "rb").read()).decode()

CSS = """
:root{--ink:#2b2622;--muted:#8a7f76;--line:#e7ded3;--paper:#fbf8f4;--card:#fff;
      --gold:#b08d57;--rose:#c98a86;--lead:#5b7b8a;--follow:#c98a86;--sig:#b08d57;--done:#3f9d5a}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
     font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.5}
.wrap{max-width:min(96vw,1500px);margin:0 auto;padding:24px 20px 90px}
header{text-align:center;padding:22px 12px 8px;border-bottom:1px solid var(--line);margin-bottom:8px}
h1{font-family:Georgia,serif;font-weight:500;font-size:2.4rem;margin:0 0 6px}
h1 .amp{color:var(--rose)}
.tag{color:var(--ink);font-family:Georgia,serif;font-style:italic;font-size:1.05rem;margin:0 auto 14px;max-width:640px;opacity:.85}
.sub{color:var(--muted);font-size:1rem;margin:0 0 16px}
.meta{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:center;font-size:.85rem;color:var(--muted)}
.meta b{color:var(--ink);font-weight:600}
.legend{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:14px 0 2px;font-size:.8rem}
.pill{display:inline-flex;align-items:center;gap:6px;padding:3px 11px;border-radius:999px;border:1px solid var(--line);background:#fff}
.dot{width:9px;height:9px;border-radius:50%}
.dot.lead{background:var(--lead)}.dot.follow{background:var(--follow)}.dot.sig{background:var(--sig)}
.progress{position:sticky;top:0;z-index:30;background:rgba(251,248,244,.96);backdrop-filter:blur(8px);
   border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:14px 0 4px;
   display:flex;align-items:center;gap:12px;flex-wrap:wrap;box-shadow:0 2px 10px rgba(60,45,30,.05)}
.pbar{flex:1;min-width:130px;height:10px;background:#eee5d8;border-radius:999px;overflow:hidden}
.fill{height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--rose));transition:width .25s ease}
.pmeta{font-size:.86rem;color:var(--muted);display:flex;align-items:center;gap:8px;white-space:nowrap}
.pmeta #count{font-weight:700;color:var(--ink)}
.pct{color:var(--gold);font-weight:700}
#reset{border:1px solid var(--line);background:#fff;border-radius:8px;padding:5px 11px;font-size:.8rem;cursor:pointer;color:var(--muted)}
#reset:hover{color:var(--ink);border-color:var(--muted)}
.note{max-width:820px;margin:18px auto 8px;font-size:.9rem;color:#6f655c;background:#fff;border:1px solid var(--line);
      border-left:3px solid var(--gold);border-radius:8px;padding:12px 16px}
.sectionhead{font-family:Georgia,serif;font-size:1.12rem;color:var(--gold);text-transform:uppercase;letter-spacing:2px;
     margin:30px 4px 2px;padding-bottom:6px;border-bottom:1px dashed var(--line)}
.cards{display:flex;flex-direction:column;gap:18px;margin-top:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;
      box-shadow:0 1px 3px rgba(60,45,30,.05);display:flex;flex-direction:column;transition:border-color .15s,opacity .15s}
.card.sig{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold) inset,0 2px 12px rgba(176,141,87,.14)}
.card.done{border-color:var(--done)}
.card.done .thumb{opacity:.82}
.thumb{position:relative;aspect-ratio:16/9;background:#111}
.thumb video{width:100%;height:100%;object-fit:cover;display:block}
.num{position:absolute;top:12px;left:12px;min-width:32px;height:32px;padding:0 9px;border-radius:999px;background:rgba(43,38,34,.82);
     color:#fff;font-size:.86rem;font-weight:600;display:flex;align-items:center;justify-content:center;z-index:2;pointer-events:none}
.tstamp{position:absolute;top:12px;right:12px;background:rgba(255,255,255,.92);color:var(--ink);font-size:.8rem;
      font-weight:600;padding:4px 10px;border-radius:999px;z-index:2;pointer-events:none}
.done-ribbon{position:absolute;bottom:12px;left:12px;background:var(--done);color:#fff;font-size:.74rem;font-weight:700;
      letter-spacing:.4px;padding:3px 10px;border-radius:999px;z-index:2;pointer-events:none;display:none}
.card.done .done-ribbon{display:inline-block}
.body{padding:15px 18px 16px;display:flex;flex-direction:column}
.metarow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.bars{font-family:Georgia,serif;font-weight:700;font-size:.82rem;color:#fff;background:var(--gold);padding:3px 10px;border-radius:999px}
.bars::before{content:"\\266A  "}
.trange{font-size:.82rem;color:var(--muted);font-weight:600}
.title{font-weight:600;font-size:1.12rem;margin:0 0 6px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.rtag{font-size:.64rem;text-transform:uppercase;letter-spacing:.5px;padding:2px 7px;border-radius:5px;color:#fff}
.rtag.lead{background:var(--lead)}.rtag.follow{background:var(--follow)}.rtag.both{background:#a99}
.sigbadge{font-size:.62rem;font-weight:700;letter-spacing:.5px;color:#fff;background:var(--gold);padding:2px 7px;border-radius:5px}
.lyric{margin:0 0 7px;font-family:Georgia,serif;font-style:italic;color:var(--rose);font-size:.96rem}
.lyric::before{content:"\\201C"}.lyric::after{content:"\\201D"}
.lyric.inst{color:var(--muted);font-style:normal}
.lyric.inst::before,.lyric.inst::after{content:""}
.cap{color:#5f564e;font-size:.94rem;margin:0 0 10px}
.pnote{font-size:.9rem;color:#7a5a25;background:#faf3e6;border:1px solid #ecd9b6;border-radius:8px;padding:9px 12px;margin:0 0 12px}
.pnote b{color:var(--gold)}
.got{align-self:flex-start;display:inline-flex;align-items:center;gap:9px;padding:9px 16px;border:1px solid var(--line);border-radius:999px;
     cursor:pointer;font-size:.9rem;user-select:none;-webkit-tap-highlight-color:transparent;color:var(--muted);transition:.15s}
.got input{width:18px;height:18px;accent-color:var(--done);cursor:pointer;margin:0}
.card.done .got{background:#eaf5ee;border-color:#9eccac;color:#2f6b43;font-weight:600}
.cardnote{margin-top:10px;width:100%;border:1px solid var(--line);border-radius:8px;padding:8px 10px;
  font:inherit;font-size:.88rem;color:var(--ink);background:#fffdfa;resize:vertical;min-height:40px}
.cardnote::placeholder{color:#b8ac9f}
.cardnote:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 2px rgba(176,141,87,.15)}
.notespanel{max-width:820px;margin:12px auto 4px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.nhead{font-family:Georgia,serif;color:var(--ink);font-size:1rem;margin:0 0 8px;display:flex;gap:8px;align-items:center}
.nsave{font-size:.72rem;color:var(--done);opacity:0;transition:opacity .2s;font-family:-apple-system,sans-serif}
.nsave.show{opacity:1}
#globalnotes{width:100%;border:1px solid var(--line);border-radius:8px;padding:10px 12px;font:inherit;
  font-size:.92rem;background:#fffdfa;resize:vertical;min-height:72px;color:var(--ink)}
#globalnotes::placeholder{color:#b8ac9f}
#globalnotes:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 2px rgba(176,141,87,.15)}
.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:2px}
.queue{display:inline-flex;align-items:center;gap:7px;padding:9px 14px;border:1px solid var(--line);border-radius:999px;
  cursor:pointer;font-size:.86rem;color:var(--muted);user-select:none;-webkit-tap-highlight-color:transparent;transition:.15s}
.queue input{width:17px;height:17px;accent-color:var(--gold);margin:0;cursor:pointer}
.card.queued .queue{background:#f6efe2;border-color:var(--gold);color:#8a6a2e;font-weight:600}
.card.playing{border-color:var(--rose);box-shadow:0 0 0 2px var(--rose),0 6px 20px rgba(201,138,134,.25)}
.playbar{position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:50;display:flex;align-items:center;gap:10px;
  background:rgba(43,38,34,.94);backdrop-filter:blur(8px);color:#fff;padding:9px 12px;border-radius:999px;
  box-shadow:0 8px 28px rgba(0,0,0,.28);font-size:.86rem}
.playbar button{border:0;border-radius:999px;padding:8px 15px;font-size:.85rem;font-weight:600;cursor:pointer}
.playbar .primary{background:var(--gold);color:#fff}
.playbar .primary:hover{background:#c39c63}
.playbar .ghost{background:rgba(255,255,255,.14);color:#fff}
.playbar .ghost:hover{background:rgba(255,255,255,.24)}
.playbar select{border:0;border-radius:999px;padding:7px 10px;font-size:.82rem;font-weight:600;
  background:rgba(255,255,255,.16);color:#fff;cursor:pointer}
.playbar select option{color:#2b2622}
.mnudge{display:inline-flex;align-items:center;gap:4px;color:#eadfd2;font-size:.78rem}
.mnudge button{background:rgba(255,255,255,.16);color:#fff;border:0;border-radius:6px;padding:3px 9px;font-size:.9rem;line-height:1;cursor:pointer;font-weight:700}
.mnudge button:hover{background:rgba(255,255,255,.28)}
.mnudge #mOff{min-width:46px;text-align:center;font-variant-numeric:tabular-nums}
.playbar label{display:inline-flex;align-items:center;gap:6px;color:#eadfd2;cursor:pointer}
.playbar input{accent-color:var(--gold);width:15px;height:15px}
.playbar #nowplaying{color:#e9c893;font-size:.8rem;max-width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media(max-width:600px){.playbar{flex-wrap:wrap;max-width:94vw;justify-content:center;bottom:10px;gap:8px}}
.stage[hidden]{display:none}
.stage{position:fixed;inset:0;z-index:80;background:rgba(20,16,12,.92);backdrop-filter:blur(5px);
  display:flex;align-items:center;justify-content:center;padding:20px}
.stage-inner{width:min(94vw,1180px);display:flex;flex-direction:column;gap:12px;align-items:center;position:relative}
.beatdot{position:absolute;top:16px;left:16px;width:24px;height:24px;border-radius:50%;background:#fff;opacity:.18;
  transform:scale(1);pointer-events:none;z-index:4;box-shadow:0 0 0 2px rgba(255,255,255,.35)}
.beatdot.hit{animation:beatpulse .2s ease}
.beatdot.hit.down{background:var(--gold);box-shadow:0 0 0 3px rgba(176,141,87,.5)}
@keyframes beatpulse{0%{transform:scale(1.9);opacity:1}100%{transform:scale(1);opacity:.18}}
.stage-inner video{width:100%;max-height:72vh;border-radius:14px;background:#000;box-shadow:0 12px 44px rgba(0,0,0,.5)}
.stage-cap{color:#f4ece0;text-align:center;font-size:1rem;display:flex;flex-direction:column;align-items:center;gap:4px}
#stageBars{background:var(--gold);color:#fff;padding:3px 11px;border-radius:999px;font-weight:700;font-size:.85rem}
#stageBars::before{content:"\\266A  "}
#stageTitle{font-weight:600;margin-top:2px}
#stageLyric{font-family:Georgia,serif;font-style:italic;color:#e6b9b4}
.stage-ctrls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;color:#eadfd2;font-size:.82rem}
.sctl{border:0;background:rgba(255,255,255,.16);color:#fff;padding:8px 16px;border-radius:999px;font-weight:600;cursor:pointer}
.sctl.on{background:var(--gold)}
.stage-close{border:0;background:rgba(255,255,255,.16);color:#fff;padding:9px 18px;border-radius:999px;font-weight:600;cursor:pointer}
.stage-close:hover{background:rgba(255,255,255,.26)}
footer{margin-top:44px;padding:22px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}
footer h3{font-family:Georgia,serif;color:var(--ink);font-weight:500;margin:0 0 8px}
footer ul{margin:6px 0 0;padding-left:18px}footer li{margin:4px 0}
/* THEATER: wide screens -> video and details side by side, player grows with window */
@media(min-width:860px){
  .card{flex-direction:row;align-items:stretch}
  .thumb{flex:1.7 1 0;min-width:0;aspect-ratio:16/9}
  .body{flex:1 1 0;min-width:280px;justify-content:center}
}
@media(max-width:600px){
  .wrap{padding:18px 12px 60px}
  h1{font-size:1.85rem}.tag{font-size:.98rem}
  .sectionhead{font-size:1.02rem;letter-spacing:1.5px;margin-top:24px}
  .title{font-size:1.05rem}
  .got{padding:11px 18px;font-size:.94rem}
}
/* passkey gate */
.gate{position:fixed;inset:0;z-index:200;background:linear-gradient(160deg,#2b2622,#4a3f34);
  display:flex;align-items:center;justify-content:center;padding:20px}
.gate[hidden]{display:none}
.gate-box{background:#fbf8f4;border-radius:16px;padding:30px 28px;max-width:340px;width:100%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.gate-emoji{font-size:2rem}
.gate-box h2{font-family:Georgia,serif;font-weight:500;margin:.3rem 0 .1rem}
.gate-box p{color:var(--muted);font-size:.9rem;margin:.3rem 0 1rem}
.gate-box input{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:10px;font-size:1rem;margin-bottom:10px}
.gate-box input:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,141,87,.15)}
.gate-box button{width:100%;padding:11px;border:0;border-radius:10px;background:var(--gold);color:#fff;font-weight:700;font-size:1rem;cursor:pointer}
.gate-box button:hover{background:#c39c63}
.gate-err{color:#c0392b!important;min-height:1em;font-size:.85rem!important;margin:.6rem 0 0!important}
/* notes tools + timestamps */
.nhead{flex-wrap:wrap}
.ntools{display:inline-flex;gap:6px;margin-left:auto;flex-wrap:wrap}
.ntools button,.impbtn{border:1px solid var(--line);background:#fff;border-radius:8px;padding:5px 10px;font-size:.76rem;color:var(--muted);cursor:pointer}
.ntools button:hover,.impbtn:hover{color:var(--ink);border-color:var(--muted)}
.impbtn{display:inline-flex;align-items:center}
.nstamp{font-size:.72rem;color:#b0a596;margin-top:4px;min-height:.9em}
.noteslog{display:flex;flex-direction:column;gap:8px;margin-bottom:10px}
.logitem{background:#faf6ef;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:8px;padding:8px 10px}
.logmeta{display:flex;justify-content:space-between;align-items:center;font-size:.72rem;color:var(--muted);margin-bottom:3px}
.logdel{border:0;background:transparent;color:var(--muted);cursor:pointer;font-size:1.05rem;line-height:1;padding:0 2px}
.logdel:hover{color:#c0392b}
.logtext{font-size:.92rem;color:var(--ink);white-space:pre-wrap}
.savenote{margin-top:8px;border:0;background:var(--gold);color:#fff;border-radius:8px;padding:9px 18px;font-weight:600;font-size:.88rem;cursor:pointer}
.savenote:hover{background:#c39c63}
.practice{max-width:820px;margin:14px auto 4px;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.practice>summary{cursor:pointer;list-style:none;padding:14px 18px;font-family:Georgia,serif;font-size:1.06rem;color:var(--ink);
  background:linear-gradient(0deg,#fff,#fbf4e9);display:flex;align-items:center;gap:8px}
.practice>summary::-webkit-details-marker{display:none}
.practice>summary::after{content:"\\25B8";margin-left:auto;color:var(--gold);transition:transform .2s}
.practice[open]>summary::after{transform:rotate(90deg)}
.practice .ptap{color:var(--muted);font-family:-apple-system,sans-serif;font-size:.78rem;font-style:italic}
.pbody{padding:2px 20px 18px;font-size:.92rem;color:#514a42;line-height:1.6}
.pbody h4{font-family:Georgia,serif;color:var(--gold);margin:16px 0 6px;font-size:1rem}
.pbody ol,.pbody ul{margin:6px 0;padding-left:20px}
.pbody li{margin:5px 0}
.pbody .lead{font-style:italic;color:var(--rose);font-family:Georgia,serif;font-size:1rem}
.pbody .kicker{background:#faf3e6;border-left:3px solid var(--gold);border-radius:8px;padding:10px 14px;margin:14px 0 0;color:#7a5a25}
.secmenu{display:none;position:fixed;top:74px;right:16px;width:198px;max-height:calc(100vh - 150px);overflow:auto;
  background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 26px rgba(60,45,30,.14);padding:12px;flex-direction:column;gap:6px;z-index:40}
.sm-head{font-family:Georgia,serif;color:var(--gold);text-transform:uppercase;letter-spacing:1px;font-size:.72rem;margin-bottom:4px}
.secToggle{display:flex;justify-content:space-between;align-items:center;gap:8px;border:1px solid var(--line);background:#fff;border-radius:8px;padding:7px 10px;font-size:.82rem;color:var(--ink);cursor:pointer;text-align:left}
.secToggle em{font-style:normal;color:var(--muted);font-size:.72rem}
.secToggle:hover{border-color:var(--muted)}
.secToggle.some{border-color:var(--gold);background:#faf5ec}
.secToggle.on{background:var(--gold);color:#fff;border-color:var(--gold)}
.secToggle.on em{color:#f4e7d0}
.sm-clear{margin-top:6px;border:1px solid var(--line);background:#fff;border-radius:8px;padding:7px;font-size:.8rem;color:var(--muted);cursor:pointer}
.sm-clear:hover{color:var(--ink);border-color:var(--muted)}
@media(min-width:1200px){ .secmenu{display:flex} body{padding-right:226px} }
"""

def card(s):
    sig = s["sig"] == 1
    cls = "card sig" if sig else "card"
    sigb = '<span class="sigbadge">&#9733; SIGNATURE</span>' if sig else ""
    lyr = s["lyric"]
    lcls = "lyric inst" if lyr.strip().startswith("(") else "lyric"
    lyr_html = esc(lyr[1:-1]) if lcls == "lyric inst" and lyr.startswith("(") and lyr.endswith(")") else esc(lyr)
    if lcls == "lyric inst":
        lyr_html = esc(lyr.strip("()"))
    pnote = ""
    if s["id"] in PNOTE:
        pnote = f'<p class="pnote"><b>&#127775; Coaching:</b> {esc(PNOTE[s["id"]])}</p>'
    trange = f'{mmss(s["start"])}–{mmss(s["end"])}'
    return f'''<div class="{cls}" data-id="{s['id']}">
  <div class="thumb">
    <video controls loop preload="none" playsinline poster="data:image/jpeg;base64,{b64poster(s['id'])}">
      <source src="clips/m{s['id']}.mp4" type="video/mp4">
    </video>
    <div class="num">{s['id']}</div><div class="tstamp">{trange}</div>
    <div class="done-ribbon">&#10003; LEARNED</div>
  </div>
  <div class="body">
    <div class="metarow"><span class="bars">Bars {esc(s['bars'])}</span></div>
    <p class="title">{esc(s['title'])} <span class="rtag {s['role']}">{s['role']}</span>{sigb}</p>
    <p class="{lcls}">{lyr_html}</p>
    <p class="cap">{esc(s['cap'])}</p>
    {pnote}
    <div class="controls">
      <label class="got"><input type="checkbox" class="chk" data-id="{s['id']}"> Got it</label>
      <label class="queue"><input type="checkbox" class="pq" data-id="{s['id']}" data-section="{esc(s['section'])}"> &#9654; Queue</label>
    </div>
    <textarea class="cardnote" data-id="{s['id']}" rows="2" placeholder="Notes for this phrase — counts, fixes, reminders…"></textarea>
    <div class="nstamp cardstamp" data-id="{s['id']}"></div>
  </div>
</div>'''

# group by section preserving order
out = []
prev = None
for s in seg:
    if s["section"] != prev:
        if prev is not None:
            out.append("</div>")
        out.append(f'<div class="sectionhead">{esc(s["section"])}</div>\n<div class="cards">')
        prev = s["section"]
    out.append(card(s))
out.append("</div>")
cards_html = "\n".join(out)

N = len(seg)
seg_json = json.dumps([{"id":s["id"],"start":round(s["start"],3),"end":round(s["end"],3),
                        "bars":s["bars"],"title":s["title"],"lyric":s["lyric"]} for s in seg],
                      ensure_ascii=False)
# section -> ids, in order, for the quick-queue menu
_secmap = {}
for s in seg: _secmap.setdefault(s["section"], []).append(s["id"])
_sec_rows = "".join(f'<button class="secToggle" data-section="{esc(k)}">{esc(k)} <em>{len(v)}</em></button>'
                    for k, v in _secmap.items())
secmenu_html = (f'<aside class="secmenu" id="secmenu"><div class="sm-head">Add to queue</div>'
                f'{_sec_rows}<button class="sm-clear" id="clearQueue">Clear queue</button></aside>')

PRACTICE = """<details class="practice">
  <summary>&#127891; How to practice — a coach's guide <span class="ptap">(tap to open)</span></summary>
  <div class="pbody">
    <p class="lead">Train it until you can forget it &mdash; then go be a couple in love on a dance floor.</p>
    <h4>A repeatable 25&ndash;30 min session</h4>
    <ol>
      <li><b>Warm up (3 min)</b> &mdash; sway through the song once, find the frame &amp; eye contact, turn &#9835; Beat on.</li>
      <li><b>Review (5 min)</b> &mdash; replay yesterday's phrases at 0.5&times;, then full speed. No new material until the old feels easy.</li>
      <li><b>Learn ONE chunk (8 min)</b> &mdash; one or two phrases: watch at 0.5&times;, walk the footwork slowly, then add music. Read the scene's &#127775; Coaching cue first.</li>
      <li><b>Drill the hard bit (5 min)</b> &mdash; isolate the turn or lift; 8&ndash;10 slow, correct reps. Quality over tired reps.</li>
      <li><b>Link &amp; run (4 min)</b> &mdash; queue the new chunk with the one before it, play back-to-back; end on a clean run of all you know.</li>
      <li><b>Log it (1 min)</b> &mdash; tick &ldquo;Got it&rdquo;, Save a note on what to fix tomorrow.</li>
    </ol>
    <h4>Rules of thumb</h4>
    <ul>
      <li><b>Learn it &rarr; link it &rarr; live it.</b> Don't skip linking (transitions break first) or living (dance it as music, not counts).</li>
      <li><b>Connection over steps.</b> Soft breathing and real eye contact beats a busy routine danced at your feet.</li>
      <li><b>Lifts get their own lane.</b> Rehearse separately on carpet with a verbal &ldquo;down&rdquo; every time &mdash; stop the moment either of you tires.</li>
      <li><b>Film a full run weekly.</b> The phone shows the drift and tense shoulders you can't feel.</li>
      <li><b>Dress-rehearse late</b> &mdash; a few sessions in the real shoes and a practice skirt.</li>
    </ul>
    <h4>Is there such a thing as learning too much?</h4>
    <p>Yes &mdash; it's the common trap. The goal is <b>automaticity, not perfection</b>: drill just enough that your body runs it so your mind can be present. Past that point you start over-thinking, which reads as stiff (&ldquo;paralysis by analysis&rdquo;). The curve goes clueless &rarr; solid &rarr; polished &rarr; <i>robotic and joyless</i> &mdash; and that last step is real.</p>
    <ul>
      <li><b>Protect the fun.</b> If a session turns into a fight, stop and just dance the song with no counts. That's the whole point.</li>
      <li><b>Taper, don't cram.</b> Final week = light run-throughs only; learn nothing new.</li>
      <li><b>Simple &amp; owned</b> beats ambitious &amp; white-knuckled. If a phrase still scares you two weeks out, simplify or cut it &mdash; nobody knows what you planned.</li>
    </ul>
    <p class="kicker">Sweet spot: when a full run feels <i>easy and joyful</i>, you're done refining &mdash; start &ldquo;living&rdquo; it to the music.</p>
  </div>
</details>"""
HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ordinary — Alex Warren · First Dance (continuous + bars)</title>
<style>{CSS}</style>
</head>
<body>
<div class="gate" id="gate">
  <div class="gate-box">
    <div class="gate-emoji">&#128131;&#127997;&#8205;&#9792;&#65039;</div>
    <h2>Ordinary &middot; First Dance</h2>
    <p>Enter the passkey to view.</p>
    <input type="password" id="gatePass" placeholder="Passkey" autocomplete="off" autocapitalize="off" spellcheck="false">
    <button id="gateBtn" type="button">Unlock</button>
    <p class="gate-err" id="gateErr"></p>
  </div>
</div>
<div class="wrap">
<header>
  <h1>Ordinary <span class="amp">&#10084;</span> First Dance</h1>
  <p class="tag">{esc(TAGLINE)}</p>
  <p class="sub">Alex Warren · {N} gapless clips · bar-by-bar · 112 BPM</p>
  <div class="meta">
    <span><b>Source</b> Dance From Home (demo)</span>
    <span><b>Covers</b> the whole video, 0:00–2:29</span>
    <span><b>Roles</b> Lead = grey suit · Follow = white gown</span>
  </div>
  <div class="legend">
    <span class="pill"><span class="dot lead"></span> Lead-driven</span>
    <span class="pill"><span class="dot follow"></span> Follow features</span>
    <span class="pill"><span class="dot sig"></span> Signature moment</span>
  </div>
</header>

<div class="progress">
  <div class="pbar"><div class="fill" id="fill"></div></div>
  <div class="pmeta"><span id="count">0 / {N}</span> learned · <span class="pct" id="pct">0%</span>
     <button id="reset" type="button">Reset</button></div>
</div>

<div class="note"><b>The clips are continuous</b> — played in order (01 → {N:02d}) they rebuild the entire video with
no gaps or repeats, each cut on a musical bar line. Every card shows which <b>bars</b> of the song it covers and the
lyric you’ll hear. Tick <b>&ldquo;Got it&rdquo;</b> as you nail each phrase; progress saves in this browser. Gold cards are the
three signature moments (the reach + two lifts). Widen the window and the player grows.<br>
<b>Play-through:</b> tick <b>&#9654; Queue</b> on the phrases you want and hit <b>Play queued</b> (bottom bar) to run them
back-to-back; or <b>Play all</b> for the whole dance end-to-end.</div>

<div class="notespanel">
  <div class="nhead">&#128221; My notes <span class="nsave" id="gnsave"></span>
    <span class="ntools">
      <button id="expJson" type="button">&#8595; Save file (.json)</button>
      <button id="expMd" type="button">&#8595; Readable (.md)</button>
      <label class="impbtn">&#8593; Load<input type="file" id="impFile" accept="application/json,.json" hidden></label>
    </span>
  </div>
  <div class="noteslog" id="noteslog"></div>
  <textarea id="globalnotes" placeholder="Type a note — problem spots, counts, what to drill… then Save (or ⌘/Ctrl+Enter)"></textarea>
  <button id="saveNote" class="savenote">&#43; Save note</button>
</div>

{PRACTICE}

{cards_html}

<footer>
  <h3>The 4 things to actually drill</h3>
  <ul>
    <li><b>Turns &amp; flourish (Bars 13–16, 0:26–0:35):</b> follow spots the head or a slow turn gets dizzy; lead’s raised hand stays still.</li>
    <li><b>The reach / open line (Bars 31–32, 1:05):</b> a shape, not a step — commit, hold a beat, reel in smoothly.</li>
    <li><b>Both lifts (Bars 53–55 · 1:52, and Bars 62–63 · 2:11):</b> soft surface first; lead lifts with legs, follow keeps her frame tight, agree a verbal down-cue.</li>
    <li><b>Floor travel (Bars 25–30, 0:52–1:05):</b> mark start &amp; end spots so you don’t drift off-camera.</li>
  </ul>
  <p style="margin-top:14px">Keep <b>index.html</b> with its <b>clips/</b> folder. Bar grid detected from the audio at 112 BPM (1 bar = 2.14 s). Progress stored per-browser.</p>
</footer>

<div class="stage" id="stage" hidden>
  <div class="stage-inner">
    <video id="stageVid" controls playsinline preload="auto">
      <source src="clips/full.mp4" type="video/mp4">
    </video>
    <span id="beatDot" class="beatdot"></span>
    <div class="stage-cap">
      <span id="stageBars"></span><span id="stageTitle"></span>
      <div id="stageLyric"></div>
    </div>
    <div class="stage-ctrls">
      <button id="sMetro" class="sctl">&#9835; Beat: off</button>
      <span class="mnudge" title="Nudge the beat earlier / later until it locks onto the music">
        <button id="sMinus" type="button">&minus;</button><span id="sOff">+0ms</span><button id="sPlus" type="button">+</button>
      </span>
    </div>
    <button class="stage-close" id="stageClose">&times; Close</button>
  </div>
</div>

{secmenu_html}

<div class="playbar" id="playbar">
  <button class="primary" id="playSel">&#9654; Play queued (<span id="qcount">0</span>)</button>
  <button class="ghost" id="playAll">&#9654;&#9654; Play all</button>
  <button class="ghost" id="replay">&#8635; Replay</button>
  <label>Speed
    <select id="speed">
      <option value="1">1&times;</option>
      <option value="0.75">0.75&times;</option>
      <option value="0.5">0.5&times;</option>
      <option value="0.35">0.35&times;</option>
    </select>
  </label>
  <label><input type="checkbox" id="loopQueue"> Loop</label>
  <label><input type="checkbox" id="metro"> &#9835; Beat</label>
  <span class="mnudge" title="Nudge the clicks earlier / later to lock onto the music">
    <button id="mMinus" type="button">&minus;</button><span id="mOff">+0ms</span><button id="mPlus" type="button">+</button>
  </span>
  <button class="ghost" id="stopPlay">&#9632; Stop</button>
  <span id="nowplaying"></span>
</div>
</div>

<script>
(function(){{
  // ---- passkey gate (client-side; light protection for a personal link) ----
  var GKEY='ordUnlocked', PASS='{PASS_B64}';
  var gate=document.getElementById('gate');
  function unlock(){{gate.hidden=true;document.body.style.overflow='';}}
  try{{ if(localStorage.getItem(GKEY)==='1') unlock(); }}catch(e){{}}
  if(!gate.hidden) document.body.style.overflow='hidden';
  function tryPass(){{
    var v=document.getElementById('gatePass').value||'';
    var ok=false; try{{ok=(btoa(unescape(encodeURIComponent(v)))===PASS);}}catch(e){{ok=false;}}
    if(ok){{ try{{localStorage.setItem(GKEY,'1')}}catch(e){{}} unlock(); }}
    else {{ document.getElementById('gateErr').textContent='Wrong passkey — try again.'; }}
  }}
  document.getElementById('gateBtn').addEventListener('click',tryPass);
  document.getElementById('gatePass').addEventListener('keydown',function(e){{ if(e.key==='Enter')tryPass(); }});

  var KEY='ordinaryFirstDanceProgress2',store={{}};
  try{{store=JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{store={{}}}}
  var boxes=Array.prototype.slice.call(document.querySelectorAll('.chk'));
  var total=boxes.length,countEl=document.getElementById('count'),
      fillEl=document.getElementById('fill'),pctEl=document.getElementById('pct');
  function refresh(){{
    var done=0;
    boxes.forEach(function(b){{
      var on=!!store[b.dataset.id];
      b.checked=on;
      b.closest('.card').classList.toggle('done',on);
      if(on)done++;
    }});
    var pct=total?Math.round(done/total*100):0;
    countEl.textContent=done+' / '+total;
    pctEl.textContent=pct+'%';
    fillEl.style.width=pct+'%';
  }}
  boxes.forEach(function(b){{
    b.addEventListener('change',function(){{
      if(b.checked)store[b.dataset.id]=1;else delete store[b.dataset.id];
      try{{localStorage.setItem(KEY,JSON.stringify(store))}}catch(e){{}}
      refresh();
    }});
  }});
  document.getElementById('reset').addEventListener('click',function(){{
    if(!confirm('Reset the Got-it checkboxes? (Your written notes are kept.)'))return;
    store={{}};try{{localStorage.removeItem(KEY)}}catch(e){{}}refresh();
  }});
  // ---- notes (autosave, timestamped) + export/import ----
  var NKEY='ordinaryFirstDanceNotes', CKEY='ordinaryFirstDanceCardNotes';
  function fmt(ms){{ if(!ms)return''; try{{return new Date(ms).toLocaleString([],{{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}});}}catch(e){{return'';}} }}
  var gn=document.getElementById('globalnotes'), gsave=document.getElementById('gnsave'), gt;
  var LOGKEY='ordNotesLog', noteslog=[];
  try{{ noteslog=JSON.parse(localStorage.getItem(LOGKEY))||[]; }}catch(e){{ noteslog=[]; }}
  // migrate a previously autosaved single note into the log
  try{{ var _old=localStorage.getItem(NKEY);
    if(_old&&!noteslog.length){{ var _p; try{{_p=JSON.parse(_old);}}catch(e){{_p={{t:_old,ts:0}};}}
      if(_p&&_p.t)noteslog.push({{t:_p.t,ts:_p.ts||0}}); }} }}catch(e){{}}
  function saveLog(){{ try{{localStorage.setItem(LOGKEY,JSON.stringify(noteslog));}}catch(e){{}} }}
  function renderLog(){{
    var el=document.getElementById('noteslog'); if(!el)return; el.innerHTML='';
    noteslog.forEach(function(n,idx){{
      var d=document.createElement('div'); d.className='logitem';
      var meta=document.createElement('div'); meta.className='logmeta';
      var t=document.createElement('span'); t.textContent=n.ts?fmt(n.ts):''; meta.appendChild(t);
      var del=document.createElement('button'); del.className='logdel'; del.textContent='\\u00d7'; del.title='Delete note';
      del.addEventListener('click',function(){{ noteslog.splice(idx,1); saveLog(); renderLog(); }});
      meta.appendChild(del);
      var tx=document.createElement('div'); tx.className='logtext'; tx.textContent=n.t;
      d.appendChild(meta); d.appendChild(tx); el.appendChild(d);
    }});
  }}
  renderLog();
  function flashG(){{gsave.textContent='saved';gsave.classList.add('show');clearTimeout(gt);gt=setTimeout(function(){{gsave.classList.remove('show');}},1400);}}
  function doSaveNote(){{ var v=(gn.value||'').trim(); if(!v)return; noteslog.push({{t:v,ts:Date.now()}}); saveLog(); renderLog(); gn.value=''; flashG(); }}
  var snBtn=document.getElementById('saveNote'); if(snBtn)snBtn.addEventListener('click',doSaveNote);
  gn.addEventListener('keydown',function(e){{ if((e.metaKey||e.ctrlKey)&&e.key==='Enter'){{e.preventDefault();doSaveNote();}} }});
  var cstore={{}};
  try{{ var craw=localStorage.getItem(CKEY); if(craw)cstore=JSON.parse(craw)||{{}}; }}catch(e){{cstore={{}}}}
  Array.prototype.slice.call(document.querySelectorAll('.cardnote')).forEach(function(ta){{
    var id=ta.dataset.id, rec=cstore[id];
    if(typeof rec==='string')rec={{t:rec,ts:0}};
    var st=document.querySelector('.cardstamp[data-id="'+id+'"]');
    if(rec&&rec.t){{ ta.value=rec.t; if(st)st.textContent='saved '+fmt(rec.ts); }}
    ta.addEventListener('input',function(){{
      if(ta.value.trim()){{cstore[id]={{t:ta.value,ts:Date.now()}};}} else {{delete cstore[id];}}
      try{{localStorage.setItem(CKEY,JSON.stringify(cstore))}}catch(e){{}}
      if(st)st.textContent=cstore[id]?('saved '+fmt(cstore[id].ts)):'';
    }});
  }});
  function download(name,text,type){{
    var b=new Blob([text],{{type:type||'text/plain'}}), u=URL.createObjectURL(b);
    var a=document.createElement('a'); a.href=u; a.download=name; document.body.appendChild(a); a.click();
    setTimeout(function(){{document.body.removeChild(a);URL.revokeObjectURL(u);}},120);
  }}
  function datestamp(){{ var d=new Date(); return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); }}
  document.getElementById('expJson').addEventListener('click',function(){{
    var prog={{}}; try{{prog=JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{}}
    download('ordinary-notes-'+datestamp()+'.json',
      JSON.stringify({{app:'ordinary-first-dance',version:3,exportedAt:new Date().toISOString(),notes:noteslog,cards:cstore,progress:prog}},null,2),
      'application/json');
  }});
  document.getElementById('expMd').addEventListener('click',function(){{
    var prog={{}}; try{{prog=JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{}}
    var L=['# Ordinary — First Dance · notes','','_Exported '+new Date().toLocaleString()+'_',''];
    if(noteslog.length){{ L.push('## Notes',''); noteslog.forEach(function(n){{L.push('- '+n.t+(n.ts?'  _('+fmt(n.ts)+')_':''));}}); L.push(''); }}
    L.push('## Per-phrase notes','');
    SEGS.forEach(function(s){{ var r=cstore[s.id]; if(r&&r.t){{
      L.push('### '+s.id+' · Bars '+s.bars+' · '+s.title+(prog[s.id]?' ✓':''));
      L.push(r.t); if(r.ts)L.push('_saved '+fmt(r.ts)+'_'); L.push('');
    }} }});
    var done=SEGS.filter(function(s){{return prog[s.id];}});
    L.push('## Learned ('+done.length+'/'+SEGS.length+')');
    L.push(done.length?done.map(function(s){{return '- '+s.id+' '+s.title;}}).join('\\n'):'- (none yet)');
    download('ordinary-notes-'+datestamp()+'.md',L.join('\\n'),'text/markdown');
  }});
  document.getElementById('impFile').addEventListener('change',function(e){{
    var f=e.target.files[0]; if(!f)return; var r=new FileReader();
    r.onload=function(){{ try{{ var d=JSON.parse(r.result);
      if(d.notes)localStorage.setItem(LOGKEY,JSON.stringify(d.notes));
      else if(d.global&&d.global.t)localStorage.setItem(LOGKEY,JSON.stringify([d.global]));
      if(d.cards)localStorage.setItem(CKEY,JSON.stringify(d.cards));
      if(d.progress)localStorage.setItem(KEY,JSON.stringify(d.progress));
      alert('Notes loaded — reloading.'); location.reload();
    }}catch(err){{alert('Could not read that file: '+err);}} }};
    r.readAsText(f);
  }});
  // ---- speed + queue selection ----
  var pqs=Array.prototype.slice.call(document.querySelectorAll('.pq'));
  var allVids=Array.prototype.slice.call(document.querySelectorAll('.card video'));
  var qcount=document.getElementById('qcount');
  var loopQ=false, rate=1, lastId=null;
  document.getElementById('loopQueue').addEventListener('change',function(e){{loopQ=e.target.checked;}});
  document.getElementById('speed').addEventListener('change',function(e){{
    rate=parseFloat(e.target.value)||1;
    allVids.forEach(function(v){{v.playbackRate=rate;}});
    if(sv)sv.playbackRate=rate;
  }});
  function updateCount(){{qcount.textContent=pqs.filter(function(c){{return c.checked;}}).length;}}
  pqs.forEach(function(c){{c.addEventListener('change',function(){{
    c.closest('.card').classList.toggle('queued',c.checked);updateCount();refreshSecMenu();
  }});}});
  // ---- section quick-queue menu ----
  var secToggles=Array.prototype.slice.call(document.querySelectorAll('.secToggle'));
  function pqsFor(sec){{ return pqs.filter(function(c){{return c.dataset.section===sec;}}); }}
  function setPq(c,val){{ if(c.checked!==val){{ c.checked=val; c.dispatchEvent(new Event('change')); }} }}
  function refreshSecMenu(){{
    secToggles.forEach(function(b){{
      var g=pqsFor(b.dataset.section);
      var on=g.length&&g.every(function(c){{return c.checked;}});
      var some=g.some(function(c){{return c.checked;}});
      b.classList.toggle('on',on); b.classList.toggle('some',some&&!on);
    }});
  }}
  secToggles.forEach(function(b){{ b.addEventListener('click',function(){{
    var g=pqsFor(b.dataset.section);
    var allOn=g.length&&g.every(function(c){{return c.checked;}});
    g.forEach(function(c){{ setPq(c,!allOn); }}); refreshSecMenu();
  }}); }});
  var cq=document.getElementById('clearQueue');
  if(cq)cq.addEventListener('click',function(){{ pqs.forEach(function(c){{ setPq(c,false); }}); refreshSecMenu(); }});
  allVids.forEach(function(v){{v.addEventListener('play',function(){{
    v.playbackRate=rate; lastId=v.closest('.card').dataset.id;
  }});}});

  // ---- seamless stage: play time-ranges of ONE continuous file (no element swaps) ----
  var SEGS={seg_json};
  var segById={{}}; SEGS.forEach(function(s){{segById[s.id]=s;}});
  var stage=document.getElementById('stage'), sv=document.getElementById('stageVid');
  var sBars=document.getElementById('stageBars'), sTitle=document.getElementById('stageTitle'), sLyric=document.getElementById('stageLyric');
  var ranges=[], ri=0, stagePlaying=false;
  function highlightCard(id){{
    allVids.forEach(function(v){{v.closest('.card').classList.remove('playing');}});
    var c=document.querySelector('.card[data-id="'+id+'"]'); if(c)c.classList.add('playing');
  }}
  function showCap(r){{
    sBars.textContent='Bars '+r.bars; sTitle.textContent=r.title;
    var inst=/^\\s*\\(/.test(r.lyric);
    sLyric.textContent=inst?r.lyric.replace(/[()]/g,''):('\\u201C'+r.lyric+'\\u201D');
    highlightCard(r.id);
  }}
  function startRange(i){{
    ri=i; var r=ranges[i]; showCap(r);
    try{{sv.currentTime=r.start;}}catch(e){{}}
    sv.playbackRate=rate;
    var p=sv.play(); if(p&&p.catch)p.catch(function(){{}});
  }}
  sv.addEventListener('timeupdate',function(){{
    if(!stagePlaying||ri>=ranges.length)return;
    var r=ranges[ri];
    if(sv.currentTime>=r.end-0.04){{
      var n=ri+1;
      if(n<ranges.length){{
        var nr=ranges[n];
        if(Math.abs(nr.start-r.end)<0.06){{ ri=n; showCap(nr); }}   // contiguous -> keep rolling, zero gap
        else {{ startRange(n); }}                                   // non-adjacent -> one fast keyframe seek
      }} else if(loopQ){{ startRange(0); }}
      else {{ closeStage(); }}
    }}
  }});
  function openStage(ids){{
    var rs=ids.map(function(id){{return segById[id];}}).filter(Boolean);
    if(!rs.length)return;
    ranges=rs; stagePlaying=true; stage.hidden=false; document.body.style.overflow='hidden';
    var go=function(){{startRange(0);}};
    if(sv.readyState>=1)go(); else sv.addEventListener('loadedmetadata',go,{{once:true}});
  }}
  function closeStage(){{
    stagePlaying=false; try{{sv.pause();}}catch(e){{}} stage.hidden=true; document.body.style.overflow='';
    allVids.forEach(function(v){{v.closest('.card').classList.remove('playing');}});
  }}
  document.getElementById('playSel').addEventListener('click',function(){{
    openStage(pqs.filter(function(c){{return c.checked;}}).map(function(c){{return c.dataset.id;}}));
  }});
  document.getElementById('playAll').addEventListener('click',function(){{ openStage(SEGS.map(function(s){{return s.id;}})); }});
  document.getElementById('replay').addEventListener('click',function(){{ openStage([lastId||SEGS[0].id]); }});
  function stopEverything(){{ closeStage(); allVids.forEach(function(v){{ try{{v.pause();}}catch(e){{}} }}); }}
  document.getElementById('stopPlay').addEventListener('click',stopEverything);
  document.getElementById('stageClose').addEventListener('click',closeStage);
  stage.addEventListener('click',function(e){{ if(e.target===stage)closeStage(); }});
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape'&&!stage.hidden)closeStage(); }});

  // ---- beat metronome at HALF tempo (~56 BPM), phase-locked to the music ----
  var BPM=112.34, BEAT=60/(BPM/2), T0=0.549, BEAT0=T0-Math.floor(T0/BEAT)*BEAT;
  var acx=null, metroOn=false, nextBeat=0, metroTimer=null, mOffset=0, LAT=-0.22;
  var beatDot=document.getElementById('beatDot');
  try{{ var _mv=localStorage.getItem('ordMetroOffset2'); if(_mv!==null&&_mv!=='')mOffset=parseFloat(_mv); }}catch(e){{}}
  if(isNaN(mOffset))mOffset=0;
  var mOffEl=document.getElementById('mOff'), sOffEl=document.getElementById('sOff');
  function showOff(){{ var s=(mOffset>=0?'+':'')+Math.round(mOffset*1000)+'ms'; if(mOffEl)mOffEl.textContent=s; if(sOffEl)sOffEl.textContent=s; }}
  showOff();
  function ensureAudio(){{
    if(!acx){{ try{{acx=new (window.AudioContext||window.webkitAudioContext)();}}catch(e){{acx=null;}} }}
    if(acx&&acx.state==='suspended')acx.resume();
  }}
  function beatTime(i){{ return BEAT0+i*BEAT; }}
  function isDown(i){{ return ((((i)%2)+2)%2)===0; }}
  function pulse(down){{
    if(!beatDot)return;
    beatDot.classList.remove('hit','down'); void beatDot.offsetWidth;
    beatDot.classList.add('hit'); if(down)beatDot.classList.add('down');
  }}
  function tick(when,down){{
    var o=acx.createOscillator(), g=acx.createGain();
    o.type='square'; o.frequency.value=down?1760:1100;
    o.connect(g); g.connect(acx.destination);
    g.gain.setValueAtTime(0.0001,when);
    g.gain.exponentialRampToValueAtTime(down?0.6:0.34,when+0.001);
    g.gain.exponentialRampToValueAtTime(0.0001,when+0.06);
    o.start(when); o.stop(when+0.07);
    setTimeout(function(){{pulse(down);}}, Math.max(0,(when-acx.currentTime)*1000));
  }}
  function metroSched(){{
    if(!metroOn||!acx||!stagePlaying||sv.paused)return;
    var ct=sv.currentTime, rate=sv.playbackRate||1, la=0.15;
    if(beatTime(nextBeat)<ct-0.25||beatTime(nextBeat)>ct+2){{ nextBeat=Math.ceil((ct-BEAT0)/BEAT); }}
    while(beatTime(nextBeat)<=ct+la){{
      var when=acx.currentTime+Math.max(0,(beatTime(nextBeat)-ct)/rate+LAT+mOffset);
      tick(when,isDown(nextBeat)); nextBeat++;
    }}
  }}
  var metroChk=document.getElementById('metro'), sMetro=document.getElementById('sMetro');
  function setMetro(on){{
    metroOn=on;
    if(metroChk)metroChk.checked=on;
    if(sMetro){{ sMetro.textContent='\\u266A Beat: '+(on?'on':'off'); sMetro.classList.toggle('on',on); }}
    if(on){{ ensureAudio();
      var ct=(sv&&sv.currentTime)||0; nextBeat=Math.ceil((ct-BEAT0)/BEAT);
      if(!metroTimer)metroTimer=setInterval(metroSched,25);
    }} else if(metroTimer){{ clearInterval(metroTimer); metroTimer=null; }}
  }}
  if(metroChk)metroChk.addEventListener('change',function(e){{ setMetro(e.target.checked); }});
  if(sMetro)sMetro.addEventListener('click',function(){{ setMetro(!metroOn); }});
  function nudge(d){{ mOffset=Math.max(-0.6,Math.min(0.6,mOffset+d)); try{{localStorage.setItem('ordMetroOffset2',mOffset);}}catch(e){{}} showOff(); }}
  [['mPlus',0.02],['mMinus',-0.02],['sPlus',0.02],['sMinus',-0.02]].forEach(function(p){{
    var el=document.getElementById(p[0]); if(el)el.addEventListener('click',function(){{nudge(p[1]);}});
  }});
  updateCount(); refreshSecMenu();
  refresh();
}})();
</script>
</body></html>'''

os.makedirs(os.path.join(DEST, "clips"), exist_ok=True)
open(os.path.join(DEST, "index.html"), "w").write(HTML)
print(f"wrote {os.path.join(DEST,'index.html')}  ({len(HTML)//1024} KB)  segments={N}")

"""Build 'Mikan in a URL' — a ≤3072-byte data-URI cat app.

The app: Mikan walks on a tiny stage; click to pet her (hearts + blush).
Everything inline, procedural pixel art via canvas.
"""
from pathlib import Path
import urllib.parse

OUT = Path(__file__).parent
APP = r'''<!doctype html><html><head><meta charset=utf-8><title>Mikan in a URL</title><style>html,body{margin:0;height:100%;overflow:hidden;background:#141620}canvas{display:block}i{position:fixed;left:50%;bottom:6px;transform:translateX(-50%);color:#8b93a8;font:13px system-ui}</style></head><body><canvas id=c></canvas><i>click Mikan = pet her 🧡</i><script>
X=c.getContext('2d');W=c.width=innerWidth;H=c.height=innerHeight;t=0;x=W/2;d=1;s=0;h=[];p=0;
onclick=e=>{var r=c.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
if(Math.abs(mx-x)<70&&my>H-190){p=90;for(var i=0;i<7;i++)h.push({x:x+Math.random()*40-20,y:H-150,v:-2-Math.random()*2,a:1})}}
function R(a,b,c,d,e,f){X.fillStyle=f;X.fillRect(a,b,c,d);X.fillStyle=e}
function cat(px,py,f){
X.save();X.translate(px,py);X.scale(f,1);var O='#f7a354',D='#de7c3c',C='#ffe7c4',K='#3d2b26',P='#f7a8a8';
R(-16,-30,32,64,C,O);R(-22,-42,44,38,O,O);              // head+body base
R(-26,-46,12,10,O,O);R(14,-46,12,10,O,O);               // ears
R(-24,-44,8,6,P,P);R(16,-44,8,6,P,P);                   // inner ears
R(-10,-22,7,6,K,K);R(3,-22,7,6,K,K);                    // eyes
R(-2,-14,4,3,P,P);R(-8,-8,16,8,C,C);                    // nose+muzzle
R(-14,-50,4,6,D,D);R(2,-50,4,6,D,D);                    // head stripes
R(-14,34,10,10,O,O);R(4,34,10,10,O,O);                  // legs
X.beginPath();X.moveTo(20,-6);X.quadraticCurveTo(40,-14,34,-36);X.lineWidth=8;X.strokeStyle=O;X.stroke();
X.restore()}
function loop(){
t++;X.fillStyle='#141620';X.fillRect(0,0,W,H);
var gy=H-70;
for(var i=0;i<40;i++){X.fillStyle='rgba(255,255,255,.05)';X.fillRect((i*97+t*.5)%W,gy+20+(i*37)%40,2,2)}
// floor
X.fillStyle='#1d2233';X.fillRect(0,gy+60,W,H);
if(p>0){p--}else{if(s>0){s--}else{x+=d*1.6;if(x>W-60){d=-1}s=30;if(x<60){d=1}}}
var wig=Math.sin(t/8)*2;
cat(x,gy+(p>0?4:0)+wig,d);
if(p>0){X.fillStyle='rgba(247,168,168,.35)';X.beginPath();X.arc(x-26,gy-26,6,0,7);X.arc(x+30,gy-26,6,0,7);X.fill()}
if(t%60<30&&p<=0&&s<=0){X.fillStyle='#8b93a8';X.font='14px monospace';X.fillText('z',x+34,gy-70)}
h=h.filter(v=>v.a>0);h.forEach(v=>{v.y+=v.v;v.v+=.06;v.a-=.015;X.fillStyle='rgba(247,120,120,'+v.a+')';X.font='20px serif';X.fillText('♥',v.x,v.y)});
if(t%300<150){X.fillStyle='#8b93a8';X.font='12px monospace';X.fillText('mrrp!',x-18,gy-110)}
requestAnimationFrame(loop)}loop();
</script></body></html>'''

# encode as a data URI: minimal escaping (keep chars that are safe in data: URIs)
enc = urllib.parse.quote(APP, safe="=%:/#?,;()[]{}$+-@!*'~._")
data_uri = "data:text/html;charset=utf-8," + enc
size_app = len(APP.encode('utf-8'))
size_uri = len(data_uri.encode('utf-8'))
print(f"app bytes: {size_app}")
print(f"data-URI bytes: {size_uri} / 3072")
(OUT / 'mikan_app.html').write_text(APP, encoding='utf-8')
(OUT / 'mikan_uri.txt').write_text(data_uri, encoding='utf-8')
print("saved mikan_app.html + mikan_uri.txt")

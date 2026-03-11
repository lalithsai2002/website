#!/usr/bin/env python3
"""
💌 Sorry Website — One-file Python server + QR generator
────────────────────────────────────────────────────────
Folder structure:
  sorry.py          ← this file
  src/
    photo1.jpeg
    photo2.jpeg
    ...
    photo10.jpeg

Run:   python sorry.py
Open:  http://localhost:8080
"""

import http.server
import socketserver
import threading
import webbrowser
import os
import sys
import mimetypes

PORT = int(os.environ.get("PORT", 8080))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR    = os.path.join(SCRIPT_DIR, "src")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I'm Sorry 💕</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,500;1,300;1,400&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
<style>
:root{--rose:#e8536a;--rose2:#c0395a;--blush:#f9c6ce;--cream:#fff8f0;--gold:#c9a96e;--gold2:#e8c98a;--deep:#2a1520;--wine:#7b1f3a;}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--cream);font-family:'Cormorant Garamond',serif;color:var(--deep);overflow-x:hidden;cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Ctext y='26' font-size='26'%3E🌸%3C/text%3E%3C/svg%3E") 16 16,auto;}
body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:.4;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");}
.petals-bg{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden;}
.petal{position:absolute;animation:fall linear infinite;}
@keyframes fall{0%{transform:translateY(-80px) rotate(0deg) scale(1);opacity:0}8%{opacity:.55}92%{opacity:.4}100%{transform:translateY(115vh) rotate(900deg) scale(.6);opacity:0}}
.stars-bg{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden;}
.star{position:absolute;border-radius:50%;background:var(--gold2);animation:twinkle ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:0;transform:scale(.3)}50%{opacity:.65;transform:scale(1)}}
/* HERO */
.hero{position:relative;z-index:2;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2rem;overflow:hidden;background:radial-gradient(ellipse at 50% -10%,#fce4ec 0%,#ffe8f0 35%,var(--cream) 75%);}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 20% 80%,rgba(232,83,106,.09),transparent 55%),radial-gradient(circle at 80% 20%,rgba(201,169,110,.07),transparent 50%);}
.hero::after{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(42,21,32,.18) 100%);}
.hero-inner{position:relative;z-index:2;}
.envelope{font-size:7rem;margin-bottom:1.5rem;animation:envelopePulse 3s ease-in-out infinite;filter:drop-shadow(0 12px 32px rgba(232,83,106,.4));display:inline-block;}
@keyframes envelopePulse{0%,100%{transform:scale(1) rotate(-3deg) translateY(0)}50%{transform:scale(1.1) rotate(3deg) translateY(-8px)}}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(3.2rem,9vw,7rem);font-weight:700;color:var(--rose);line-height:1.08;animation:fadeSlideUp 1.1s ease both;text-shadow:0 4px 20px rgba(232,83,106,.25),0 0 60px rgba(232,83,106,.1);letter-spacing:-.02em;}
.hero h1 em{font-style:italic;color:var(--gold);}
.hero-sub{font-family:'Dancing Script',cursive;font-size:clamp(1.4rem,3.5vw,2.2rem);color:#b36078;margin-top:1.2rem;animation:fadeSlideUp 1.1s .25s ease both;opacity:0;text-shadow:0 2px 8px rgba(232,83,106,.15);}
.hero-hearts{margin-top:1.8rem;font-size:2rem;letter-spacing:.6rem;animation:fadeSlideUp 1.1s .45s ease both;opacity:0;}
.scroll-hint{margin-top:2.5rem;font-size:2.2rem;color:var(--rose);animation:bounce 2.2s ease-in-out infinite,fadeSlideUp 1s .65s ease both;opacity:0;}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(12px)}}
@keyframes fadeSlideUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:translateY(0)}}
section{position:relative;z-index:2;padding:6rem 2rem;}
.divider{text-align:center;font-size:1.6rem;letter-spacing:1rem;color:var(--rose);opacity:.5;padding:0 2rem 1rem;position:relative;z-index:2;}
/* LETTER */
.apology-section{background:linear-gradient(160deg,#fff0f6 0%,#fff5ef 60%,var(--cream) 100%);text-align:center;}
.letter-wrap{max-width:720px;margin:0 auto;position:relative;}
.letter-wrap::before,.letter-wrap::after{content:'🌹';position:absolute;font-size:2.5rem;opacity:.35;animation:roseSway 4s ease-in-out infinite;}
.letter-wrap::before{top:-1.5rem;left:-1rem;}
.letter-wrap::after{bottom:-1.5rem;right:-1rem;animation-delay:2s;}
@keyframes roseSway{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
.letter-card{background:linear-gradient(145deg,#fffaf8,#fff6f0);border-radius:3px;padding:4rem 3.5rem;box-shadow:0 2px 0 var(--gold),0 4px 0 rgba(201,169,110,.3),0 12px 60px rgba(232,83,106,.13),0 2px 12px rgba(0,0,0,.06),inset 0 1px 0 rgba(255,255,255,.9);border-top:4px solid var(--rose);position:relative;}
.letter-card::before{content:'❝';position:absolute;top:-1.8rem;left:50%;transform:translateX(-50%);font-size:3.5rem;color:var(--rose);background:linear-gradient(145deg,#fffaf8,#fff6f0);padding:0 .6rem;line-height:1;font-family:'Playfair Display',serif;}
.letter-card::after{content:'';position:absolute;inset:4rem 3.5rem;background:repeating-linear-gradient(transparent,transparent 39px,rgba(232,83,106,.07) 39px,rgba(232,83,106,.07) 40px);pointer-events:none;}
.letter-card p{font-size:1.3rem;line-height:2.1;color:#5a3040;margin-bottom:1.3rem;position:relative;z-index:1;}
.letter-card p:first-child{font-family:'Dancing Script',cursive;font-size:1.6rem;color:var(--wine);}
.letter-card .signature{font-family:'Dancing Script',cursive;font-size:2.4rem;color:var(--rose);margin-top:2.2rem;position:relative;z-index:1;text-shadow:0 2px 8px rgba(232,83,106,.2);}
/* REASONS */
.reasons-section{background:var(--cream);}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5.5vw,4rem);text-align:center;color:var(--rose);margin-bottom:3.5rem;text-shadow:0 2px 12px rgba(232,83,106,.15);}
.section-title span{color:var(--gold);font-style:italic;}
.section-title small{display:block;font-family:'Cormorant Garamond',serif;font-size:.45em;font-style:italic;color:#b36078;font-weight:400;margin-top:.4rem;letter-spacing:.05em;}
.reasons-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1.8rem;max-width:1060px;margin:0 auto;}
.reason-card{background:linear-gradient(145deg,#fff,#fff8f5);padding:2.2rem 2rem;border-left:4px solid var(--blush);box-shadow:0 4px 24px rgba(232,83,106,.07),0 1px 4px rgba(0,0,0,.04);transition:transform .35s,box-shadow .35s,border-color .35s;position:relative;overflow:hidden;}
.reason-card::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 80% 20%,rgba(232,83,106,.06),transparent 65%);pointer-events:none;}
.reason-card:hover{transform:translateY(-8px) rotate(.3deg);box-shadow:0 20px 50px rgba(232,83,106,.18);border-color:var(--rose);}
.reason-card .icon{font-size:2.8rem;margin-bottom:1rem;display:block;}
.reason-card h3{font-family:'Playfair Display',serif;font-size:1.25rem;color:var(--rose);margin-bottom:.7rem;}
.reason-card p{font-size:1.05rem;color:#7a4a55;line-height:1.8;}
/* PHOTOS */
.photos-section{background:linear-gradient(180deg,#fff3f7 0%,#fce4ec 50%,#ffe8f5 100%);padding-bottom:7rem;}
.photos-section::before{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 40%,rgba(232,83,106,.05) 100%);}
.mosaic{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,200px);gap:14px;max-width:1040px;margin:0 auto;}
.mosaic .photo:nth-child(1){grid-column:span 2;grid-row:span 2;}
.mosaic .photo:nth-child(4){grid-column:span 2;}
.mosaic .photo:nth-child(7){grid-column:span 2;grid-row:span 2;}
.mosaic .photo:nth-child(10){grid-column:span 2;}
.photo{overflow:hidden;position:relative;box-shadow:0 8px 32px rgba(0,0,0,.12),0 2px 6px rgba(0,0,0,.08);transition:transform .45s cubic-bezier(.23,1,.32,1),box-shadow .45s;cursor:pointer;border-radius:1px;}
.photo::before{content:'';position:absolute;inset:0;z-index:1;border:2px solid rgba(255,255,255,.25);pointer-events:none;}
.photo:hover{transform:scale(1.04) rotate(.6deg);box-shadow:0 24px 64px rgba(232,83,106,.3),0 8px 20px rgba(0,0,0,.12);z-index:3;}
.photo img{width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.23,1,.32,1),filter .5s;filter:saturate(.85) brightness(1.02);}
.photo:hover img{transform:scale(1.1);filter:saturate(1.15) brightness(1.05);}
.photo::after{content:'';position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(to top,rgba(123,31,58,.72) 0%,rgba(123,31,58,.1) 45%,transparent 70%);opacity:0;transition:opacity .35s;}
.photo:hover::after{opacity:1;}
.photo-overlay{position:absolute;bottom:0;left:0;right:0;z-index:3;padding:1.2rem 1rem .9rem;display:flex;flex-direction:column;gap:.2rem;transform:translateY(8px);opacity:0;transition:opacity .35s,transform .35s;}
.photo:hover .photo-overlay{opacity:1;transform:translateY(0);}
.photo-overlay .caption{font-family:'Dancing Script',cursive;font-size:1.2rem;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.5);}
.photo-overlay .caption-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.85rem;color:rgba(255,255,255,.75);}
/* PROMISES */
.promise-section{background:linear-gradient(145deg,var(--wine) 0%,var(--rose) 60%,#f06a80 100%);color:#fff;text-align:center;position:relative;overflow:hidden;}
.promise-section::before{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 30% 50%,rgba(255,255,255,.06),transparent 60%),radial-gradient(ellipse at 70% 50%,rgba(255,255,255,.04),transparent 55%);}
.promise-section .section-title{color:#fff;}
.promise-section .section-title span{color:var(--blush);}
.promises{display:flex;flex-wrap:wrap;gap:1.3rem;justify-content:center;max-width:860px;margin:0 auto;position:relative;z-index:1;}
.promise-pill{background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.45);border-radius:999px;padding:.8rem 1.8rem;font-size:1.1rem;backdrop-filter:blur(6px);transition:background .3s,transform .3s,box-shadow .3s;box-shadow:0 4px 16px rgba(0,0,0,.1);}
.promise-pill:hover{background:rgba(255,255,255,.25);transform:scale(1.07) translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.15);}
/* CTA */
.cta-section{background:radial-gradient(ellipse at 50% 0%,#fce4ec,var(--cream) 65%);text-align:center;padding-bottom:7rem;}
.heart-big{font-size:7rem;display:block;margin-bottom:1.5rem;animation:heartbeat 1.5s ease-in-out infinite;filter:drop-shadow(0 10px 28px rgba(232,83,106,.5));}
@keyframes heartbeat{0%,100%{transform:scale(1)}14%{transform:scale(1.18)}28%{transform:scale(.97)}42%{transform:scale(1.12)}56%{transform:scale(1)}}
.cta-section h2{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5.5vw,4rem);color:var(--deep);margin-bottom:1rem;}
.cta-sub{font-family:'Dancing Script',cursive;font-size:clamp(1.4rem,3vw,2rem);color:#b36078;margin-bottom:2.8rem;}
.forgive-btn{display:inline-block;background:linear-gradient(135deg,var(--rose),var(--rose2));color:#fff;font-family:'Playfair Display',serif;font-size:1.4rem;font-style:italic;padding:1.1rem 3.5rem;border:none;border-radius:999px;cursor:pointer;box-shadow:0 8px 32px rgba(232,83,106,.45),0 2px 8px rgba(0,0,0,.1);transition:transform .3s,box-shadow .3s;position:relative;overflow:hidden;}
.forgive-btn::before{content:'';position:absolute;inset:0;border-radius:999px;background:linear-gradient(135deg,rgba(255,255,255,.2),transparent);}
.forgive-btn:hover{transform:translateY(-5px) scale(1.03);box-shadow:0 20px 56px rgba(232,83,106,.55);}
/* CONFETTI */
.confetti-container{position:fixed;inset:0;pointer-events:none;z-index:9999;}
.conf{position:absolute;border-radius:2px;animation:confFall 2.2s ease forwards;}
@keyframes confFall{0%{transform:translateY(0) rotate(0) scale(1);opacity:1}100%{transform:translateY(700px) rotate(900deg) scale(.4);opacity:0}}
footer{background:var(--deep);color:rgba(255,255,255,.45);text-align:center;padding:2.5rem 2rem;font-size:1rem;position:relative;z-index:2;border-top:1px solid rgba(232,83,106,.2);}
footer span{color:var(--rose);}
footer .footer-hearts{display:block;font-size:1.5rem;margin-bottom:.4rem;letter-spacing:.5rem;}
.reveal{opacity:0;transform:translateY(44px);transition:opacity .8s ease,transform .8s ease;}
.reveal.visible{opacity:1;transform:none;}
@media(max-width:700px){
  .mosaic{grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(6,150px);}
  .mosaic .photo:nth-child(1){grid-column:span 2;grid-row:span 1;}
  .mosaic .photo:nth-child(4){grid-column:span 1;}
  .mosaic .photo:nth-child(7){grid-column:span 2;grid-row:span 1;}
  .mosaic .photo:nth-child(10){grid-column:span 1;}
  .letter-card{padding:2.2rem 1.5rem;}
  .letter-card::after{inset:2.2rem 1.5rem;}
}
</style>
</head>
<body>

<div class="petals-bg" id="petals"></div>
<div class="stars-bg" id="stars"></div>

<section class="hero">
  <div class="hero-inner">
    <div class="envelope">💌</div>
    <h1>I'm <em>So</em> Sorry,<br>My Love</h1>
    <p class="hero-sub">A letter straight from the bottom of my heart…</p>
    <div class="hero-hearts">🌹 💕 🌹</div>
    <div class="scroll-hint">↓</div>
  </div>
</section>

<div class="divider">❧ ✦ ❧</div>

<section class="apology-section">
  <div class="letter-wrap reveal">
    <div class="letter-card">
      <p>My dearest,</p>
      <p>I know I hurt you, and I am truly sorry for that. I don't have any excuses. I just want you to know that I care about you a lot, and it hurts me to know that my actions made you feel bad.</p>
      <p>You deserve someone who treats you well and is always there for you. I really want to be that person, and I promise I will try to become better.</p>
      <p>Every moment with you means a lot to me. You bring so much happiness into my life, and I would do anything to see your smile again.</p>
      <p>Will you please forgive me? 🌸</p>
      <div class="signature">Forever yours 💕</div>
    </div>
  </div>
</section>

<div class="divider">❧ ✦ ❧</div>

<section class="reasons-section">
  <h2 class="section-title reveal">Reasons I <span>Love</span> You<small>let me count the ways…</small></h2>
  <div class="reasons-grid">
    <div class="reason-card reveal"><span class="icon">😊</span><h3>Your Laugh</h3><p>Your laugh makes my whole day brighter. I love hearing it again and again.</p></div>
    <div class="reason-card reveal"><span class="icon">✨</span><h3>Your Kindness</h3><p>You are so kind and caring to everyone. That is one of the most beautiful things about you.</p></div>
    <div class="reason-card reveal"><span class="icon">💖</span><h3>Being With You</h3><p>Whenever I see you, I feel something magical. Just being near you makes everything feel special.</p></div>
    <div class="reason-card reveal"><span class="icon">🌍</span><h3>My Whole World</h3><p>You mean everything to me. In my heart, you are my whole world.</p></div>
    <div class="reason-card reveal"><span class="icon">❤️</span><h3>Your Heart</h3><p>Your loving heart is the most precious thing to me.</p></div>
    <div class="reason-card reveal"><span class="icon">💫</span><h3>Simply You and I</h3><p>With you, I never have to pretend. You know me exactly as I am and understand me completely. Just being with you means everything to me.</p></div>
  </div>
</section>

<div class="divider">❧ ✦ ❧</div>

<section class="photos-section">
  <h2 class="section-title reveal">Our <span>Favourite</span> Moments<small>ten memories I'll treasure forever</small></h2>
  <div class="mosaic reveal" id="mosaic"></div>
</section>

<div class="divider">❧ ✦ ❧</div>

<section class="promise-section">
  <h2 class="section-title reveal">My <span>Promises</span> to You<small>words I mean with all of my heart</small></h2>
  <div class="promises reveal">
    <div class="promise-pill">💬 I'll always listen</div>
    <div class="promise-pill">🤝 I'll communicate better</div>
    <div class="promise-pill">💖 I'll never take you for granted</div>
    <div class="promise-pill">🌿 I'll give you space when you need it</div>
    <div class="promise-pill">⭐ I'll choose you every single day</div>
    <div class="promise-pill">🕯️ I'll be patient and understanding</div>
    <div class="promise-pill">🏡 I'll always be your safe place</div>
  </div>
</section>

<section class="cta-section">
  <span class="heart-big">❤️</span>
  <h2 class="reveal">Can You Forgive Me?</h2>
  <p class="cta-sub reveal">I miss your smile… I miss us.</p>
  <button class="forgive-btn" id="forgiveBtn" onclick="celebrate()">Yes, I Forgive You 💕</button>
</section>

<div class="confetti-container" id="confetti"></div>

<footer>
  <span class="footer-hearts">🌹 💕 🌹</span>
  Made with <span>♥</span> just for you — because you deserve the whole world.
</footer>

<script>
// Petals
const pe=['🌸','🌷','🌺','💮','🏵️','💐','🌹','🌼'];
const pc=document.getElementById('petals');
for(let i=0;i<32;i++){const p=document.createElement('div');p.className='petal';p.textContent=pe[Math.floor(Math.random()*pe.length)];p.style.cssText=`left:${Math.random()*105-2}vw;animation-duration:${9+Math.random()*14}s;animation-delay:${Math.random()*15}s;font-size:${.7+Math.random()*1.4}rem`;pc.appendChild(p);}

// Stars
const sc=document.getElementById('stars');
for(let i=0;i<40;i++){const s=document.createElement('div');s.className='star';const sz=2+Math.random()*3;s.style.cssText=`left:${Math.random()*100}vw;top:${Math.random()*100}vh;width:${sz}px;height:${sz}px;animation-duration:${2+Math.random()*4}s;animation-delay:${Math.random()*5}s`;sc.appendChild(s);}

// Photos — your local images from src/
const captions=[
  {main:'Every moment with you',   sub:'my favourite memory ✨'},
  {main:'My favourite smile',      sub:'the one that undoes me 💕'},
  {main:'Where we belong',         sub:'together, always 🌸'},
  {main:'You & me',                sub:'my whole universe 🌹'},
  {main:'Magic in the ordinary',   sub:'you make it extraordinary 🦋'},
  {main:'Forever & ever',          sub:"that's my plan 💫"},
  {main:'My whole world',          sub:'right here 🌺'},
  {main:'The way you look at me',  sub:'I live for that 💌'},
  {main:'Us, always',              sub:'no matter what 🤍'},
  {main:'I choose you',            sub:'today, tomorrow, always 💕'},
];
const mosaic=document.getElementById('mosaic');
for(let i=1;i<=10;i++){
  const cap=captions[i-1];
  const d=document.createElement('div');
  d.className='photo';
  d.innerHTML=`<img src="/src/photo${i}.jpeg" alt="memory ${i}" loading="lazy" onerror="this.src='https://picsum.photos/seed/${i*7}/800/600'"><div class="photo-overlay"><span class="caption">${cap.main}</span><span class="caption-sub">${cap.sub}</span></div>`;
  mosaic.appendChild(d);
}

// Scroll reveal
const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));

// Confetti
function celebrate(){
  const colors=['#e8536a','#f9c6ce','#c9a96e','#fff','#fde8ec','#f06292','#c0395a','#e8c98a'];
  const conf=document.getElementById('confetti');
  conf.innerHTML='';
  for(let i=0;i<160;i++){const c=document.createElement('div');c.className='conf';const sz=6+Math.random()*10;c.style.cssText=`left:${Math.random()*100}vw;top:${Math.random()*35+25}vh;width:${sz}px;height:${sz}px;background:${colors[Math.floor(Math.random()*colors.length)]};animation-delay:${Math.random()*.9}s;transform:rotate(${Math.random()*360}deg);border-radius:${Math.random()>.5?'50%':'3px'}`;conf.appendChild(c);}
  for(let i=0;i<20;i++){const h=document.createElement('div');h.style.cssText=`position:fixed;font-size:${1.5+Math.random()*2}rem;left:${Math.random()*100}vw;top:${60+Math.random()*30}vh;animation:confFall ${1.5+Math.random()}s ease forwards;pointer-events:none;z-index:9999;animation-delay:${Math.random()*.5}s`;h.textContent=['💕','❤️','🌹','💖','💗'][Math.floor(Math.random()*5)];conf.appendChild(h);}
  const btn=document.getElementById('forgiveBtn');
  btn.textContent='💕 Thank You, My Love 💕';
  btn.style.background='linear-gradient(135deg,#c9a96e,#e8c98a)';
  setTimeout(()=>conf.innerHTML='',3000);
}
</script>
</body>
</html>"""


# ── Static file server for /src/ images ──────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            data = HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        elif self.path.startswith('/src/'):
            filename = os.path.basename(self.path)
            filepath = os.path.join(SRC_DIR, filename)
            if os.path.isfile(filepath):
                mime, _ = mimetypes.guess_type(filepath)
                mime = mime or 'application/octet-stream'
                with open(filepath, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


def generate_qr(url, filename="sorry_qr.png"):
    try:
        import qrcode
    except ImportError:
        print("  📦  Installing qrcode...")
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "qrcode[pil]"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        import qrcode

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    try:
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
        from qrcode.image.styles.colormasks import RadialGradiantColorMask
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(center_color=(232,83,106), edge_color=(201,169,110))
        )
    except Exception:
        img = qr.make_image(fill_color="#e8536a", back_color="white")

    out = os.path.join(SCRIPT_DIR, filename)
    img.save(out)
    return out


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.isdir(SRC_DIR):
        print(f"\n  ⚠️   'src/' folder not found next to sorry.py")
        print(f"       Create it and add photo1.jpeg … photo10.jpeg inside.")
        print(f"       (Missing images fall back to placeholder photos.)\n")
    else:
        found = sorted([f for f in os.listdir(SRC_DIR) if f.lower().endswith(('.jpeg','.jpg','.png'))])
        print(f"\n  🖼️   Found {len(found)} image(s) in src/: {', '.join(found[:6])}{'…' if len(found)>6 else ''}")

    ip    = get_local_ip()
    url   = f"http://{ip}:{PORT}"
    local = f"http://localhost:{PORT}"

    print()
    print("  💌  Sorry Website is LIVE!")
    print("  " + "─" * 46)
    print(f"  🌐  Local (you):   {local}")
    print(f"  📡  Network (her): {url}")
    print("  " + "─" * 46)
    print()
    print("  🎀  Generating QR code…")
    try:
        qr_path = generate_qr(url)
        print(f"  ✅  QR saved → {qr_path}")
        print("  📱  Send her the QR — she scans & sees your apology!")
    except Exception as e:
        print(f"  ⚠️   QR skipped ({e})")
        print(f"       She can visit: {url}")

    print()
    print("  Press  Ctrl+C  to stop.")
    print()

    threading.Timer(1.2, lambda: webbrowser.open(local)).start()

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:

            print("\n  💕  Server stopped. Good luck! 🌸\n")

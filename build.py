"""Builds the Kenny's leadership microsite: a homepage and one page per director.
Usage: python3 build.py [HOME_URL]
"""
import sys, pathlib, json
from PIL import Image

HOME_URL = sys.argv[1] if len(sys.argv) > 1 else "#"
OUT = pathlib.Path(__file__).parent / "site"
MAIN = "https://kennysinternational.com"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Jost:wght@300..600&display=swap">')

CSS = r"""
:root{
  /* Layout: gold-framed black opener, white content bands, black footer; the gold hairline is the one ornament */
  --ink:#000;--paper:#fff;--gold:#C9A55C;--gold-ink:#86671F;--gold-soft:rgba(201,165,92,.45);
  --mute:#BDBDBD;--mute-2:#8C8C8C;--body-ink:#3A3A3A;--line:#E8E8E8;--line-dk:#2B2B2B;
  --glass:rgba(18,18,18,.24);--shade:rgba(0,0,0,.5);--shade-2:rgba(0,0,0,.72);--photo:#EEE;--tile-dk:#0B0B0B;
  --f-body:"Jost","Futura","Century Gothic",sans-serif;
  --f-wide:"Syncopate","Michroma","Eurostile",sans-serif;
  --g:clamp(64px,6.4vw,120px);
  --ease:cubic-bezier(.2,.8,.1,1);
  color-scheme:light;
}
@media (max-width:600px){:root{--g:22px}}
*{box-sizing:border-box}
html{background:var(--ink)}
body{margin:0;background:var(--ink);color:var(--ink);font-family:var(--f-body);font-size:16px;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{display:block;max-width:100%}
[hidden]{display:none !important}
html:has(dialog[open]){overflow:hidden}
:focus-visible{outline:2px solid var(--gold);outline-offset:4px}
.wrap{width:100%;max-width:1680px;margin:0 auto;padding-left:max(var(--g),env(safe-area-inset-left,0px));padding-right:max(var(--g),env(safe-area-inset-right,0px))}
.wide{font-family:var(--f-wide);font-weight:400;text-transform:uppercase;letter-spacing:.04em}
.cap{font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:500}
.gold{color:var(--gold-ink)}
.dark{background:var(--ink);color:var(--paper)}
.dark .gold{color:var(--gold)}
.light{background:var(--paper);color:var(--ink)}
.h2{margin:0;font-size:clamp(26px,3vw,52px);line-height:1.12;text-wrap:balance}
.body{margin:0;max-width:34em;font-size:16px;line-height:1.8;font-weight:300}
.light .body{color:var(--body-ink)}
.dark .body{color:var(--mute)}
.band{padding-block:clamp(72px,8vw,130px)}

/* brand row (no menu) */
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:clamp(68px,9vh,96px)}
.brand{display:inline-flex;align-items:center;gap:12px;text-decoration:none;color:var(--paper)}
.brand img{width:30px;height:30px;filter:invert(1)}
.brand .cap{transition:color .35s}
a.brand:hover .cap{color:var(--gold)}
.top .tag{color:var(--mute-2)}

/* buttons and arrow links */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:18px;min-height:54px;padding:0 34px;border:1px solid var(--ink);background:transparent;color:var(--ink);text-decoration:none;font:inherit;font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;cursor:pointer;transition:background .35s,color .35s,border-color .35s}
.btn svg{transition:transform .5s var(--ease)}
.btn:hover svg{transform:translateX(6px)}
.btn.solid{background:var(--ink);color:var(--paper)}
.btn.solid:hover{background:var(--gold);border-color:var(--gold);color:var(--ink)}
.lnk{display:inline-flex;align-items:center;gap:18px;min-height:44px;text-decoration:none;font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;color:inherit;transition:color .35s}
.lnk svg{width:46px;transition:width .5s var(--ease)}
.lnk:hover{color:var(--gold-ink)}
.dark .lnk:hover{color:var(--gold)}
.lnk:hover svg{width:70px}
.vw{flex:none;width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);color:var(--gold-ink);transition:background .35s,border-color .35s,color .35s}

/* figures */
.stats{margin:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;max-width:520px}
.stats>div{display:flex;flex-direction:column;justify-content:flex-end}
.stats dt{color:var(--mute-2);font-size:10px;line-height:1.5}
.stats dd{margin:12px 0 0;font-size:clamp(20px,2vw,32px)}
.stats.words dd{font-size:clamp(12px,1.05vw,16px);line-height:1.45}

/* HOME hero */
.hero{background:var(--ink);color:var(--paper)}
.frame{position:relative;min-height:clamp(600px,84svh,920px);border:1px solid var(--gold);overflow:hidden;display:flex;flex-direction:column;isolation:isolate}
.hbg{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;object-position:50% 60%;z-index:-3;filter:brightness(.82);animation:settle 2.4s var(--ease) both}
.frame::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,var(--shade),transparent 45%);z-index:-2}
.glass{position:absolute;left:0;top:0;bottom:0;width:42%;background:var(--glass);-webkit-backdrop-filter:blur(16px) brightness(.72);backdrop-filter:blur(16px) brightness(.72);border-right:1px solid var(--gold);z-index:-1;animation:tin 1.2s var(--ease) both}
.frame .top{padding-left:max(7%,env(safe-area-inset-left,0px));padding-right:max(clamp(22px,3.4vw,56px),env(safe-area-inset-right,0px))}
.ttl{flex:1;display:flex;flex-direction:column;justify-content:center;margin:0;padding:24px 0 24px max(7%,env(safe-area-inset-left,0px));font-weight:500;font-size:clamp(44px,min(10.4vw,17vh),220px);line-height:.92;letter-spacing:-.035em;text-transform:lowercase;white-space:nowrap;animation:tin 1.2s .1s var(--ease) both}
.ttl span{display:block}
.ttl .l2{padding-left:15%}
.hinfo{width:42%;display:flex;flex-direction:column;gap:22px;padding:0 5% clamp(32px,5.5vh,60px) max(7%,env(safe-area-inset-left,0px));animation:fadeup 1s .35s var(--ease) both}
.hinfo .body{font-size:clamp(15px,1.1vw,17px);color:var(--paper);opacity:.86}
.hinfo .stats{padding-top:22px;border-top:1px solid var(--gold-soft)}
.hinfo .stats dt{color:var(--mute)}

/* HOME main-website section */
.web{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(40px,6vw,120px);align-items:center}
.web .txt{display:flex;flex-direction:column;gap:22px;align-items:flex-start;min-width:0}
.web .btn{margin-top:12px}
.webcard{display:block;text-decoration:none;color:inherit;min-width:0}
.webcard .ph{overflow:hidden;aspect-ratio:16/9;max-width:100%;background:var(--photo)}
.webcard .ph img{width:100%;height:100%;object-fit:cover;transition:transform 1.3s var(--ease)}
.webcard:hover .ph img{transform:scale(1.06)}
.webcard .bar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-block:18px;border-bottom:1px solid var(--line)}
.webcard .bar .wide{font-size:clamp(11px,1vw,14px);overflow-wrap:anywhere;transition:color .35s}
.webcard:hover .bar .wide{color:var(--gold-ink)}
.webcard:hover .vw{background:var(--gold);border-color:var(--gold);color:var(--ink)}

/* HOME social section */
.socband{padding-top:0}
.socband .inner{border-top:1px solid var(--line);padding-top:clamp(64px,7vw,110px)}
.head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:end;margin-bottom:clamp(40px,5vw,72px)}
.head>*{min-width:0}
.head>div>.cap{margin:0 0 18px}
.tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-left:1px solid var(--line)}
.stile{position:relative;display:flex;flex-direction:column;gap:12px;height:100%;min-height:clamp(160px,13vw,200px);padding:28px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink);background:var(--paper);transition:background .45s,color .45s}
.stile .ic{width:48px;height:48px;display:flex;align-items:center;justify-content:center;border:1px solid var(--line);color:var(--gold-ink);transition:border-color .45s,color .45s}
.stile .txt{margin-top:auto;display:flex;flex-direction:column;gap:8px}
.stile .nm{font-size:clamp(14px,1.3vw,20px)}
.stile .hd{font-size:14px;color:var(--mute-2);overflow-wrap:anywhere}
.stile .vw{position:absolute;top:16px;right:16px}
a.stile:hover{background:var(--ink);color:var(--paper)}
a.stile:hover .ic{border-color:var(--gold);color:var(--gold)}
a.stile:hover .vw{background:var(--gold);border-color:var(--gold);color:var(--ink)}

/* DIRECTOR hero */
.dhero{padding-block:0 clamp(56px,7vw,110px)}
.dgrid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(40px,6vw,120px);align-items:center;padding-top:clamp(12px,2.5vw,36px)}
.portrait{position:relative;margin:0;aspect-ratio:4/5;max-width:100%;max-height:72svh;overflow:hidden;border:1px solid var(--gold);display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:clamp(28px,3vw,44px) 20px;isolation:isolate;animation:tin 1.2s var(--ease) both}
.portrait .pbg{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;filter:blur(22px) brightness(.42);transform:scale(1.15);z-index:-2}
.portrait::after{content:"";position:absolute;inset:12px;border:1px solid var(--gold-soft);z-index:-1;pointer-events:none}
.portrait .em{width:34px;height:34px;filter:invert(1);opacity:.9}
.mono{font-family:var(--f-wide);font-size:clamp(60px,7.6vw,128px);line-height:1;letter-spacing:.06em;color:var(--gold);text-transform:uppercase}
.portrait figcaption{color:var(--mute)}
.dtxt{min-width:0;animation:fadeup 1s .25s var(--ease) both}
.dtxt .role{margin:0}
.name{margin:22px 0 0;font-weight:500;font-size:clamp(52px,7.4vw,140px);line-height:.92;letter-spacing:-.035em;text-transform:lowercase}
.name span{display:block}
.name .l2{padding-left:15%}
.dtxt .body{margin-top:34px}
.dtxt .stats{margin-top:40px;padding-top:24px;border-top:1px solid var(--line-dk)}

/* DIRECTOR focus */
.quote{margin:0;max-width:30em}
.quote p{margin:0;font-size:clamp(19px,1.6vw,26px);line-height:1.5;font-weight:300}
.quote cite{display:block;margin-top:18px;font-style:normal}
.focus{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(28px,3vw,56px)}
.focus li{border-top:1px solid var(--line);padding-top:28px;min-width:0}
.focus .dia{display:block;width:10px;height:10px;transform:rotate(45deg);background:var(--gold)}
.focus h3{margin:22px 0 0;font-size:clamp(13px,1.05vw,15px);line-height:1.5}
.focus p{margin:14px 0 0;font-size:15px;line-height:1.75;font-weight:300;color:var(--body-ink)}
.back{margin-top:clamp(40px,5vw,72px);display:flex;flex-wrap:wrap;gap:8px 40px}
.dark .btn{border-color:var(--gold);color:var(--paper)}
.dark .btn:hover{background:var(--gold);color:var(--ink)}

/* DIRECTOR gallery: masonry columns, grows with any number of photos */
.gal{border-bottom:1px solid var(--line-dk)}
.gal .count{display:block;margin-top:18px}
.masonry{list-style:none;margin:0;padding:0;columns:3 280px;column-gap:16px}
.masonry li{break-inside:avoid;margin:0 0 16px}
.gi{position:relative;display:block;overflow:hidden;background:var(--tile-dk);color:var(--paper);text-decoration:none}
.gi img{width:100%;height:auto;transition:transform 1.3s var(--ease)}
.gi::after{content:"";position:absolute;inset:0;border:1px solid transparent;transition:border-color .35s;pointer-events:none}
.gi:hover img,.gi:focus-visible img{transform:scale(1.05)}
.gi:hover::after,.gi:focus-visible::after{border-color:var(--gold)}
.gcap{position:absolute;left:0;right:0;bottom:0;padding:44px 18px 16px;background:linear-gradient(0deg,var(--shade-2),transparent);font-size:13px;line-height:1.4;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .5s var(--ease)}
.gi:hover .gcap,.gi:focus-visible .gcap{opacity:1;transform:none}
@media (hover:none){.gcap{opacity:1;transform:none}}
.gmore{display:flex;justify-content:center;margin-top:clamp(28px,3.5vw,48px)}
.gal .back{padding-top:32px;border-top:1px solid var(--line-dk)}

/* photo viewer */
.lb{position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;background:var(--ink);color:var(--paper);font-family:var(--f-body)}
.lb::backdrop{background:var(--ink)}
.lb[open]{display:grid;grid-template-rows:auto minmax(0,1fr) auto}
.lb-bar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-left:max(clamp(16px,3vw,48px),env(safe-area-inset-left,0px));padding-right:max(clamp(16px,3vw,48px),env(safe-area-inset-right,0px))}
.lb-bar.t{padding-block:calc(12px + env(safe-area-inset-top,0px)) 12px;border-bottom:1px solid var(--line-dk)}
.lb-bar.b{padding-block:16px calc(20px + env(safe-area-inset-bottom,0px))}
.lb-count{color:var(--gold);font-variant-numeric:tabular-nums}
.lb-x{display:inline-flex;align-items:center;gap:12px;min-height:44px;padding:0;background:none;border:0;color:var(--paper);font:inherit;font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:500;cursor:pointer;transition:color .3s}
.lb-x:hover{color:var(--gold)}
.lb-fig{margin:0;min-height:0;display:flex;align-items:center;justify-content:center;padding:clamp(12px,2vw,28px) clamp(12px,4vw,64px);touch-action:pan-y}
.lb-img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;opacity:0;transition:opacity .45s ease}
.lb-img.on{opacity:1}
.lb-cap{margin:0;min-width:0;font-size:14px;line-height:1.5;color:var(--mute)}
.lb-nav{display:flex;gap:14px;flex:none}
.arr{width:48px;height:48px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;transition:background .3s,color .3s}
.arr.p{background:transparent;border:1px solid var(--gold);color:var(--gold)}
.arr.n{background:var(--gold);border:1px solid var(--gold);color:var(--ink)}
.arr.p:hover{background:var(--gold);color:var(--ink)}
.arr.n:hover{background:transparent;color:var(--gold)}

/* footer (same as kennysinternational.com) */
.foot{padding-block:clamp(90px,9vw,150px) 36px}
.fgrid{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(3,minmax(0,1fr));gap:48px}
.fbrand{display:flex;align-items:center;gap:16px}
.fbrand img{width:48px;height:48px;filter:invert(1)}
.fbrand .wide{font-size:15px;line-height:1.5}
.ftag{margin:28px 0 0;font-size:15px}
.fh{margin:0 0 20px}
.flist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;font-size:15px;color:var(--mute)}
.flist a,.faddr a{text-decoration:none;transition:color .3s}
.flist a:hover,.faddr a:hover{color:var(--paper)}
.faddr{margin:0;font-size:15px;line-height:1.7;color:var(--mute)}
.faddr a{word-break:break-all}
.fbar{margin-top:80px;padding-top:26px;border-top:1px solid var(--line-dk);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--mute-2)}

/* motion */
@keyframes tin{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes fadeup{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes settle{from{transform:scale(1.08)}to{transform:none}}
@keyframes rise{from{transform:translateY(48px)}to{transform:none}}
@supports (animation-timeline: view()){
  .rise{animation:rise linear both;animation-timeline:view();animation-range:entry 0% entry 70%}
  .rise.r2{animation-range:entry 8% entry 78%}
  .rise.r3{animation-range:entry 16% entry 86%}
}

/* responsive */
@media (max-width:1100px){
  .fgrid{grid-template-columns:minmax(0,1fr)}
  .web,.head{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:900px){
  .glass{width:100%;border-right:0;background:rgba(18,18,18,.34)}
  .hinfo{width:auto;padding-right:max(7%,env(safe-area-inset-right,0px))}
  .ttl{font-size:clamp(40px,11.2vw,120px);padding-top:clamp(40px,10vh,90px)}
  .ttl .l2{padding-left:10%}
  .dgrid{grid-template-columns:minmax(0,1fr)}
  .portrait{aspect-ratio:4/3;max-height:none}
  .focus{grid-template-columns:minmax(0,1fr)}
  .tiles{grid-template-columns:minmax(0,1fr)}
  .stile{min-height:0;flex-direction:row;align-items:center;gap:20px;padding:22px 64px 22px 22px}
  .stile .txt{margin-top:0}
  .stile .vw{top:50%;transform:translateY(-50%)}
}
@media (max-width:600px){
  .top .tag{display:none}
  .stats dd{font-size:20px}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none !important;transition:none !important}}
"""

ARROW_BTN = '<svg width="22" height="12" viewBox="0 0 22 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M0 6h21M16 1l5 5-5 5"/></svg>'
ARROW_LNK = '<svg height="10" viewBox="0 0 46 10" preserveAspectRatio="none" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M0 5h45M40 1l5 4-5 4"/></svg>'
NE = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M2 8L8 2M3.5 2H8v4.5"/></svg>'
ICONS = {
    "Instagram": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>',
    "Facebook": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg>',
    "LinkedIn": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M7 10v8M7 6v.01M11 18v-5a3 3 0 0 1 6 0v5M11 10v8"/></svg>',
}
SOCIALS = [
    ("Instagram", "https://www.instagram.com/kennysinternational/", "@kennysinternational"),
    ("Facebook", "https://www.facebook.com/KennysInternationals", "KennysInternationals"),
    ("LinkedIn", "https://www.linkedin.com/company/kennysinternational/", "Kenny's International"),
]
EXT = 'target="_blank" rel="noopener"'

FOOTER = f"""
<footer class="dark foot">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="fbrand"><img src="assets/emblem.png" alt=""><span class="wide">Kenny's<br>International</span></div>
        <p class="gold ftag">Sharing the luxury of your life since 1993.</p>
      </div>
      <nav aria-label="Footer">
        <p class="cap gold fh">Explore</p>
        <ul class="flist">
          <li><a href="{MAIN}/about-us.html" {EXT}>About us</a></li>
          <li><a href="{MAIN}/distribution-brands.html" {EXT}>Distribution brands</a></li>
          <li><a href="{MAIN}/k-galerie.html" {EXT}>K-Galerie</a></li>
          <li><a href="{MAIN}/franchise-retail.html" {EXT}>Franchise retail</a></li>
          <li><a href="{MAIN}/press" {EXT}>Press</a></li>
          <li><a href="{MAIN}/contact.html" {EXT}>Contact</a></li>
        </ul>
      </nav>
      <div>
        <p class="cap gold fh">Head office</p>
        <p class="faddr">124 Boulevard du 30 Juin, Gombe, Kinshasa<br>Royal building, ref. K Lounge, opposite Interpol<br><a href="tel:+243818592999">+243 818 592 999</a><br><a href="mailto:serviceclient@kennysinternational.com">serviceclient@kennysinternational.com</a></p>
      </div>
      <div>
        <p class="cap gold fh">Follow</p>
        <ul class="flist">
          {''.join(f'<li><a href="{u}" {EXT}>{n}</a></li>' for n, u, _ in SOCIALS)}
        </ul>
      </div>
    </div>
    <div class="fbar"><span>© 2026 Kenny's Group. All rights reserved.</span><span>Kinshasa, Lubumbashi, Kolwezi, Pointe-Noire</span></div>
  </div>
</footer>"""


def page(title, body):
    return (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="Kenny\'s International, sharing the luxury of your life since 1993.">\n'
            f'{FONTS}\n<style>{CSS}</style>\n{body}\n{FOOTER}\n')


def brand(link=None):
    inner = '<img src="assets/emblem.png" alt=""><span class="cap">Kenny\'s International</span>'
    if link:
        return f'<a class="brand" href="{link}" {EXT} aria-label="Kenny\'s International, home">{inner}</a>'
    return f'<span class="brand">{inner}</span>'


# ---------------- HOME ----------------
home = f"""
<section class="hero" aria-labelledby="hero-h">
  <div class="frame">
    <img class="hbg" src="assets/hero-kennys.jpg" alt="The Kenny's building in Kinshasa">
    <div class="glass" aria-hidden="true"></div>
    <header class="top">{brand()}<span class="cap tag">Since 1993</span></header>
    <h1 id="hero-h" class="ttl" aria-label="Kenny's International"><span>kenny's</span><span class="l2">international</span></h1>
    <div class="hinfo">
      <p class="cap gold" style="margin:0">by Kenny's Group</p>
      <p class="body">The world's leading watch, jewellery and fashion houses, presented together in Kinshasa, Lubumbashi, Kolwezi and Pointe-Noire since 1993.</p>
      <dl class="stats">
        <div><dt class="cap">Since</dt><dd class="wide gold">1993</dd></div>
        <div><dt class="cap">Franchises</dt><dd class="wide gold">16</dd></div>
        <div><dt class="cap">Distribution brands</dt><dd class="wide gold">21</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="light band" aria-labelledby="web-h">
  <div class="wrap web">
    <div class="txt">
      <p class="cap gold" style="margin:0">Main website</p>
      <h2 id="web-h" class="wide h2 rise">The full world of Kenny's</h2>
      <p class="body rise r2">Our houses, our franchise stores, K-Galerie in Pointe-Noire and the latest press, all in one place.</p>
      <a class="btn solid" href="{MAIN}/" {EXT}>Visit the website{ARROW_BTN}</a>
    </div>
    <a class="webcard rise r2" href="{MAIN}/" {EXT}>
      <div class="ph"><img src="assets/about-storefront.jpg" alt="The Kenny's flagship storefront in Kinshasa"></div>
      <div class="bar"><span class="wide">kennysinternational.com</span><span class="vw">{NE}</span></div>
    </a>
  </div>
</section>

<section class="light band socband" aria-labelledby="soc-h">
  <div class="wrap"><div class="inner">
    <div class="head">
      <div><p class="cap gold">Follow us</p><h2 id="soc-h" class="wide h2 rise">Kenny's on social media</h2></div>
      <p class="body rise r2">Store openings, new arrivals from the houses and private events, as they happen.</p>
    </div>
    <ul class="tiles">
      {''.join(f'<li><a class="stile rise r{i+1}" href="{u}" {EXT}><span class="ic">{ICONS[n]}</span><span class="txt"><span class="nm wide">{n}</span><span class="hd">{h}</span></span><span class="vw">{NE}</span></a></li>' for i, (n, u, h) in enumerate(SOCIALS))}
    </ul>
  </div></div>
</section>
"""

# ---------------- DIRECTORS ----------------
DIRECTORS = [
    dict(slug="john-doe", first="john", last="doe", full="John Doe", role="Marketing Director", initials="JD",
         img="hero-boggi.jpg",
         bio="John Doe leads marketing for Kenny's International. He shapes how the group presents its watch, jewellery and fashion houses in Kinshasa, Lubumbashi, Kolwezi and Pointe-Noire, from store openings and private client events to the press and the group's social channels.",
         facts=[("Department", "Marketing"), ("Office", "Kinshasa"), ("Distribution brands", "21")],
         quote="Every house we carry has its own story. Our work is to tell it here, to clients who know craftsmanship.",
         socials=[("LinkedIn", "", "John Doe"), ("Instagram", "", "@johndoe"), ("Facebook", "", "John Doe")],
         gallery_intro="Openings, private evenings and the houses John works with across the group.",
         focus=[("Brand & campaigns", "Plans each season's campaigns with the partner houses and keeps every message true to both the house and Kenny's."),
                ("Openings & events", "Leads store launches and private client evenings across the group, including at K-Galerie in Pointe-Noire."),
                ("Press & digital", "Oversees press relations, the website and the group's Instagram, Facebook and LinkedIn channels.")]),
    dict(slug="jane-doe", first="jane", last="doe", full="Jane Doe", role="Sales Director", initials="JD",
         img="about-storefront.jpg",
         bio="Jane Doe leads sales across Kenny's Stores and the group's franchise stores. She works with store teams in all four cities so that every client receives attentive, informed advice, whatever the house or the piece.",
         facts=[("Department", "Sales"), ("Office", "Kinshasa"), ("Franchises", "16")],
         quote="A client should leave with the right piece and a reason to come back.",
         socials=[("LinkedIn", "", "Jane Doe"), ("Instagram", "", "@janedoe"), ("Facebook", "", "Jane Doe")],
         gallery_intro="Stores, collections and the pieces Jane's teams present to clients every day.",
         focus=[("Store performance", "Sets sales objectives for Kenny's Stores and the franchise stores, and follows results store by store."),
                ("Private clients", "Builds long-term relationships with private clients through personal appointments, previews and after-sales care."),
                ("Sales teams", "Trains advisers to the standards of each house, from product knowledge to the way a client is welcomed.")]),
    dict(slug="richard-roe", first="richard", last="roe", full="Richard Roe", role="Operations Director", initials="RR",
         img="kgalerie-hero.jpg",
         bio="Richard Roe runs operations for Kenny's International. He makes sure the group's stores in Kinshasa, Lubumbashi, Kolwezi and Pointe-Noire are stocked, staffed and ready, and he oversees the sites that host them, including K-Galerie.",
         facts=[("Department", "Operations"), ("Office", "Kinshasa"), ("Distribution brands", "21")],
         quote="Clients see the finished store. Our work is everything that has to happen before the doors open.",
         socials=[("LinkedIn", "", "Richard Roe"), ("Instagram", "", "@richardroe"), ("Facebook", "", "Richard Roe")],
         gallery_intro="The sites, stores and openings Richard's teams prepare across the group.",
         focus=[("Store operations", "Sets the standards every store follows, from opening routines to visual presentation and security."),
                ("Supply & logistics", "Coordinates shipments from the houses to Kinshasa and Pointe-Noire, and keeps stock moving between stores."),
                ("Sites & projects", "Oversees K-Galerie and new store fit-outs, from the first plans to the day the doors open.")]),
]


GAL_SRC = pathlib.Path(__file__).parent / "gallery"
GAL_FIRST = 6   # photos shown before "Show more"
GAL_STEP = 9    # photos added per "Show more"
ARROW_L = '<svg width="22" height="12" viewBox="0 0 22 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M22 6H1M6 1L1 6l5 5"/></svg>'
CLOSE = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13"/></svg>'


def gallery_photos(slug):
    """Resize every photo in gallery/<slug>/ into a full-size view and a grid thumbnail."""
    src = GAL_SRC / slug
    out = OUT / "assets" / "gallery" / slug
    out.mkdir(parents=True, exist_ok=True)
    caps_file = src / "captions.json"
    caps = json.loads(caps_file.read_text()) if caps_file.exists() else {}
    photos = []
    for f in sorted(x for x in src.iterdir() if x.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")):
        full, thumb = out / f"{f.stem}.jpg", out / f"{f.stem}-t.jpg"
        im = Image.open(f).convert("RGB")
        if not full.exists() or full.stat().st_mtime < f.stat().st_mtime:
            big = im.copy(); big.thumbnail((1800, 1800)); big.save(full, quality=82, optimize=True, progressive=True)
            sm = im.copy(); sm.thumbnail((720, 2000)); sm.save(thumb, quality=78, optimize=True, progressive=True)
        tw, th = Image.open(thumb).size
        photos.append(dict(full=f"assets/gallery/{slug}/{full.name}", thumb=f"assets/gallery/{slug}/{thumb.name}",
                           w=tw, h=th, cap=caps.get(f.name, "")))
    return photos


def social_tiles(socials):
    tiles = []
    for i, (n, u, h) in enumerate(socials):
        inner = f'<span class="ic">{ICONS[n]}</span><span class="txt"><span class="nm wide">{n}</span><span class="hd">{h}</span></span>'
        if u:
            tiles.append(f'<li><a class="stile rise r{i+1}" href="{u}" {EXT}>{inner}<span class="vw">{NE}</span></a></li>')
        else:
            tiles.append(f'<li><div class="stile rise r{i+1}">{inner}</div></li>')
    return ''.join(tiles)


GALLERY_JS = r"""
<script>
(function(){
  var list=document.querySelector('.masonry'), dlg=document.querySelector('.lb');
  if(!list||!dlg) return;
  var items=[].slice.call(list.querySelectorAll('.gi'));
  var step=+list.getAttribute('data-step')||9;
  var more=document.querySelector('.gmore');
  function refreshMore(){
    if(!more) return;
    var left=list.querySelectorAll('li[hidden]').length;
    more.hidden=!left;
    var n=more.querySelector('.n'); if(n) n.textContent=Math.min(left,step);
  }
  if(more) more.querySelector('button').addEventListener('click',function(){
    var hid=[].slice.call(list.querySelectorAll('li[hidden]')).slice(0,step);
    hid.forEach(function(li){li.hidden=false;});
    if(hid[0]) hid[0].querySelector('a').focus();
    refreshMore();
  });
  refreshMore();
  var img=dlg.querySelector('.lb-img'), cap=dlg.querySelector('.lb-cap'), cnt=dlg.querySelector('.lb-count'), fig=dlg.querySelector('.lb-fig');
  var cur=0;
  function pad(n){return (n<10?'0':'')+n;}
  function show(k){
    cur=(k+items.length)%items.length;
    var a=items[cur], t=a.querySelector('img');
    img.classList.remove('on');
    img.onload=function(){img.classList.add('on');};
    img.src=a.getAttribute('href'); img.alt=t.alt;
    if(img.complete) img.classList.add('on');
    cap.textContent=a.getAttribute('data-cap')||'';
    cnt.textContent=pad(cur+1)+' / '+pad(items.length);
    [1,-1].forEach(function(o){var pre=new Image(); pre.src=items[(cur+o+items.length)%items.length].getAttribute('href');});
  }
  function open(k){show(k); if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');}
  function close(){if(dlg.close) dlg.close(); else dlg.removeAttribute('open');}
  items.forEach(function(a,k){a.addEventListener('click',function(e){e.preventDefault();open(k);});});
  dlg.querySelector('.lb-prev').addEventListener('click',function(){show(cur-1);});
  dlg.querySelector('.lb-next').addEventListener('click',function(){show(cur+1);});
  dlg.querySelector('.lb-x').addEventListener('click',close);
  fig.addEventListener('click',function(e){if(e.target===fig) close();});
  dlg.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){e.preventDefault();show(cur-1);}
    if(e.key==='ArrowRight'){e.preventDefault();show(cur+1);}
  });
  var x0=null;
  fig.addEventListener('pointerdown',function(e){x0=e.clientX;});
  fig.addEventListener('pointerup',function(e){
    if(x0===null) return; var dx=e.clientX-x0; x0=null;
    if(Math.abs(dx)>50) show(dx<0?cur+1:cur-1);
  });
})();
</script>"""


def gallery_section(d):
    photos = gallery_photos(d["slug"])
    first = d["full"].split()[0]
    lis = []
    for i, ph in enumerate(photos):
        alt = ph["cap"] or f"Photo {i+1}"
        hid = " hidden" if i >= GAL_FIRST else ""
        lis.append(f'<li{hid}><a class="gi" href="{ph["full"]}" data-cap="{ph["cap"]}" aria-label="Open photo {i+1} of {len(photos)}: {alt}">'
                   f'<img src="{ph["thumb"]}" width="{ph["w"]}" height="{ph["h"]}" alt="{alt}" loading="lazy" decoding="async">'
                   f'<span class="gcap" aria-hidden="true">{ph["cap"]}</span></a></li>')
    left = max(0, len(photos) - GAL_FIRST)
    more = (f'<div class="gmore"><button class="btn" type="button"><span>Show <span class="n">{min(left, GAL_STEP)}</span> more photos</span>{ARROW_BTN}</button></div>'
            if left else '')
    return f"""
<section class="dark band gal" aria-labelledby="gal-h">
  <div class="wrap">
    <div class="head">
      <div><p class="cap gold">Gallery</p><h2 id="gal-h" class="wide h2 rise">In pictures</h2></div>
      <p class="body rise r2">{d['gallery_intro']}<span class="cap gold count">{len(photos)} photos</span></p>
    </div>
    <ul class="masonry" data-step="{GAL_STEP}">{''.join(lis)}</ul>
    {more}
    <div class="back">
      <a class="lnk" href="{HOME_URL}" {EXT}>Kenny's International{ARROW_LNK}</a>
      <a class="lnk" href="{MAIN}/" {EXT}>kennysinternational.com{ARROW_LNK}</a>
    </div>
  </div>
</section>
<dialog class="lb" aria-label="{first}'s photos">
  <div class="lb-bar t"><span class="cap lb-count">01 / {len(photos):02d}</span><button class="lb-x" type="button">Close{CLOSE}</button></div>
  <figure class="lb-fig"><img class="lb-img" alt=""></figure>
  <div class="lb-bar b"><p class="lb-cap"></p><div class="lb-nav"><button class="arr p lb-prev" type="button" aria-label="Previous photo">{ARROW_L}</button><button class="arr n lb-next" type="button" aria-label="Next photo">{ARROW_BTN}</button></div></div>
</dialog>
{GALLERY_JS}
"""


def director(d):
    words = not all(v.isdigit() for _, v in d["facts"])
    facts = ''.join(f'<div><dt class="cap">{k}</dt><dd class="wide gold">{v}</dd></div>' for k, v in d["facts"])
    focus = ''.join(f'<li class="rise r{i+1}"><span class="dia" aria-hidden="true"></span><h3 class="wide">{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(d["focus"]))
    return f"""
<section class="dark dhero" aria-labelledby="name-h">
  <div class="wrap">
    <header class="top">{brand(HOME_URL)}<span class="cap tag">Leadership</span></header>
    <div class="dgrid">
      <figure class="portrait" aria-label="{d['full']}, {d['role']}">
        <img class="pbg" src="assets/{d['img']}" alt="">
        <img class="em" src="assets/emblem.png" alt="">
        <span class="mono" aria-hidden="true">{d['initials']}</span>
        <figcaption class="cap">{d['role']}</figcaption>
      </figure>
      <div class="dtxt">
        <p class="cap gold role">{d['role']} · Kenny's International</p>
        <h1 id="name-h" class="name" aria-label="{d['full']}"><span>{d['first']}</span><span class="l2">{d['last']}</span></h1>
        <p class="body">{d['bio']}</p>
        <dl class="stats{' words' if words else ''}">{facts}</dl>
      </div>
    </div>
  </div>
</section>

<section class="light band" aria-labelledby="focus-h">
  <div class="wrap">
    <div class="head">
      <div><p class="cap gold">The role</p><h2 id="focus-h" class="wide h2 rise">Areas of focus</h2></div>
      <blockquote class="quote rise r2"><p>“{d['quote']}”</p><cite class="cap gold">{d['full']}</cite></blockquote>
    </div>
    <ul class="focus">{focus}</ul>
  </div>
</section>

<section class="light band socband" aria-labelledby="soc-h">
  <div class="wrap"><div class="inner">
    <div class="head">
      <div><p class="cap gold">Follow {d['full'].split()[0]}</p><h2 id="soc-h" class="wide h2 rise">On social media</h2></div>
      <p class="body rise r2">News, events and moments from {d['full'].split()[0]}'s work at Kenny's International.</p>
    </div>
    <ul class="tiles">{social_tiles(d['socials'])}</ul>
  </div></div>
</section>
{gallery_section(d)}"""


OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(page("Kenny's International", home))
for d in DIRECTORS:
    (OUT / f"{d['slug']}.html").write_text(page(f"{d['full']}, {d['role']}", director(d)))
print("built", [p.name for p in OUT.glob('*.html')])

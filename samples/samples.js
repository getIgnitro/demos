/* samples.js — personalisation (?b=), pre-filled WhatsApp, reels, tracer.
   Per-page config is read from <body data-page="social|web" data-msg="..."> */
(function(){
  var body=document.body, PAGE=body.getAttribute('data-page')||'page', MSG=body.getAttribute('data-msg')||"I'd like to get started.";
  /* ---------- personalisation ---------- */
  var q=new URLSearchParams(location.search), raw=(q.get('b')||'').replace(/[-_+]+/g,' ').trim();
  var biz=raw?raw.replace(/\b\w/g,function(c){return c.toUpperCase();}):'';
  var h1=document.getElementById('h1'), forEl=document.getElementById('for');
  if(biz){ if(forEl) forEl.textContent='For '+biz;
    if(h1&&h1.getAttribute('data-p')) h1.innerHTML=biz+' — '+h1.getAttribute('data-p');
    document.title=biz+' — KN Services'; }
  /* ---------- WhatsApp with the business already typed ---------- */
  var NUMBER='97460027117'; /* TODO: switch to the US (Tello) number when it exists */
  var msg='Hi KN Services, '+(biz?"I'm from "+biz+' and ':'')+MSG;
  var wa='https://wa.me/'+NUMBER+'?text='+encodeURIComponent(msg);
  ['wa-go','wa-top'].forEach(function(id){var el=document.getElementById(id); if(el) el.href=wa;});
  /* ---------- tracer (dormant until TRACER is set) ---------- */
  var TRACER=''; /* TODO: Apps Script web-app URL */
  var sent={};
  function track(ev){ if(!TRACER||sent[ev]) return; sent[ev]=1;
    try{ fetch(TRACER,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify({b:raw||'(no code)',page:PAGE,ev:ev,t:new Date().toISOString()})}); }catch(e){} }
  window.knTrack=track;
  track('open');
  document.querySelectorAll('[data-ev]').forEach(function(el){el.addEventListener('click',function(){track(el.getAttribute('data-ev'));});});
  var seen=false; window.addEventListener('scroll',function(){ if(seen) return; var t=document.querySelector('table'); if(t&&t.getBoundingClientRect().top<window.innerHeight){seen=true; track('prices');} },{passive:true});
  /* ---------- reels (only if the page has #reels) ---------- */
  var g=document.getElementById('reels'); if(!g) return;
  var A='https://portfolio.getignitro.com/portfolio_assets/';
  var reels=[['r01','Restaurant'],['r03','Restaurant'],['r04','Restaurant'],['r05','Restaurant'],['r02','Restaurant'],['r13','Restaurant'],['r16','Restaurant'],['r11','Salon'],['r12','Salon'],['r24','Salon'],['r10','Flowers'],['r22','Flowers']];
  var n=parseInt(g.getAttribute('data-n')||'12',10);
  g.innerHTML=reels.slice(0,n).map(function(r){return '<a class="reel" href="#" data-id="'+r[0]+'"><video muted loop playsinline preload="none" poster="'+A+'posters/'+r[0]+'.jpg" data-src="'+A+'reels_lite/'+r[0]+'.mp4"></video><span class="play"><i></i></span><span class="tag">'+r[1]+'</span></a>';}).join('');
  var cur=null;
  g.addEventListener('click',function(e){var a=e.target.closest('.reel'); if(!a) return; e.preventDefault();
    var v=a.querySelector('video'); if(!v.src){v.src=v.getAttribute('data-src');}
    if(cur&&cur!==a){var cv=cur.querySelector('video'); cv.pause(); cv.muted=true; cur.classList.remove('on');}
    if(a.classList.contains('on')){v.pause(); v.muted=true; a.classList.remove('on'); cur=null; return;}
    v.muted=false; v.play(); a.classList.add('on'); cur=a; track('reel:'+a.getAttribute('data-id'));});
})();

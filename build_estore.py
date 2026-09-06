"""Builds intl/estore/ — Maison Cacao, a full e-commerce demo ($700 listing): 40 products, shop filters,
product pages, cart, checkout with simulated Stripe/PayPal, account + order history, policies, cookie consent.
Run from repo root (build_intl.py calls it at the end)."""
import pathlib, json
root = pathlib.Path(__file__).parent
out = root / "intl" / "estore"; out.mkdir(parents=True, exist_ok=True)

# ---------- 40 products from 8 verified photos ----------
U = lambda i: f"https://images.unsplash.com/photo-{i}?w=800&h=800&fit=crop&q=75"
IMG = {"box": U("1481391319762-47dff72954d9"), "cake": U("1578985545062-69928b1d9587"), "drip": U("1616690710400-a16d146927c5"),
       "cookies": U("1558961363-fa8fdf82db35"), "cupcake": U("1599785209707-a456fc1337bb"), "cupcakes2": U("1607478900766-efe13248b125"),
       "donut": U("1551024601-bec78aea704b"), "crepe": U("1587314168485-3236d6710814"), "tiramisu": U("1571115177098-24ec42ed204d")}
P = []
def add(cat, name, price, img, desc, tag=None, stock=12):
    P.append({"id": f"p{len(P)+1:02d}", "cat": cat, "name": name, "price": price, "img": IMG[img], "desc": desc, "tag": tag, "stock": stock})
for n, pr in [(9, 18), (16, 29), (24, 42), (36, 59), (48, 76)]:
    add("pralines", f"Signature Praliné Box · {n} pieces", pr, "box", "Hazelnut, sea-salt caramel, pistachio and 70% dark, hand-finished in Brussels.", "BEST SELLER" if n == 16 else None)
for fl, pr in [("Dark 70%", 12), ("Milk 38%", 12), ("Hazelnut", 14), ("Sea Salt", 14), ("Pistachio", 16), ("Orange Peel", 14), ("Speculoos", 14), ("Raspberry", 15)]:
    add("bars", f"Tablet · {fl} · 100 g", pr, "box", "Single-origin couverture, tempered by hand. Snaps clean, melts slow.")
for fl, pr in [("Champagne", 24), ("Espresso", 22), ("Salted Caramel", 22), ("Raspberry Rose", 24), ("Praliné Crunch", 22), ("Matcha", 24)]:
    add("truffles", f"Truffle Selection · {fl} · 12 pcs", pr, "box", "Ganache rolled in cocoa, boxed the morning it is made.", "NEW" if fl == "Matcha" else None)
add("pastries", "Gâteau au Chocolat · serves 10", 48, "cake", "Three layers, dark ganache, piped rosettes. Made to order.")
add("pastries", "Fraisier · serves 12", 64, "drip", "Génoise, strawberries, crème mousseline. Made to order.", "SEASONAL")
add("pastries", "Sablés au Chocolat · box of 12", 14, "cookies", "Buttery shortbread, chocolate chips, baked each morning.")
add("pastries", "Cupcakes de Fête · box of 6", 19, "cupcake", "Vanilla and chocolate, your colours on request.")
add("pastries", "Cupcakes de Fête · box of 12", 34, "cupcakes2", "Vanilla and chocolate, your colours on request.")
add("pastries", "Beignets Glacés · box of 6", 15, "donut", "Chocolate, vanilla and sprinkles.")
add("pastries", "Crêpes aux Fraises · box of 4", 18, "crepe", "Fresh cream and strawberries, made to order.")
add("pastries", "Tiramisu · 4 parts", 21, "tiramisu", "Coffee-soaked, mascarpone, cocoa. Alcohol-free.")
for name, pr, img, d in [("Discovery Gift Set", 39, "box", "Praliné 9 + two tablets + a truffle box, ribboned."), ("Grand Gift Hamper", 89, "box", "Praliné 24, four tablets, two truffle boxes, handwritten card."),
                          ("Corporate Box · 20 units", 340, "box", "Twenty Praliné 9 boxes with your logo on the sleeve. 48 h notice."), ("Wedding Favour Set · 50 units", 425, "box", "Fifty two-piece boxes, ribbon in your colours."),
                          ("Advent Calendar", 46, "box", "24 doors, 24 pralines. Ships from 1 November.", ), ("Easter Egg · 300 g", 32, "box", "Hand-painted milk chocolate egg filled with mini pralines.")]:
    add("gifts", name, pr, img, d, "GIFT")
for name, pr, img, d in [("Hot Chocolate Flakes · 250 g", 13, "box", "Real couverture flakes. Two spoons per cup."), ("Cocoa Nibs · 200 g", 9, "box", "Roasted, unsweetened, for baking and bowls."),
                          ("Baking Couverture · 1 kg", 28, "box", "Dark 64%, callets, for professionals and serious home bakers."), ("Praliné Spread · 300 g", 11, "box", "Hazelnut praliné, no palm oil."),
                          ("Chocolate Fondue Kit", 36, "cake", "500 g couverture, ceramic pot, four forks."), ("Tasting Flight · 6 origins", 27, "box", "Six 20 g squares, tasting card included.")]:
    add("pantry", name, pr, img, d)
assert len(P) == 40, len(P)
CATS = [("all", "All"), ("pralines", "Pralines"), ("truffles", "Truffles"), ("bars", "Tablets"), ("pastries", "Pastries"), ("gifts", "Gifts"), ("pantry", "Pantry")]

CSS = '''/* Maison Cacao — e-commerce demo */
:root{--cocoa:#2B1A12;--cream:#FAF6F0;--gold:#B8892E;--gold2:#F0E3CC;--ink:#1F150F;--mute:#7A6656;--line:#E8DED0;--ok:#1E7F4F;--wa:#25D366}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,sans-serif;background:var(--cream);color:var(--ink);line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;line-height:1.08;letter-spacing:.2px}
a{color:inherit;text-decoration:none}img{max-width:100%;display:block}button{font:inherit;cursor:pointer}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
.ship{background:var(--cocoa);color:#EAD9C0;text-align:center;font-size:12.5px;padding:8px 12px}
header{position:sticky;top:0;z-index:20;background:rgba(250,246,240,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav{display:flex;align-items:center;justify-content:space-between;height:70px;gap:14px}
.logo{font-family:'Cormorant Garamond',serif;font-size:26px;letter-spacing:1px;font-weight:600}.logo b{color:var(--gold);font-weight:600}
.menu{display:flex;gap:22px;font-size:14px;font-weight:600}.menu a.active,.menu a:hover{color:var(--gold)}
.right{display:flex;gap:10px;align-items:center}
.icon{position:relative;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:8px}
.icon i{font-style:normal;background:var(--cocoa);color:#fff;border-radius:999px;min-width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:900}
.burger{display:none;background:none;border:0;font-size:26px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--cocoa);color:#fff;font-weight:700;padding:13px 22px;border-radius:999px;font-size:14.5px;border:0}
.btn.gold{background:var(--gold);color:#fff}.btn.line{background:transparent;border:1.5px solid var(--cocoa);color:var(--cocoa)}.btn.w{width:100%}
.btn[disabled]{opacity:.5;cursor:default}
.hero{position:relative;min-height:66vh;display:grid;align-items:center;color:#fff;overflow:hidden;background:var(--cocoa)}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(43,26,18,.85),rgba(43,26,18,.15))}
.hero .wrap{position:relative;z-index:1;padding:70px 20px;text-align:center}
.eyebrow{display:inline-block;font-size:12px;letter-spacing:3px;text-transform:uppercase;font-weight:700;color:var(--gold);margin-bottom:12px}
.hero h1{font-size:clamp(40px,6.5vw,76px);max-width:820px;margin:0 auto}.hero p{margin:14px auto 0;font-size:18px;max-width:560px;color:#EAD9C0}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px;justify-content:center}
section{padding:60px 0}.sec-h{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:26px;flex-wrap:wrap}
.sec-h h2{font-size:clamp(28px,4vw,42px)}.sec-h p{color:var(--mute)}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.p{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 26px rgba(43,26,18,.06);display:flex;flex-direction:column;position:relative}
.p img{aspect-ratio:1;object-fit:cover;width:100%}.p .b{padding:14px 14px 16px;display:flex;flex-direction:column;gap:5px;flex:1}
.p h3{font-size:19px}.p .d{color:var(--mute);font-size:13px;flex:1}.p .pr{display:flex;justify-content:space-between;align-items:center;margin-top:8px}
.p .pr b{font-size:16px}.badge{position:absolute;top:10px;left:10px;background:var(--gold);color:#fff;font-size:10.5px;font-weight:900;letter-spacing:1px;padding:5px 9px;border-radius:999px}
.wish{position:absolute;top:10px;right:10px;background:#fff;border:0;border-radius:50%;width:32px;height:32px;font-size:15px}.wish.on{color:#c0392b}
.add{font-size:13px;font-weight:800;background:var(--cocoa);color:#fff;border:0;border-radius:999px;padding:8px 14px}.add.done{background:var(--gold)}
.low{font-size:11px;color:#b04a3a;font-weight:700}
.toolbar{display:grid;grid-template-columns:1fr auto auto;gap:10px;margin-bottom:18px}
.toolbar input,.toolbar select{font:inherit;padding:11px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff}
.cats{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.cats button{font-size:13px;font-weight:700;padding:8px 14px;border-radius:999px;border:1.5px solid var(--cocoa);background:none;color:var(--cocoa)}.cats button.on{background:var(--cocoa);color:#fff}
.usp{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.usp div{background:#fff;border-radius:14px;padding:20px;text-align:center}.usp b{display:block;font-family:'Cormorant Garamond',serif;font-size:22px}.usp span{color:var(--mute);font-size:13.5px}
.pd{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}.pd img{border-radius:20px;aspect-ratio:1;object-fit:cover}
.pd h1{font-size:clamp(30px,4vw,46px)}.pd .price{font-size:28px;font-weight:800;margin:12px 0}.pd .d{color:var(--mute);font-size:16px}
.qty{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:#fff}.qty button{background:none;border:0;width:36px;height:38px;font-weight:900}.qty span{min-width:28px;text-align:center;font-weight:800}
.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:16px}
.meta{margin-top:22px;font-size:13.5px;color:var(--mute);line-height:1.8}.meta b{color:var(--ink)}
.rev{margin-top:26px;border-top:1px solid var(--line);padding-top:18px}.rev .r{background:#fff;border-radius:12px;padding:12px 14px;margin-bottom:8px;font-size:14px}.rev .r b{display:block;font-size:13px}.stars{color:var(--gold)}
.cart{display:grid;grid-template-columns:1.4fr .9fr;gap:30px;align-items:start}
.line{display:grid;grid-template-columns:70px 1fr auto auto;gap:14px;align-items:center;background:#fff;border-radius:14px;padding:12px;margin-bottom:10px}
.line img{width:70px;height:70px;border-radius:10px;object-fit:cover}.line b{display:block;font-size:15px}.line small{color:var(--mute)}
.rm{background:none;border:0;color:#b04a3a;font-size:13px;font-weight:700}
.sum{background:#fff;border-radius:18px;padding:22px;position:sticky;top:90px}.sum .r{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px dashed var(--line);font-size:15px}.sum .r.t{border:0;font-size:20px;font-weight:800;margin-top:6px}
.coupon{display:flex;gap:8px;margin:10px 0}.coupon input{flex:1}
label{display:block;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--mute);margin:12px 0 6px}
input,select,textarea{width:100%;font:inherit;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.empty{text-align:center;padding:60px 20px;color:var(--mute)}
.chk{display:grid;grid-template-columns:1.2fr .8fr;gap:30px;align-items:start}
.step{background:#fff;border-radius:18px;padding:22px;margin-bottom:16px}.step h3{font-size:22px;margin-bottom:6px}
.pay-tabs{display:flex;gap:8px;margin:10px 0 6px}.pay-tabs button{flex:1;padding:12px;border-radius:12px;border:1.5px solid var(--line);background:#fff;font-weight:700}.pay-tabs button.on{border-color:var(--cocoa);background:var(--gold2)}
.card-ui{background:#F6F1E8;border-radius:14px;padding:14px;margin-top:8px}
.secure{font-size:12px;color:var(--mute);margin-top:10px}.secure b{color:var(--ok)}
.demo-note{background:#FFF4D6;border:1px solid #F0D48A;border-radius:12px;padding:10px 14px;font-size:13px;margin-top:12px}
.done{background:#fff;border-radius:22px;padding:40px;text-align:center}.done .big{font-size:56px}.done h2{font-size:34px;margin:8px 0}.done p{color:var(--mute)}
.acct{display:grid;grid-template-columns:.9fr 1.3fr;gap:30px;align-items:start}
.orders .o{background:#fff;border-radius:14px;padding:14px 16px;margin-bottom:10px;font-size:14px}.orders .o b{display:block}.orders .o span{color:var(--mute)}
.pol h2{font-size:26px;margin:26px 0 8px}.pol p,.pol li{color:var(--mute);font-size:15px}.pol ul{padding-left:20px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}.split img{border-radius:22px;aspect-ratio:1;object-fit:cover}.split h2{font-size:clamp(28px,3.6vw,40px);margin-bottom:12px}.split p{color:var(--mute);margin-bottom:10px}
.contact{display:grid;grid-template-columns:1fr 1fr;gap:34px}.info div{margin-bottom:16px}.info b{display:block;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--gold)}
.map{border-radius:18px;overflow:hidden;border:0;width:100%;height:280px;margin-top:20px}
.news{background:var(--cocoa);color:#fff;border-radius:22px;padding:34px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}.news h2{font-size:30px}.news p{color:#EAD9C0}.news form{display:flex;gap:8px}.news input{width:260px}
footer{background:var(--cocoa);color:#D9C6AC;padding:44px 0 30px;font-size:13.5px;margin-top:20px}footer .wrap{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:24px}footer b{color:#fff;display:block;margin-bottom:6px}footer a{display:block;padding:2px 0}
footer .demo{grid-column:1/-1;margin-top:22px;padding-top:16px;border-top:1px solid #4d3628;opacity:.75;font-size:12px}
.cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:50;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 18px;display:none;gap:14px;align-items:center;justify-content:space-between;box-shadow:0 14px 40px rgba(0,0,0,.15);font-size:13.5px}
.cookie.show{display:flex}.cookie .b{display:flex;gap:8px}
.toast{position:fixed;left:50%;bottom:90px;transform:translateX(-50%);background:var(--cocoa);color:#fff;padding:12px 20px;border-radius:999px;font-size:14px;font-weight:700;opacity:0;transition:opacity .2s;pointer-events:none;z-index:40}.toast.show{opacity:1}
.wa{position:fixed;right:18px;bottom:18px;z-index:30;width:56px;height:56px;border-radius:50%;background:var(--wa);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(37,211,102,.4)}.wa svg{width:28px;height:28px;fill:#fff}
@media(max-width:960px){.grid{grid-template-columns:repeat(2,1fr)}.usp,.pd,.cart,.chk,.acct,.split,.contact{grid-template-columns:1fr}footer .wrap{grid-template-columns:1fr 1fr}
  .menu{display:none;position:absolute;top:70px;left:0;right:0;background:var(--cream);flex-direction:column;padding:18px 20px;gap:16px;border-bottom:1px solid var(--line)}.menu.open{display:flex}.burger{display:block}
  .sum{position:static}.toolbar{grid-template-columns:1fr}.line{grid-template-columns:60px 1fr}.line .qty,.line .rm{grid-column:2}section{padding:44px 0}.icon span.t{display:none}}
'''

JS = r'''// Maison Cacao — e-commerce demo. Static front end; cart/orders/wishlist in localStorage; payment simulated.
(function(){
  var P=__PRODUCTS__, CATS=__CATS__;
  var K={cart:'mc_cart',wish:'mc_wish',orders:'mc_orders',user:'mc_user',cookie:'mc_cookie',coupon:'mc_coupon'};
  var g=function(k,d){try{return JSON.parse(localStorage.getItem(k))||d;}catch(e){return d;}}, s=function(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
  var $=function(q,el){return (el||document).querySelector(q);}, $$=function(q,el){return Array.prototype.slice.call((el||document).querySelectorAll(q));};
  var money=function(n){return '$'+(Math.round(n*100)/100).toFixed(2).replace(/\.00$/,'');};
  var byId=function(id){return P.filter(function(p){return p.id===id;})[0];};
  function toast(t){var el=$('#toast'); if(!el) return; el.textContent=t; el.classList.add('show'); setTimeout(function(){el.classList.remove('show');},1400);}
  function counts(){var c=g(K.cart,{}),n=0; for(var k in c) n+=c[k]; $$('.cartn').forEach(function(e){e.textContent=n;}); $$('.wishn').forEach(function(e){e.textContent=g(K.wish,[]).length;});}
  function add(id,q){var c=g(K.cart,{}); c[id]=(c[id]||0)+(q||1); s(K.cart,c); counts(); toast('Added to cart');}
  function card(p){var w=g(K.wish,[]).indexOf(p.id)>=0; return '<div class="p">'+(p.tag?'<span class="badge">'+p.tag+'</span>':'')+'<button class="wish'+(w?' on':'')+'" data-w="'+p.id+'" aria-label="wishlist">'+(w?'♥':'♡')+'</button><a href="product.html?id='+p.id+'"><img src="'+p.img+'" alt="" loading="lazy"></a><div class="b"><h3><a href="product.html?id='+p.id+'">'+p.name+'</a></h3><div class="d">'+p.desc+'</div>'+(p.stock<=5?'<div class="low">Only '+p.stock+' left</div>':'')+'<div class="pr"><b>'+money(p.price)+'</b><button class="add" data-id="'+p.id+'">Add</button></div></div></div>';}
  function bind(root){$$('.add',root).forEach(function(b){b.onclick=function(){add(b.dataset.id,1); b.classList.add('done'); b.textContent='Added ✓'; setTimeout(function(){b.classList.remove('done'); b.textContent='Add';},1100);};});
    $$('.wish',root).forEach(function(b){b.onclick=function(){var w=g(K.wish,[]),i=w.indexOf(b.dataset.w); if(i>=0) w.splice(i,1); else w.push(b.dataset.w); s(K.wish,w); b.classList.toggle('on',i<0); b.textContent=i<0?'♥':'♡'; counts(); toast(i<0?'Saved to wishlist':'Removed from wishlist');};});}
  // nav
  var bg=$('#burger'),m=$('#menu'); if(bg&&m) bg.onclick=function(){m.classList.toggle('open');};
  // cookie consent (EU)
  var ck=$('#cookie'); if(ck&&!g(K.cookie,null)){ck.classList.add('show'); $$('#cookie button').forEach(function(b){b.onclick=function(){s(K.cookie,b.dataset.c); ck.classList.remove('show');};});}
  // home: featured
  var feat=$('#featured'); if(feat){feat.innerHTML=P.filter(function(p){return p.tag;}).slice(0,8).map(card).join(''); bind(feat);}
  // shop
  var grid=$('#products'); if(grid){
    var state={cat:(location.hash||'#all').slice(1),q:'',sort:'featured'};
    function render(){var list=P.filter(function(p){return (state.cat==='all'||p.cat===state.cat)&&(!state.q||(p.name+' '+p.desc).toLowerCase().indexOf(state.q)>=0);});
      if(state.sort==='low') list=list.slice().sort(function(a,b){return a.price-b.price;}); if(state.sort==='high') list=list.slice().sort(function(a,b){return b.price-a.price;}); if(state.sort==='name') list=list.slice().sort(function(a,b){return a.name.localeCompare(b.name);});
      grid.innerHTML=list.length?list.map(card).join(''):'<div class="empty">Nothing matches. Try another word.</div>'; bind(grid); var c=$('#count'); if(c) c.textContent=list.length+' of '+P.length+' products';
      $$('.cats button').forEach(function(b){b.classList.toggle('on',b.dataset.cat===state.cat);});}
    $$('.cats button').forEach(function(b){b.onclick=function(){state.cat=b.dataset.cat; location.hash=state.cat; render();};});
    var q=$('#q'); if(q) q.oninput=function(){state.q=q.value.trim().toLowerCase(); render();};
    var so=$('#sort'); if(so) so.onchange=function(){state.sort=so.value; render();};
    render();
  }
  // product page
  var pd=$('#pd'); if(pd){var id=(location.search.match(/id=(p\d+)/)||[])[1], p=byId(id)||P[0]; document.title=p.name+' — Maison Cacao'; var qty=1;
    var rel=P.filter(function(x){return x.cat===p.cat&&x.id!==p.id;}).slice(0,4);
    pd.innerHTML='<img src="'+p.img+'" alt=""><div>'+(p.tag?'<span class="badge" style="position:static;display:inline-block;margin-bottom:10px">'+p.tag+'</span>':'')+'<h1>'+p.name+'</h1><div class="stars">★★★★★ <span style="color:var(--mute);font-size:13px">4.9 · 128 reviews</span></div><div class="price">'+money(p.price)+'</div><p class="d">'+p.desc+'</p><div class="row"><div class="qty"><button id="qm">−</button><span id="qv">1</span><button id="qp">+</button></div><button class="btn" id="addp">Add to cart</button><button class="btn line" id="buy">Buy now</button></div><div class="meta"><b>Ships</b> in 1–2 working days · <b>Free delivery</b> over $60 · <b>Returns</b> 14 days on unopened goods · <b>Stock</b> '+(p.stock<=5?'only '+p.stock+' left':'in stock')+'</div><div class="rev"><h3 style="font-size:20px;margin-bottom:8px">Reviews</h3><div class="r"><b>Marie L. · Brussels</b>"The praliné box is the one gift everyone asks where I got it."</div><div class="r"><b>Tom H. · Antwerp</b>"Arrived next day, perfectly packed, nothing melted."</div></div></div>';
    $('#qm').onclick=function(){qty=Math.max(1,qty-1); $('#qv').textContent=qty;}; $('#qp').onclick=function(){qty++; $('#qv').textContent=qty;};
    $('#addp').onclick=function(){add(p.id,qty);}; $('#buy').onclick=function(){add(p.id,qty); location.href='checkout.html';};
    var rg=$('#related'); if(rg){rg.innerHTML=rel.map(card).join(''); bind(rg);}
  }
  // cart + checkout totals
  function totals(){var c=g(K.cart,{}),sub=0,items=[]; for(var k in c){var p=byId(k); if(p){sub+=p.price*c[k]; items.push({p:p,q:c[k]});}}
    var cp=g(K.coupon,null), disc=cp==='WELCOME10'?sub*0.10:0, ship=(sub-disc)>=60||sub===0?0:6, tax=0; return {items:items,sub:sub,disc:disc,ship:ship,total:sub-disc+ship,coupon:cp};}
  function paint(t){var f=function(id,v){var el=$('#'+id); if(el) el.textContent=v;}; f('sub',money(t.sub)); f('disc',t.disc?'−'+money(t.disc):'—'); f('shipc',t.ship?money(t.ship):'Free'); f('tot',money(t.total));}
  var cart=$('#cart'); if(cart){function rc(){var t=totals(); cart.innerHTML=t.items.length?t.items.map(function(it){return '<div class="line"><img src="'+it.p.img+'" alt=""><div><b>'+it.p.name+'</b><small>'+money(it.p.price)+'</small></div><div class="qty"><button data-d="-1" data-id="'+it.p.id+'">−</button><span>'+it.q+'</span><button data-d="1" data-id="'+it.p.id+'">+</button></div><button class="rm" data-id="'+it.p.id+'">Remove</button></div>';}).join(''):'<div class="empty">Your cart is empty. <a href="shop.html" style="color:var(--gold);font-weight:800">Shop</a></div>';
      $$('.qty button',cart).forEach(function(b){b.onclick=function(){var c=g(K.cart,{}); c[b.dataset.id]=Math.max(0,(c[b.dataset.id]||0)+parseInt(b.dataset.d,10)); if(!c[b.dataset.id]) delete c[b.dataset.id]; s(K.cart,c); counts(); rc();};});
      $$('.rm',cart).forEach(function(b){b.onclick=function(){var c=g(K.cart,{}); delete c[b.dataset.id]; s(K.cart,c); counts(); rc();};}); paint(t); var co=$('#checkout-btn'); if(co) co.disabled=!t.items.length;}
    var cb=$('#apply'); if(cb) cb.onclick=function(){var v=$('#code').value.trim().toUpperCase(); if(v==='WELCOME10'){s(K.coupon,v); toast('10% off applied');} else {s(K.coupon,null); toast('Code not recognised');} rc();}; rc();}
  // checkout
  var ck2=$('#checkout'); if(ck2){var t=totals(); if(!t.items.length){ck2.innerHTML='<div class="empty">Your cart is empty. <a href="shop.html" style="color:var(--gold);font-weight:800">Shop</a></div>';}
    else {paint(t); $('#items').innerHTML=t.items.map(function(it){return '<div class="r"><span>'+it.p.name+' × '+it.q+'</span><span>'+money(it.p.price*it.q)+'</span></div>';}).join('');
      var pay='card'; $$('.pay-tabs button').forEach(function(b){b.onclick=function(){pay=b.dataset.p; $$('.pay-tabs button').forEach(function(x){x.classList.toggle('on',x===b);}); $('#cardui').style.display=pay==='card'?'block':'none'; $('#paypalui').style.display=pay==='paypal'?'block':'none';};});
      var cn=$('#cardnum'); if(cn) cn.oninput=function(){cn.value=cn.value.replace(/\D/g,'').slice(0,16).replace(/(\d{4})(?=\d)/g,'$1 ');};
      var ex=$('#exp'); if(ex) ex.oninput=function(){ex.value=ex.value.replace(/\D/g,'').slice(0,4).replace(/(\d{2})(?=\d)/,'$1/');};
      $('#payform').onsubmit=function(e){e.preventDefault(); var f=e.target, v=function(n){return (f.querySelector('[name='+n+']')||{}).value||'';};
        if(pay==='card'&&(cn.value.replace(/\s/g,'').length<16||ex.value.length<5||$('#cvc').value.length<3)){toast('Check the card details'); return;}
        var btn=$('#paybtn'); btn.disabled=true; btn.textContent=pay==='card'?'Processing…':'Redirecting to PayPal…';
        setTimeout(function(){var num='MC-'+new Date().getFullYear()+'-'+String(Math.floor(1000+Math.random()*9000)); var orders=g(K.orders,[]); orders.unshift({num:num,date:new Date().toISOString().slice(0,10),total:t.total,items:t.items.map(function(i){return i.p.name+' × '+i.q;}),name:v('name'),pay:pay==='card'?'Card •••• '+cn.value.slice(-4):'PayPal'}); s(K.orders,orders); s(K.cart,{}); s(K.coupon,null); if(!g(K.user,null)) s(K.user,{name:v('name'),email:v('email')}); counts();
          ck2.innerHTML='<div class="done"><div class="big">✓</div><h2>Order confirmed</h2><p>Order <b>'+num+'</b> · '+money(t.total)+' · '+(pay==='card'?'paid by card':'paid with PayPal')+'<br>A confirmation email goes to '+v('email')+'. Ships in 1–2 working days.</p><div class="demo-note">Demo mode — no money moved. In the live build this step runs on Stripe or PayPal with real receipts.</div><div class="cta-row"><a class="btn" href="account.html">View order history</a><a class="btn line" href="shop.html">Continue shopping</a></div></div>'; window.scrollTo(0,0);},1400);};}}
  // account
  var ac=$('#account'); if(ac){function ra(){var u=g(K.user,null), o=g(K.orders,[]); $('#acc-form').style.display=u?'none':'block'; $('#acc-in').style.display=u?'block':'none'; if(u){$('#acc-name').textContent=u.name||u.email; $('#orders').innerHTML=o.length?o.map(function(x){return '<div class="o"><b>'+x.num+' · '+money(x.total)+'</b><span>'+x.date+' · '+x.pay+'</span><div>'+x.items.join(', ')+'</div></div>';}).join(''):'<div class="empty">No orders yet.</div>';}}
    $('#acc-form').onsubmit=function(e){e.preventDefault(); var f=e.target; s(K.user,{name:f.name.value||f.email.value.split('@')[0],email:f.email.value}); toast('Signed in (demo)'); ra();}; var so=$('#signout'); if(so) so.onclick=function(){s(K.user,null); ra();}; ra();}
  // wishlist page section
  var wl=$('#wishlist'); if(wl){var w=g(K.wish,[]); wl.innerHTML=w.length?P.filter(function(p){return w.indexOf(p.id)>=0;}).map(card).join(''):'<div class="empty">Nothing saved yet. Tap ♡ on any product.</div>'; bind(wl);}
  // newsletter + contact forms (demo)
  $$('form.demo').forEach(function(f){f.onsubmit=function(e){e.preventDefault(); toast('Thanks — this is a demo, nothing was sent.'); f.reset();};});
  counts();
})();
'''

HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css"></head><body>
<div class="ship">Free delivery over $60 · Ships in 1–2 working days · Use code WELCOME10 for 10% off your first order</div>
<header><div class="wrap"><nav>
  <a class="logo" href="index.html">Maison <b>Cacao</b></a>
  <div class="menu" id="menu"><a href="index.html" class="{a_index}">Home</a><a href="shop.html" class="{a_shop}">Shop</a><a href="about.html" class="{a_about}">About</a><a href="contact.html" class="{a_contact}">Contact</a><a href="policies.html" class="{a_policies}">Policies</a></div>
  <div class="right"><a class="icon" href="account.html"><span class="t">Account</span> ♥ <i class="wishn">0</i></a><a class="icon" href="cart.html"><span class="t">Cart</span> <i class="cartn">0</i></a><button class="burger" id="burger" aria-label="menu">☰</button></div>
</nav></div></header>
'''
FOOT = '''<footer><div class="wrap">
  <div><b>Maison Cacao</b>Chocolatier in the Sablon, Brussels, since 2009. Pralines, truffles, tablets and pastries, made in our own atelier.</div>
  <div><b>Shop</b><a href="shop.html#pralines">Pralines</a><a href="shop.html#truffles">Truffles</a><a href="shop.html#bars">Tablets</a><a href="shop.html#gifts">Gifts</a></div>
  <div><b>Help</b><a href="policies.html#shipping">Shipping</a><a href="policies.html#returns">Returns</a><a href="policies.html#privacy">Privacy</a><a href="contact.html">Contact</a></div>
  <div><b>Visit</b>Rue au Beurre 12, 1000 Brussels<br>Mon–Sat 10:00–19:00<br>+1 (555) 010-0199<br>hello@maisoncacao.be</div>
  <div class="demo">Portfolio demo — Maison Cacao is a fictional business. Payments are simulated; the live build runs on Stripe or PayPal. A store like this, with payment gateway and 40 products loaded: $700, delivered in 14 days.</div>
</div></footer>
<div class="cookie" id="cookie"><span>We use cookies for the cart and basic analytics. No tracking across sites.</span><span class="b"><button class="btn line" data-c="essential" style="padding:9px 14px">Essential only</button><button class="btn" data-c="all" style="padding:9px 14px">Accept</button></span></div>
<div class="toast" id="toast"></div>
<a class="wa" href="https://wa.me/15550100199" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.1.6 2.8.5a2.4 2.4 0 0 0 1.6-1.1 2 2 0 0 0 .1-1.1c0-.1-.2-.2-.5-.3z"/></svg></a>
<script src="app.js"></script></body></html>
'''
cats_html = "".join(f'<button data-cat="{k}">{v}</button>' for k, v in CATS)
PAGES = {
"index": ("Maison Cacao — Chocolatier, Brussels", "Pralines, truffles, tablets and pastries from our Brussels atelier. Ships in 1–2 days.", f'''
<section class="hero" style="padding:0"><img src="{IMG['box']}" alt=""><div class="wrap"><span class="eyebrow">Sablon, Brussels · since 2009</span><h1>Chocolate the way Brussels still makes it.</h1><p>Pralines, truffles and tablets from our own atelier — boxed the morning they are made and at your door in two days.</p><div class="cta-row"><a class="btn gold" href="shop.html">Shop the range</a><a class="btn line" href="shop.html#gifts" style="border-color:#fff;color:#fff">Gifts &amp; corporate</a></div></div></section>
<section><div class="wrap"><div class="sec-h"><h2>Signatures &amp; new arrivals</h2><a href="shop.html" style="color:var(--gold);font-weight:700">All 40 products →</a></div><div class="grid" id="featured"></div></div></section>
<section style="padding-top:0"><div class="wrap usp"><div><b>Ships in 1–2 days</b><span>Cold-packed in summer. Tracked, always.</span></div><div><b>Secure checkout</b><span>Card or PayPal. We never see your card number.</span></div><div><b>14-day returns</b><span>Unopened goods, no questions.</span></div><div><b>Made in Brussels</b><span>Our atelier, our recipes, our people.</span></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="news"><div><h2>10% off your first order</h2><p>Join the list — one email a month, never more.</p></div><form class="demo"><input type="email" placeholder="you@email.com" required><button class="btn gold" type="submit">Join</button></form></div></div></section>
'''),
"shop": ("Shop — Maison Cacao", "All 40 products: pralines, truffles, tablets, pastries, gifts and pantry.", f'''
<section><div class="wrap"><div class="sec-h"><h2>Shop</h2><p id="count"></p></div>
<div class="toolbar"><input id="q" placeholder="Search — hazelnut, gift, tablet…"><select id="sort"><option value="featured">Featured</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option><option value="name">Name A–Z</option></select><a class="btn line" href="account.html#wishlist">♥ Wishlist</a></div>
<div class="cats">{cats_html}</div><div class="grid" id="products"></div></div></section>
'''),
"product": ("Product — Maison Cacao", "Product details.", '''
<section><div class="wrap"><div class="pd" id="pd"></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-h"><h2>You may also like</h2></div><div class="grid" id="related"></div></div></section>
'''),
"cart": ("Your cart — Maison Cacao", "Cart.", '''
<section><div class="wrap"><div class="sec-h"><h2>Your cart</h2></div><div class="cart"><div id="cart"></div><div class="sum"><div class="r"><span>Subtotal</span><span id="sub">$0</span></div><div class="r"><span>Discount</span><span id="disc">—</span></div><div class="r"><span>Delivery (free over $60)</span><span id="shipc">—</span></div><div class="r t"><span>Total</span><span id="tot">$0</span></div><div class="coupon"><input id="code" placeholder="Coupon code — try WELCOME10"><button class="btn line" id="apply" style="padding:10px 14px">Apply</button></div><a class="btn w" id="checkout-btn" href="checkout.html">Checkout</a><p class="secure"><b>🔒 Secure</b> · card or PayPal · 14-day returns</p></div></div></div></section>
'''),
"checkout": ("Checkout — Maison Cacao", "Secure checkout.", '''
<section><div class="wrap"><div class="sec-h"><h2>Checkout</h2></div><div id="checkout"><div class="chk"><form id="payform"><div class="step"><h3>1 · Contact &amp; delivery</h3><div class="two"><div><label>Full name</label><input name="name" required></div><div><label>Email</label><input name="email" type="email" required></div></div><label>Address</label><input name="address" required placeholder="Street and number"><div class="two"><div><label>City</label><input name="city" required></div><div><label>Postcode</label><input name="zip" required></div></div><label>Country</label><select name="country"><option>Belgium</option><option>Netherlands</option><option>France</option><option>Germany</option><option>United Kingdom</option><option>United States</option></select></div>
<div class="step"><h3>2 · Payment</h3><div class="pay-tabs"><button type="button" class="on" data-p="card">💳 Card</button><button type="button" data-p="paypal">PayPal</button></div><div class="card-ui" id="cardui"><label>Card number</label><input id="cardnum" placeholder="4242 4242 4242 4242" inputmode="numeric"><div class="two"><div><label>Expiry</label><input id="exp" placeholder="MM/YY" inputmode="numeric"></div><div><label>CVC</label><input id="cvc" placeholder="123" inputmode="numeric" maxlength="4"></div></div><p class="secure"><b>🔒 Encrypted</b> · powered by Stripe in the live build · card data never touches our server</p></div><div class="card-ui" id="paypalui" style="display:none"><p style="font-size:14px;color:var(--mute)">You'll be redirected to PayPal to approve the payment, then returned here.</p></div><div class="demo-note">Demo mode: use any 16 digits, any future date, any CVC. No money moves.</div><button class="btn gold w" id="paybtn" type="submit" style="margin-top:14px">Pay now</button></div></form>
<div class="sum"><h3 style="font-size:20px;margin-bottom:8px">Order summary</h3><div id="items"></div><div class="r"><span>Subtotal</span><span id="sub">$0</span></div><div class="r"><span>Discount</span><span id="disc">—</span></div><div class="r"><span>Delivery</span><span id="shipc">—</span></div><div class="r t"><span>Total</span><span id="tot">$0</span></div></div></div></div></div></section>
'''),
"account": ("Account — Maison Cacao", "Your account and orders.", '''
<section><div class="wrap"><div class="sec-h"><h2>Account</h2></div><div id="account" class="acct"><div><form id="acc-form" class="step"><h3>Sign in</h3><p style="color:var(--mute);font-size:14px">Demo sign-in — any email works, nothing is stored outside your browser.</p><label>Name</label><input name="name"><label>Email</label><input name="email" type="email" required><button class="btn w" type="submit" style="margin-top:14px">Sign in</button></form><div id="acc-in" class="step" style="display:none"><h3>Hello, <span id="acc-name"></span></h3><p style="color:var(--mute);font-size:14px">Your orders and saved items are below.</p><button class="btn line" id="signout" style="margin-top:12px">Sign out</button></div></div><div><div class="step orders"><h3>Order history</h3><div id="orders"></div></div></div></div></div></section>
<section style="padding-top:0" id="wishlist-sec"><div class="wrap"><div class="sec-h" id="wishlist-h"><h2 id="wishlist">Wishlist</h2></div><div class="grid" id="wishlist"></div></div></section>
'''),
"about": ("About — Maison Cacao", "Our atelier in the Sablon, Brussels, since 2009.", f'''
<section><div class="wrap split"><img src="{IMG['cake']}" alt=""><div><span class="eyebrow">Our story</span><h2>A Sablon window that turned into an atelier.</h2><p>Maison Cacao began in 2009 as a single window on Rue au Beurre, selling pralines made in the back room by two people. Today the atelier employs eleven, ships across Europe, and still tempers every batch by hand.</p><p>We buy cocoa directly from three cooperatives in Ecuador and Ghana, pay above Fairtrade minimums, and print the origin on every box.</p><div class="cta-row" style="justify-content:flex-start"><a class="btn" href="shop.html">Shop the range</a></div></div></div></section>
<section style="padding-top:0"><div class="wrap usp"><div><b>2009</b><span>founded in the Sablon</span></div><div><b>11</b><span>chocolatiers and bakers</span></div><div><b>3</b><span>direct-trade origins</span></div><div><b>4.9★</b><span>from 2,400 reviews</span></div></div></section>
'''),
"contact": ("Contact — Maison Cacao", "Visit, call or write.", '''
<section><div class="wrap"><div class="sec-h"><h2>Contact</h2></div><div class="contact"><form class="demo step"><label>Name</label><input required><label>Email</label><input type="email" required><label>Subject</label><select><option>Order question</option><option>Corporate order</option><option>Wholesale</option><option>Other</option></select><label>Message</label><textarea rows="5"></textarea><button class="btn w" type="submit" style="margin-top:14px">Send</button></form><div class="info"><div><b>Boutique &amp; atelier</b>Rue au Beurre 12, 1000 Brussels</div><div><b>Hours</b>Monday to Saturday 10:00–19:00</div><div><b>Phone / WhatsApp</b>+1 (555) 010-0199</div><div><b>Email</b>hello@maisoncacao.be</div><iframe class="map" loading="lazy" src="https://www.google.com/maps?q=Rue+au+Beurre+12+Brussels&output=embed"></iframe></div></div></div></section>
'''),
"policies": ("Policies — Maison Cacao", "Shipping, returns, privacy and terms.", '''
<section><div class="wrap pol" style="max-width:820px"><h1 style="font-size:40px">Policies</h1>
<h2 id="shipping">Shipping</h2><p>Orders placed before 14:00 CET ship the same working day. Belgium 1 day, EU 2–3 days, UK and US 3–5 days. Free delivery on orders over $60; otherwise $6. Summer orders are cold-packed at no charge.</p>
<h2 id="returns">Returns</h2><p>Unopened goods may be returned within 14 days of delivery for a full refund. Made-to-order pastries and personalised gifts are excluded. Damaged in transit? Send a photo within 48 hours and we replace it.</p>
<h2 id="privacy">Privacy</h2><p>We store your name, address and order history to fulfil orders and, if you opt in, to send one newsletter a month. Card details are processed by Stripe or PayPal and never stored by us. You can request deletion at any time at hello@maisoncacao.be.</p>
<h2 id="cookies">Cookies</h2><p>Essential cookies run the cart and checkout. Analytics cookies are set only if you accept them in the banner.</p>
<h2 id="terms">Terms</h2><ul><li>Prices include VAT where applicable.</li><li>Allergens: all products are made in an atelier that handles nuts, milk, gluten, soy and eggs.</li><li>Corporate and wedding orders require 48 hours' notice and a 50% deposit.</li></ul>
</div></section>
'''),
}
for name, (title, desc, body) in PAGES.items():
    act = {k: ("active" if k == name else "") for k in ["index", "shop", "about", "contact", "policies"]}
    (out / f"{name}.html").write_text(HEAD.format(title=title, desc=desc, a_index=act["index"], a_shop=act["shop"], a_about=act["about"], a_contact=act["contact"], a_policies=act["policies"]) + body + FOOT, encoding="utf-8")
(out / "styles.css").write_text(CSS, encoding="utf-8")
(out / "app.js").write_text(JS.replace("__PRODUCTS__", json.dumps(P, ensure_ascii=False)).replace("__CATS__", json.dumps(CATS)), encoding="utf-8")
print("estore built:", len(P), "products,", len(PAGES), "pages")

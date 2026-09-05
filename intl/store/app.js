// Dukkan Sweets — portfolio demo. Products, cart (localStorage), WhatsApp checkout. No backend.
(function(){
  var WA='15550100199', KEY='dukkan_cart';
  var U=function(id){return 'https://images.unsplash.com/photo-'+id+'?w=800&h=800&fit=crop&q=75';};
  var P=[
    {id:'drip-cake',cat:'cakes',en:'Fraisier — 1.5 kg',den:'Génoise, strawberries, crème mousseline. Serves 12.',price:60,img:U('1616690710400-a16d146927c5'),badge:'BEST SELLER'},
    {id:'choc-cake',cat:'cakes',en:'Gâteau au Chocolat',den:'Three layers, dark ganache, piped rosettes. Serves 10.',price:40,img:U('1578985545062-69928b1d9587')},
    {id:'choc-box',cat:'chocolate',en:'Praliné Box (16)',den:'Hazelnut, saffron, sea salt and rose pralines.',price:35,img:U('1481391319762-47dff72954d9'),badge:'GIFT'},
    {id:'cookies',cat:'baked',en:'Sablés au Chocolat (12)',den:'Baked every morning. Crisp edge, soft centre.',price:12,img:U('1558961363-fa8fdf82db35')},
    {id:'cupcakes',cat:'baked',en:'Cupcakes de Fête (6)',den:'Vanilla and chocolate, your colours on request.',price:18,img:U('1599785209707-a456fc1337bb')},
    {id:'donuts',cat:'baked',en:'Beignets Glacés (6)',den:'Chocolate, vanilla and sprinkles. Kids’ favourite.',price:15,img:U('1551024601-bec78aea704b')},
    {id:'crepes',cat:'baked',en:'Crêpes aux Fraises (4)',den:'Fresh cream and strawberries, made to order.',price:18,img:U('1587314168485-3236d6710814')},
    {id:'tiramisu',cat:'baked',en:'Tiramisu (4 parts)',den:'Coffee-soaked, mascarpone, cocoa. Alcohol-free.',price:20,img:U('1571115177098-24ec42ed204d')},
    {id:'corporate-hamper',cat:'gifts',en:'Coffret Entreprise',den:'Chocolate box, cookies and cupcakes, your logo on the card.',price:70,img:U('1607478900766-efe13248b125'),badge:'CORPORATE'}
  ];
  var body=document.body, ar=function(){return body.classList.contains('ar');};
  var saved=null; try{saved=localStorage.getItem('lang');}catch(e){} if(saved==='ar') body.classList.add('ar');
  function label(){var b=document.getElementById('lang'); if(b) b.textContent=ar()?'EN':'';} label();
  var lb=document.getElementById('lang'); if(lb) lb.addEventListener('click',function(){body.classList.toggle('ar'); try{localStorage.setItem('lang',ar()?'ar':'en');}catch(e){} label(); render();});
  var bg=document.getElementById('burger'), m=document.getElementById('menu'); if(bg&&m) bg.addEventListener('click',function(){m.classList.toggle('open');});
  function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){return {};}}
  function save(c){try{localStorage.setItem(KEY,JSON.stringify(c));}catch(e){} count();}
  function count(){var c=load(),n=0; for(var k in c) n+=c[k]; document.querySelectorAll('.cartbtn i').forEach(function(el){el.textContent=n;});}
  function toast(t){var el=document.getElementById('toast'); if(!el) return; el.textContent=t; el.classList.add('show'); setTimeout(function(){el.classList.remove('show');},1400);}
  function add(id){var c=load(); c[id]=(c[id]||0)+1; save(c); toast(ar()?'':'Added to cart');}
  var filter='all';
  function render(){
    var grid=document.getElementById('products'); if(grid){
      grid.innerHTML=P.filter(function(p){return filter==='all'||p.cat===filter;}).map(function(p){return '<div class="p">'+(p.badge?'<span class="badge">'+p.badge+'</span>':'')+'<img src="'+p.img+'" alt=""><div class="b"><h3>'+(ar()?p.ar:p.en)+'</h3><div class="d">'+(ar()?p.dar:p.den)+'</div><div class="pr"><b>$'+p.price+'</b><button class="add" data-id="'+p.id+'">'+(ar()?'':'Add')+'</button></div></div></div>';}).join('');
      grid.querySelectorAll('.add').forEach(function(b){b.addEventListener('click',function(){add(b.dataset.id); b.classList.add('done'); b.textContent=ar()?'':'Added ✓'; setTimeout(function(){b.classList.remove('done'); b.textContent=ar()?'':'Add';},1200);});});
    }
    var cart=document.getElementById('cart'); if(cart){
      var c=load(), ids=Object.keys(c), sub=0;
      if(!ids.length){cart.innerHTML='<div class="empty">'+(ar()?'':'Your cart is empty.')+' <a href="index.html" style="color:var(--gold);font-weight:800">'+(ar()?'':'Shop')+'</a></div>';}
      else cart.innerHTML=ids.map(function(id){var p=P.find(function(x){return x.id===id;}); if(!p) return ''; sub+=p.price*c[id]; return '<div class="line"><img src="'+p.img+'" alt=""><div><b>'+(ar()?p.ar:p.en)+'</b><small>$'+p.price+'</small></div><div class="qty"><button data-d="-1" data-id="'+id+'">−</button><span>'+c[id]+'</span><button data-d="1" data-id="'+id+'">+</button></div><button class="rm" data-id="'+id+'">'+(ar()?'':'Remove')+'</button></div>';}).join('');
      cart.querySelectorAll('.qty button').forEach(function(b){b.addEventListener('click',function(){var c=load(); c[b.dataset.id]=Math.max(0,(c[b.dataset.id]||0)+parseInt(b.dataset.d,10)); if(!c[b.dataset.id]) delete c[b.dataset.id]; save(c); render();});});
      cart.querySelectorAll('.rm').forEach(function(b){b.addEventListener('click',function(){var c=load(); delete c[b.dataset.id]; save(c); render();});});
      var del=sub>=40||sub===0?0:5, tot=sub+del;
      var s=function(id,v){var el=document.getElementById(id); if(el) el.textContent=v;};
      s('sub','$'+sub); s('del',del?'$'+del:(ar()?'':'Free')); s('tot','$'+tot);
      var f=document.getElementById('checkout'); if(f){f.onsubmit=function(e){e.preventDefault(); if(!ids.length) return; var v=function(n){var el=f.querySelector('[name='+n+']'); return el?el.value.trim():'';};
        var lines=ids.map(function(id){var p=P.find(function(x){return x.id===id;}); return '• '+p.en+' × '+c[id]+' = $'+(p.price*c[id]);}).join('\n');
        var msg='New order — Pâtisserie Lumière\n'+lines+'\nDelivery: '+(del?'$5':'Free')+'\nTOTAL: $'+tot+'\n\nName: '+v('name')+'\nArea: '+v('area')+'\nAddress: '+v('address')+'\nWhen: '+v('when')+'\nPayment: '+v('pay');
        window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank');};}
    }
  }
  document.querySelectorAll('.cats button').forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.cat; document.querySelectorAll('.cats button').forEach(function(x){x.classList.toggle('on',x===b);}); render();});});
  count(); render();
})();

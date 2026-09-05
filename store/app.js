// Dukkan Sweets — demo store by Ignitro. Products, cart (localStorage), WhatsApp checkout. No backend.
(function(){
  var WA='97460027117', KEY='dukkan_cart';
  var U=function(id){return 'https://images.unsplash.com/photo-'+id+'?w=800&h=800&fit=crop&q=75';};
  var P=[
    {id:'dates-khalas',cat:'dates',en:'Khalas Dates — Premium Box',ar:'تمر خلاص — علبة فاخرة',den:'Soft, caramel-sweet Saudi Khalas. 1 kg gift box.',dar:'خلاص سعودي طري بطعم الكراميل. علبة هدية ١ كجم.',price:85,img:U('1587241321921-91a834d6d191'),badge:'BEST SELLER'},
    {id:'dates-stuffed',cat:'dates',en:'Stuffed Dates — Almond & Pistachio',ar:'تمر محشو — لوز وفستق',den:'24 pieces, hand-filled daily.',dar:'٢٤ حبة، تُحشى يدويًا يوميًا.',price:95,img:U('1481391319762-47dff72954d9')},
    {id:'choc-box',cat:'chocolate',en:'Assorted Chocolate Box',ar:'علبة شوكولاتة مشكّلة',den:'16 pralines: hazelnut, saffron, sea salt, rose.',dar:'١٦ قطعة برالين: بندق، زعفران، ملح بحري، ورد.',price:120,img:U('1481391319762-47dff72954d9'),badge:'GIFT'},
    {id:'cookies',cat:'baked',en:'Chocolate Chip Cookies (12)',ar:'كوكيز بالشوكولاتة (١٢)',den:'Baked every morning. Crisp edge, soft centre.',dar:'تُخبز كل صباح. حواف مقرمشة وقلب طري.',price:45,img:U('1558961363-fa8fdf82db35')},
    {id:'cupcakes',cat:'baked',en:'Celebration Cupcakes (6)',ar:'كب كيك احتفالي (٦)',den:'Vanilla and chocolate, your colours on request.',dar:'فانيليا وشوكولاتة، بألوانك عند الطلب.',price:60,img:U('1607478900766-efe13248b125')},
    {id:'tiramisu',cat:'baked',en:'Tiramisu Slice Box (4)',ar:'علبة تيراميسو (٤ قطع)',den:'Coffee-soaked, mascarpone, cocoa. Alcohol-free.',dar:'مشبع بالقهوة مع ماسكربوني وكاكاو. خالٍ من الكحول.',price:70,img:U('1571115177098-24ec42ed204d')},
    {id:'bakery-tray',cat:'baked',en:'Majlis Tray — Mixed Pastries',ar:'صينية المجلس — معجنات مشكّلة',den:'40 pieces for gatherings. Order a day ahead.',dar:'٤٠ قطعة للمناسبات. يُطلب قبل يوم.',price:180,img:U('1593288942460-e321b92a6cde')},
    {id:'ramadan-hamper',cat:'gifts',en:'Corporate Gift Hamper',ar:'سلة هدايا للشركات',den:'Dates, chocolate, cookies, your logo on the card.',dar:'تمر وشوكولاتة وكوكيز مع شعاركم على البطاقة.',price:250,img:U('1587241321921-91a834d6d191'),badge:'CORPORATE'}
  ];
  var body=document.body, ar=function(){return body.classList.contains('ar');};
  var saved=null; try{saved=localStorage.getItem('lang');}catch(e){} if(saved==='ar') body.classList.add('ar');
  function label(){var b=document.getElementById('lang'); if(b) b.textContent=ar()?'EN':'عربي';} label();
  var lb=document.getElementById('lang'); if(lb) lb.addEventListener('click',function(){body.classList.toggle('ar'); try{localStorage.setItem('lang',ar()?'ar':'en');}catch(e){} label(); render();});
  var bg=document.getElementById('burger'), m=document.getElementById('menu'); if(bg&&m) bg.addEventListener('click',function(){m.classList.toggle('open');});
  function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){return {};}}
  function save(c){try{localStorage.setItem(KEY,JSON.stringify(c));}catch(e){} count();}
  function count(){var c=load(),n=0; for(var k in c) n+=c[k]; document.querySelectorAll('.cartbtn i').forEach(function(el){el.textContent=n;});}
  function toast(t){var el=document.getElementById('toast'); if(!el) return; el.textContent=t; el.classList.add('show'); setTimeout(function(){el.classList.remove('show');},1400);}
  function add(id){var c=load(); c[id]=(c[id]||0)+1; save(c); toast(ar()?'أُضيف إلى السلة':'Added to cart');}
  var filter='all';
  function render(){
    var grid=document.getElementById('products'); if(grid){
      grid.innerHTML=P.filter(function(p){return filter==='all'||p.cat===filter;}).map(function(p){return '<div class="p">'+(p.badge?'<span class="badge">'+p.badge+'</span>':'')+'<img src="'+p.img+'" alt=""><div class="b"><h3>'+(ar()?p.ar:p.en)+'</h3><div class="d">'+(ar()?p.dar:p.den)+'</div><div class="pr"><b>QAR '+p.price+'</b><button class="add" data-id="'+p.id+'">'+(ar()?'أضف':'Add')+'</button></div></div></div>';}).join('');
      grid.querySelectorAll('.add').forEach(function(b){b.addEventListener('click',function(){add(b.dataset.id); b.classList.add('done'); b.textContent=ar()?'تمت الإضافة ✓':'Added ✓'; setTimeout(function(){b.classList.remove('done'); b.textContent=ar()?'أضف':'Add';},1200);});});
    }
    var cart=document.getElementById('cart'); if(cart){
      var c=load(), ids=Object.keys(c), sub=0;
      if(!ids.length){cart.innerHTML='<div class="empty">'+(ar()?'سلتك فارغة.':'Your cart is empty.')+' <a href="index.html" style="color:var(--gold);font-weight:800">'+(ar()?'تسوّق':'Shop')+'</a></div>';}
      else cart.innerHTML=ids.map(function(id){var p=P.find(function(x){return x.id===id;}); if(!p) return ''; sub+=p.price*c[id]; return '<div class="line"><img src="'+p.img+'" alt=""><div><b>'+(ar()?p.ar:p.en)+'</b><small>QAR '+p.price+'</small></div><div class="qty"><button data-d="-1" data-id="'+id+'">−</button><span>'+c[id]+'</span><button data-d="1" data-id="'+id+'">+</button></div><button class="rm" data-id="'+id+'">'+(ar()?'حذف':'Remove')+'</button></div>';}).join('');
      cart.querySelectorAll('.qty button').forEach(function(b){b.addEventListener('click',function(){var c=load(); c[b.dataset.id]=Math.max(0,(c[b.dataset.id]||0)+parseInt(b.dataset.d,10)); if(!c[b.dataset.id]) delete c[b.dataset.id]; save(c); render();});});
      cart.querySelectorAll('.rm').forEach(function(b){b.addEventListener('click',function(){var c=load(); delete c[b.dataset.id]; save(c); render();});});
      var del=sub>=150||sub===0?0:15, tot=sub+del;
      var s=function(id,v){var el=document.getElementById(id); if(el) el.textContent=v;};
      s('sub','QAR '+sub); s('del',del?'QAR '+del:(ar()?'مجانًا':'Free')); s('tot','QAR '+tot);
      var f=document.getElementById('checkout'); if(f){f.onsubmit=function(e){e.preventDefault(); if(!ids.length) return; var v=function(n){var el=f.querySelector('[name='+n+']'); return el?el.value.trim():'';};
        var lines=ids.map(function(id){var p=P.find(function(x){return x.id===id;}); return '• '+p.en+' × '+c[id]+' = QAR '+(p.price*c[id]);}).join('\n');
        var msg='New order — Dukkan Sweets\n'+lines+'\nDelivery: '+(del?'QAR 15':'Free')+'\nTOTAL: QAR '+tot+'\n\nName: '+v('name')+'\nArea: '+v('area')+'\nAddress: '+v('address')+'\nWhen: '+v('when')+'\nPayment: '+v('pay');
        window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank');};}
    }
  }
  document.querySelectorAll('.cats button').forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.cat; document.querySelectorAll('.cats button').forEach(function(x){x.classList.toggle('on',x===b);}); render();});});
  count(); render();
})();

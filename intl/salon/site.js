// Élise Beauty Studio — portfolio demo. Language toggle + mobile nav + WhatsApp form.
(function(){
  var WA='15550100199'; // demo number — replaced with the client's on delivery
  var body=document.body, saved=null;
  try{saved=localStorage.getItem('lang');}catch(e){}
  if(saved==='ar') body.classList.add('ar');
  function label(){var b=document.getElementById('lang'); if(b) b.textContent=body.classList.contains('ar')?'EN':'';}
  label();
  var lb=document.getElementById('lang'); if(lb) lb.addEventListener('click',function(){body.classList.toggle('ar'); try{localStorage.setItem('lang',body.classList.contains('ar')?'ar':'en');}catch(e){} label();});
  var bg=document.getElementById('burger'), m=document.getElementById('menu'); if(bg&&m) bg.addEventListener('click',function(){m.classList.toggle('open');});
  var f=document.getElementById('book'); if(f) f.addEventListener('submit',function(e){
    e.preventDefault(); var v=function(n){var el=f.querySelector('[name='+n+']'); return el?el.value.trim():'';};
    var msg='Booking request — Élise Beauty Studio\nName: '+v('name')+'\nService: '+v('service')+'\nPreferred day/time: '+v('when')+'\nNotes: '+v('notes');
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank');
  });
})();

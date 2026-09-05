// Al Reem Contracting — demo by Ignitro. Language toggle + mobile nav + WhatsApp quote form.
(function(){
  var WA='97460027117';
  var body=document.body, saved=null; try{saved=localStorage.getItem('lang');}catch(e){}
  if(saved==='ar') body.classList.add('ar');
  function label(){var b=document.getElementById('lang'); if(b) b.textContent=body.classList.contains('ar')?'EN':'عربي';} label();
  var lb=document.getElementById('lang'); if(lb) lb.addEventListener('click',function(){body.classList.toggle('ar'); try{localStorage.setItem('lang',body.classList.contains('ar')?'ar':'en');}catch(e){} label();});
  var bg=document.getElementById('burger'), m=document.getElementById('menu'); if(bg&&m) bg.addEventListener('click',function(){m.classList.toggle('open');});
  var f=document.getElementById('quote'); if(f) f.addEventListener('submit',function(e){
    e.preventDefault(); var v=function(n){var el=f.querySelector('[name='+n+']'); return el?el.value.trim():'';};
    var msg='Quote request — Al Reem Contracting\nName: '+v('name')+'\nCompany: '+v('company')+'\nService: '+v('service')+'\nLocation: '+v('location')+'\nDetails: '+v('details');
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank');
  });
})();

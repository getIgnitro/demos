/* Ignitro — Website Brief. Multi-step form, autosave, Supabase intake + Storage uploads, WhatsApp handoff. */
(function () {
  var SB = 'https://wllbpwtjaqiyxvjvfekm.supabase.co';
  var KEY = 'sb_publishable_AcaTESSQ4nXGO_P2E0P4Ow_y9alVWro';
  var BUCKET = 'brief-uploads';
  var WA = '97460027117';
  var STORE = 'ignitro_brief_v1';

  var $ = function (q, el) { return (el || document).querySelector(q); };
  var $$ = function (q, el) { return Array.prototype.slice.call((el || document).querySelectorAll(q)); };
  var steps = $$('.step'), cur = 0, LAST = steps.length - 1, FORMLAST = LAST - 1;
  var uploads = { logo: [], photos: [], docs: [], cr: [] };

  /* ---------- language ---------- */
  var body = document.body;
  try { if (localStorage.getItem('lang') === 'ar') body.classList.add('ar'); } catch (e) {}
  function langLabel() { $('#lang').textContent = body.classList.contains('ar') ? 'EN' : 'عربي'; }
  langLabel();
  $('#lang').onclick = function () {
    body.classList.toggle('ar');
    try { localStorage.setItem('lang', body.classList.contains('ar') ? 'ar' : 'en'); } catch (e) {}
    langLabel();
  };

  /* ---------- services rows ---------- */
  function svcRow(v) {
    v = v || {};
    var d = document.createElement('div');
    d.className = 'svc';
    d.innerHTML = '<button type="button" class="del" aria-label="remove">×</button>' +
      '<div class="row"><input class="s-name" placeholder="' + (body.classList.contains('ar') ? 'اسم الخدمة أو المنتج' : 'Service or product name') + '" value="' + (v.name || '') + '">' +
      '<input class="s-price" placeholder="' + (body.classList.contains('ar') ? 'السعر (اختياري)' : 'Price (optional)') + '" value="' + (v.price || '') + '"></div>' +
      '<textarea class="s-desc" rows="2" placeholder="' + (body.classList.contains('ar') ? 'سطر وصف واحد' : 'One line of description') + '">' + (v.desc || '') + '</textarea>';
    d.querySelector('.del').onclick = function () { d.remove(); save(); };
    $$('input,textarea', d).forEach(function (i) { i.addEventListener('input', save); });
    return d;
  }
  $('#addsvc').onclick = function () { $('#services').appendChild(svcRow()); save(); };
  function services() {
    return $$('.svc').map(function (r) {
      return { name: $('.s-name', r).value.trim(), price: $('.s-price', r).value.trim(), desc: $('.s-desc', r).value.trim() };
    }).filter(function (s) { return s.name || s.desc; });
  }

  /* ---------- style chips ---------- */
  $$('#style span').forEach(function (c) {
    c.onclick = function () { c.classList.toggle('on'); save(); };
  });
  function chips() { return $$('#style span.on').map(function (c) { return c.dataset.v; }); }

  /* ---------- domain toggle ---------- */
  function domainToggle() {
    var v = ($('input[name=domain_state]:checked') || {}).value || '';
    var newOne = v.indexOf('register') >= 0;
    $('#new_domain').hidden = !newOne;
    $('#own_domain').hidden = newOne;
  }
  $$('input[name=domain_state]').forEach(function (r) { r.addEventListener('change', function () { domainToggle(); save(); }); });

  /* ---------- page count hint ---------- */
  var LIMITS = { Basic: 3, Starter: 5, Business: 12 };
  function pageHint() {
    var pkg = ($('input[name=package]:checked') || {}).value || '';
    var n = $$('input[name=pages]:checked').length;
    var lim = 0;
    Object.keys(LIMITS).forEach(function (k) { if (pkg.indexOf(k) === 0) lim = LIMITS[k]; });
    var box = $('#pagecount'); if (!box) return;
    var ar = body.classList.contains('ar');
    if (!lim) { box.textContent = n + (ar ? ' صفحات محددة' : ' pages selected'); box.className = 'note'; return; }
    if (n > lim) {
      box.className = 'note warn';
      box.textContent = ar
        ? 'اخترت ' + n + ' صفحات وباقتك تشمل ' + lim + '. لا مشكلة — سنؤكد التكلفة الإضافية (١٥٠ ر.ق للصفحة) قبل البدء.'
        : 'You picked ' + n + ' pages; your package covers ' + lim + '. That is fine — we will confirm the extra cost (QAR 150 per page) before starting.';
    } else {
      box.className = 'note';
      box.textContent = ar ? n + ' من ' + lim + ' صفحات' : n + ' of ' + lim + ' pages used';
    }
  }
  $$('input[name=pages]').forEach(function (c) { c.addEventListener('change', function () { pageHint(); save(); }); });
  $$('input[name=package]').forEach(function (r) { r.addEventListener('change', function () { pageHint(); save(); }); });

  /* ---------- autosave ---------- */
  function collect() {
    var d = {};
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.type === 'file') return;
      if (el.type === 'checkbox') { if (!d[el.name]) d[el.name] = []; if (el.checked) d[el.name].push(el.value || true); }
      else if (el.type === 'radio') { if (el.checked) d[el.name] = el.value; }
      else d[el.name] = el.value.trim();
    });
    d.services = services();
    d.style_words = chips();
    return d;
  }
  var savedTimer;
  function save() {
    try { localStorage.setItem(STORE, JSON.stringify({ d: collect(), step: cur })); } catch (e) {}
    var s = $('#saved'); s.classList.add('on');
    clearTimeout(savedTimer); savedTimer = setTimeout(function () { s.classList.remove('on'); }, 1200);
  }
  function restore() {
    var raw = null;
    try { raw = JSON.parse(localStorage.getItem(STORE)); } catch (e) {}
    if (!raw || !raw.d) { $('#services').appendChild(svcRow()); $('#services').appendChild(svcRow()); $('#services').appendChild(svcRow()); return; }
    var d = raw.d;
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.type === 'file') return;
      var v = d[el.name];
      if (el.type === 'checkbox') el.checked = Array.isArray(v) && v.indexOf(el.value) >= 0;
      else if (el.type === 'radio') el.checked = (v === el.value);
      else if (v != null) el.value = v;
    });
    (d.style_words || []).forEach(function (w) { var c = $('#style span[data-v="' + w + '"]'); if (c) c.classList.add('on'); });
    var svcs = d.services && d.services.length ? d.services : [{}, {}, {}];
    svcs.forEach(function (s) { $('#services').appendChild(svcRow(s)); });
    if (raw.step && raw.step > 0 && raw.step <= FORMLAST) go(raw.step);
  }

  /* ---------- steps ---------- */
  function go(n) {
    steps[cur].classList.remove('on');
    cur = Math.max(0, Math.min(n, LAST));
    steps[cur].classList.add('on');
    $('#bar').style.width = Math.round((cur / FORMLAST) * 100) + '%';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (cur === 2) pageHint();
    save();
  }
  function validate(i) {
    var ok = true, first = null;
    $$('.step[data-step="' + i + '"] [required]').forEach(function (el) {
      var bad = el.type === 'checkbox' ? !el.checked : !el.value.trim();
      el.classList.toggle('bad', bad);
      if (bad && !first) first = el;
      if (bad) ok = false;
    });
    if (!ok && first) { first.focus(); first.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
    return ok;
  }
  $$('.next').forEach(function (b) {
    b.onclick = function () {
      if (cur === 0 && !$('input[name=package]:checked')) { $$('.pkg')[0].scrollIntoView({ block: 'center' }); return; }
      if (!validate(cur)) return;
      go(cur + 1);
    };
  });
  $$('.back').forEach(function (b) { b.onclick = function () { go(cur - 1); }; });
  $$('input,select,textarea').forEach(function (el) { if (el.type !== 'file') el.addEventListener('input', save); });

  /* ---------- uploads ---------- */
  function fmt(b) { return b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.round(b / 1024) + ' KB'; }
  function slug(s) { return s.replace(/[^a-zA-Z0-9._-]/g, '_').slice(-70); }
  var SESSION = 'b' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

  function upload(file, kind, row) {
    var path = SESSION + '/' + kind + '/' + Date.now() + '_' + slug(file.name);
    var bar = row.querySelector('.prog2 i'), tag = row.querySelector('.s');
    return new Promise(function (resolve) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', SB + '/storage/v1/object/' + BUCKET + '/' + path, true);
      xhr.setRequestHeader('apikey', KEY);
      xhr.setRequestHeader('Authorization', 'Bearer ' + KEY);
      xhr.setRequestHeader('x-upsert', 'true');
      if (file.type) xhr.setRequestHeader('Content-Type', file.type);
      xhr.upload.onprogress = function (e) { if (e.lengthComputable && bar) bar.style.width = Math.round(e.loaded / e.total * 100) + '%'; };
      xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
          row.classList.add('up-ok'); tag.textContent = '✓';
          uploads[kind].push({ name: file.name, size: file.size, path: path });
          resolve(true);
        } else {
          row.classList.add('up-err'); tag.textContent = body.classList.contains('ar') ? 'فشل' : 'failed';
          uploads[kind].push({ name: file.name, size: file.size, path: null, failed: true });
          resolve(false);
        }
      };
      xhr.onerror = function () {
        row.classList.add('up-err'); tag.textContent = body.classList.contains('ar') ? 'فشل' : 'failed';
        uploads[kind].push({ name: file.name, size: file.size, path: null, failed: true });
        resolve(false);
      };
      xhr.send(file);
    });
  }

  function addFiles(zone, list) {
    var kind = zone.dataset.kind, box = $('.files', zone);
    Array.prototype.slice.call(list).forEach(function (file) {
      if (file.size > 25 * 1024 * 1024) {
        var w = document.createElement('div'); w.className = 'file up-err';
        w.innerHTML = '<span class="n">' + file.name + '</span><span class="s">' + (body.classList.contains('ar') ? 'أكبر من ٢٥ ميجا' : 'over 25 MB') + '</span>';
        box.appendChild(w); return;
      }
      var row = document.createElement('div'); row.className = 'file';
      row.innerHTML = '<span class="n">' + file.name + '</span><span class="prog2"><i></i></span><span class="s">…</span>';
      box.appendChild(row);
      upload(file, kind, row);
    });
  }
  $$('.up').forEach(function (zone) {
    var input = $('input[type=file]', zone);
    $('.pick', zone).onclick = function () { input.click(); };
    input.onchange = function () { addFiles(zone, input.files); input.value = ''; };
    ['dragenter', 'dragover'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('drag'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('drag'); }); });
    zone.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files.length) addFiles(zone, e.dataTransfer.files); });
  });

  /* ---------- summary + submit ---------- */
  function summary(d, ref) {
    var L = [];
    L.push('WEBSITE BRIEF — ' + (d.biz_en || 'New client'));
    L.push('Ref: ' + ref);
    L.push('Package: ' + (d.package || '—'));
    L.push('');
    L.push('BUSINESS');
    L.push('Name: ' + (d.biz_en || '') + (d.biz_ar ? ' / ' + d.biz_ar : ''));
    L.push('One line: ' + (d.tagline || ''));
    if (d.industry) L.push('Industry: ' + d.industry);
    if (d.est_year || d.team_size) L.push('Since ' + (d.est_year || '—') + ' · team ' + (d.team_size || '—'));
    L.push('Contact: ' + (d.contact_name || '') + ' · ' + (d.wa || '') + (d.phone ? ' · ' + d.phone : ''));
    L.push('Their email: ' + (d.email || ''));
    L.push('Address: ' + (d.address || ''));
    if (d.maps) L.push('Maps: ' + d.maps);
    if (d.hours) L.push('Hours: ' + d.hours);
    if (d.areas) L.push('Areas: ' + d.areas);
    var soc = ['instagram', 'facebook', 'tiktok', 'linkedin'].map(function (k) { return d[k] ? k + ' ' + d[k] : ''; }).filter(Boolean).join(' · ');
    if (soc) L.push('Social: ' + soc);
    L.push('');
    L.push('PAGES: ' + ((d.pages || []).join(', ') || '—') + (d.pages_other ? ' + ' + d.pages_other : ''));
    if ((d.services || []).length) {
      L.push('');
      L.push('SERVICES');
      d.services.forEach(function (s) { L.push('• ' + s.name + (s.price ? ' — ' + s.price : '') + (s.desc ? ' — ' + s.desc : '')); });
      L.push('Prices on site: ' + (d.show_prices || '—'));
    }
    L.push('');
    L.push('TRUST');
    if (d.story) L.push('Story: ' + d.story);
    var usp = [d.usp1, d.usp2, d.usp3].filter(Boolean);
    if (usp.length) L.push('Different: ' + usp.join(' | '));
    if (d.projects) L.push('Projects: ' + d.projects);
    if (d.certs) L.push('Certs: ' + d.certs);
    if (d.team) L.push('Team: ' + d.team);
    if (d.testimonials) L.push('Testimonials: ' + d.testimonials);
    if (d.stats) L.push('Numbers: ' + d.stats);
    L.push('');
    L.push('LOOK');
    L.push('Logo: ' + (uploads.logo.length ? uploads.logo.length + ' file(s)' : ((d.no_logo || []).length ? 'none — use name in type' : 'not sent')));
    L.push('Photos: ' + (uploads.photos.length ? uploads.photos.length + ' file(s)' : ((d.stock_photos || []).length ? 'use stock' : 'not sent')));
    if (uploads.docs.length) L.push('Other files: ' + uploads.docs.length);
    if (d.colours) L.push('Colours: ' + d.colours);
    if ((d.style_words || []).length) L.push('Feel: ' + d.style_words.join(', '));
    if (d.refs) L.push('Likes: ' + d.refs);
    if (d.avoid) L.push('Avoid: ' + d.avoid);
    L.push('');
    L.push('DOMAIN: ' + (d.domain_state || ''));
    if (d.domain_have) L.push('Has: ' + d.domain_have);
    var dn = [d.domain1, d.domain2, d.domain3].filter(Boolean);
    if (dn.length) L.push('Wants: ' + dn.join(', '));
    if (d.emails_wanted) L.push('Mailbox to create: ' + d.emails_wanted);
    if (uploads.cr.length) L.push('CR uploaded: yes');
    L.push('');
    L.push('FEATURES: ' + ((d.features || []).join(', ') || '—'));
    if (d.special) L.push('Special: ' + d.special);
    if (d.deadline) L.push('Needed by: ' + d.deadline);
    return L.join('\n');
  }

  $('#submit').onclick = function () {
    if (!validate(FORMLAST)) return;
    var btn = this, errBox = $('#err');
    errBox.hidden = true;
    btn.disabled = true;
    btn.textContent = body.classList.contains('ar') ? 'جارٍ الإرسال…' : 'Sending…';

    var d = collect();
    var ref = 'BRIEF-' + new Date().getFullYear() + '-' + Math.floor(1000 + Math.random() * 9000);
    var payload = {
      ref: ref,
      business: (d.biz_en || '').slice(0, 200),
      contact_name: (d.contact_name || '').slice(0, 120),
      whatsapp: (d.wa || '').slice(0, 40),
      email: (d.email || '').slice(0, 120),
      package: (d.package || '').slice(0, 120),
      brief: d,
      files: uploads,
      source: 'brief.getignitro.com',
      user_agent: navigator.userAgent.slice(0, 300)
    };
    var text = summary(d, ref);

    function finish() {
      $('#ref').textContent = ref; $('#ref2').textContent = ref;
      $('#wa-link').href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text);
      try { localStorage.removeItem(STORE); } catch (e) {}
      go(LAST);
      $('#bar').style.width = '100%';
    }

    fetch(SB + '/rest/v1/website_briefs', {
      method: 'POST',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      finish();
    }).catch(function () {
      // Never lose a lead: fall through to WhatsApp with the whole brief in the message.
      finish();
      var l = $('#wa-link');
      l.classList.add('go');
      errBox.hidden = false;
      errBox.textContent = body.classList.contains('ar')
        ? 'تعذّر الحفظ تلقائيًا. اضغط الزر لإرسال نسختك عبر واتساب — لن تفقد شيئًا.'
        : "We couldn't save it automatically. Tap the button to send your brief on WhatsApp — nothing is lost.";
    });
  };

  /* ---------- pre-set package from the link ---------- */
  var PKGMAP = { basic:'Basic — 3 pages · QAR 699', starter:'Starter — 5 pages · QAR 899',
                 business:'Business — 12 pages · QAR 1,199', store:'Online store · QAR 1,999',
                 ecom:'E-commerce + payment gateway · QAR 3,399' };
  (function () {
    var q = new URLSearchParams(location.search);
    var pk = (q.get('pkg') || '').toLowerCase(), who = q.get('for') || '';
    if (who) { var el = document.querySelector('[name=biz_en]'); if (el && !el.value) el.value = who; }
    if (!PKGMAP[pk]) return;
    var radio = document.querySelector('input[name=package][value="' + PKGMAP[pk] + '"]');
    if (!radio) return;
    radio.checked = true;
    document.querySelector('.pkgs').hidden = true;
    var box = document.createElement('div');
    box.className = 'locked';
    box.innerHTML = '<span class="en">Your package</span><span class="ar">باقتك</span><b>' + PKGMAP[pk] + '</b>';
    document.querySelector('.pkgs').insertAdjacentElement('afterend', box);
    var h = document.querySelector('.step[data-step="0"] .lead');
    if (h && who) {
      h.insertAdjacentHTML('beforebegin', '<p class="hello"><span class="en">Welcome, ' + who + ' 👋</span><span class="ar">أهلًا، ' + who + ' 👋</span></p>');
    }
  })();

  /* ---------- boot ---------- */
  restore();
  domainToggle();
  pageHint();
  $('#bar').style.width = Math.round((cur / FORMLAST) * 100) + '%';
  window.addEventListener('beforeunload', save);
})();

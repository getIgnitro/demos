"""Builds estore/ (Qatar e-commerce demo, QAR) from intl/estore/ (Maison Cacao, USD).
Run after build_intl.py (which builds intl/estore). Identity: Bait Al Cacao, The Pearl, Doha."""
import re, shutil, pathlib, json
root = pathlib.Path(__file__).parent
src, out = root / "intl" / "estore", root / "estore"
if out.exists(): shutil.rmtree(out)
shutil.copytree(src, out)

PRICE_LINE = "__PRICE_LINE__"   # replaced once Kashif approves the figure
TXT = [
    ("Maison <b>Cacao</b>", "Bait <b>Al Cacao</b>"), ("Maison Cacao", "Bait Al Cacao"),
    ("Chocolatier in the Sablon, Brussels, since 2009.", "Chocolatier at The Pearl, Doha, since 2015."),
    ("Sablon, Brussels · since 2009", "The Pearl, Doha · since 2015"), ("Chocolate the way Brussels still makes it.", "Chocolate made in Doha, the way it should be."),
    ("Pralines, truffles and tablets from our own atelier — boxed the morning they are made and at your door in two days.", "Pralines, truffles and tablets from our own kitchen at The Pearl — boxed the morning they are made and at your door the same day."),
    ("Rue au Beurre 12, 1000 Brussels", "Porto Arabia, Parcel 4, The Pearl, Doha"), ("Rue au Beurre 12", "Porto Arabia, The Pearl"),
    ("hello@maisoncacao.be", "hello@baitalcacao.qa"), ("+1 (555) 010-0199", "+974 6002 7117"), ("15550100199", "97460027117"),
    ("Mon–Sat 10:00–19:00", "Sat–Thu 10:00–22:00 · Fri 14:00–22:00"), ("Monday to Saturday 10:00–19:00", "Saturday to Thursday 10:00–22:00 · Friday 14:00–22:00"),
    ("maps?q=Rue+au+Beurre+12+Brussels&output=embed", "maps?q=Porto+Arabia+The+Pearl+Doha&output=embed"),
    ("Free delivery over $60 · Ships in 1–2 working days · Use code WELCOME10 for 10% off your first order", "Free delivery in Doha over QAR 200 · Same-day before 14:00 · Code WELCOME10 for 10% off your first order"),
    ("Ships in 1–2 days</b><span>Cold-packed in summer. Tracked, always.</span>", "Same-day in Doha</b><span>Order before 14:00. Cold-packed, always.</span>"),
    ("Card or PayPal. We never see your card number.", "Card, QPay debit or cash on delivery. We never see your card number."),
    ("Made in Brussels</b><span>Our atelier, our recipes, our people.</span>", "Made in Doha</b><span>Our kitchen, our recipes, our people.</span>"),
    ("<b>Ships</b> in 1–2 working days · <b>Free delivery</b> over $60", "<b>Same-day delivery</b> in Doha before 14:00 · <b>Free delivery</b> over QAR 200"),
    ("Marie L. · Brussels", "Maryam A. · West Bay"), ("Tom H. · Antwerp", "Tariq H. · Al Wakrah"), ("Arrived next day, perfectly packed, nothing melted.", "Arrived the same afternoon, perfectly packed, nothing melted."),
    ("Delivery (free over $60)", "Delivery (free over QAR 200)"), ("card or PayPal · 14-day returns", "card, QPay or cash · 14-day returns"),
    ('<div class="pay-tabs"><button type="button" class="on" data-p="card">💳 Card</button><button type="button" data-p="paypal">PayPal</button></div>', '<div class="pay-tabs"><button type="button" class="on" data-p="card">💳 Card</button><button type="button" data-p="paypal">QPay debit</button><button type="button" data-p="cod">Cash on delivery</button></div>'),
    ("powered by Stripe in the live build", "powered by Tap / Skipcash in the live build"),
    ("You'll be redirected to PayPal to approve the payment, then returned here.", "You'll be redirected to QPay to approve the payment with your Qatar debit card, then returned here."),
    ("Demo mode: use any 16 digits, any future date, any CVC. No money moves.", "Demo mode: use any 16 digits, any future date, any CVC. No money moves. Live build: Tap / Skipcash for cards, QPay for debit, cash on delivery."),
    ("<option>Belgium</option><option>Netherlands</option><option>France</option><option>Germany</option><option>United Kingdom</option><option>United States</option>", "<option>Doha</option><option>Al Wakrah</option><option>Al Khor</option><option>Lusail</option><option>Al Rayyan</option><option>Umm Salal</option>"),
    ("<label>Country</label>", "<label>City / area</label>"), ("<label>Postcode</label><input name=\"zip\" required>", "<label>Zone / street no.</label><input name=\"zip\" required placeholder=\"e.g. Zone 66, Street 850\">"),
    ("Our story</span><h2>A Sablon window that turned into an atelier.</h2><p>Bait Al Cacao began in 2009 as a single window on Rue au Beurre, selling pralines made in the back room by two people. Today the atelier employs eleven, ships across Europe, and still tempers every batch by hand.</p><p>We buy cocoa directly from three cooperatives in Ecuador and Ghana, pay above Fairtrade minimums, and print the origin on every box.</p>",
     "Our story</span><h2>A Pearl kiosk that turned into a kitchen.</h2><p>Bait Al Cacao began in 2015 as a kiosk at Porto Arabia, selling pralines made at home by two sisters. Today the kitchen employs nine, delivers across Doha, and still tempers every batch by hand.</p><p>We buy cocoa directly from three cooperatives in Ecuador and Ghana, pay above Fairtrade minimums, and print the origin on every box. Everything is halal; no alcohol in any recipe.</p>"),
    ("<div><b>2009</b><span>founded in the Sablon</span></div><div><b>11</b><span>chocolatiers and bakers</span></div><div><b>3</b><span>direct-trade origins</span></div><div><b>4.9★</b><span>from 2,400 reviews</span></div>", "<div><b>2015</b><span>founded at The Pearl</span></div><div><b>9</b><span>chocolatiers and bakers</span></div><div><b>3</b><span>direct-trade origins</span></div><div><b>4.9★</b><span>from 1,100 Google reviews</span></div>"),
    ("Orders placed before 14:00 CET ship the same working day. Belgium 1 day, EU 2–3 days, UK and US 3–5 days. Free delivery on orders over $60; otherwise $6. Summer orders are cold-packed at no charge.", "Orders placed before 14:00 are delivered the same day in Doha; Al Wakrah, Lusail and Al Khor next day. Free delivery on orders over QAR 200; otherwise QAR 15. All orders are cold-packed at no charge."),
    ("Card details are processed by Stripe or PayPal and never stored by us.", "Card details are processed by Tap / Skipcash or QPay and never stored by us."), ("hello@maisoncacao.be", "hello@baitalcacao.qa"),
    ("<li>Prices include VAT where applicable.</li>", "<li>Prices in Qatari Riyal. No VAT applicable in Qatar.</li>"),
    ("Corporate and wedding orders require 48 hours' notice and a 50% deposit.", "Corporate, Eid and wedding orders require 48 hours' notice and a 50% deposit."),
    ("Portfolio demo — Bait Al Cacao is a fictional business. Payments are simulated; the live build runs on Stripe or PayPal. A store like this, with payment gateway and 40 products loaded: $700, delivered in 14 days.",
     'Demo online store built by <a href="https://portfolio.getignitro.com" style="color:#F07800;font-weight:700">Ignitro</a> — Bait Al Cacao is a fictional business; payments are simulated. The live build runs on Tap / Skipcash / QPay with cash on delivery. ' + PRICE_LINE + ' WhatsApp "WEBSITE" to +974 6002 7117.'),
    ("Pralines, truffles, tablets and pastries from our Brussels atelier. Ships in 1–2 days.", "Pralines, truffles, tablets and pastries from our kitchen at The Pearl, Doha. Same-day delivery."),
    ("Our atelier in the Sablon, Brussels, since 2009.", "Our kitchen at The Pearl, Doha, since 2015."), ("Brussels atelier", "kitchen at The Pearl"), ("Sablon, Brussels", "The Pearl, Doha"), ("Brussels", "Doha"),
    ('<span id="sub">$0</span>', '<span id="sub">QAR 0</span>'), ('<span id="tot">$0</span>', '<span id="tot">QAR 0</span>'),
]
for f in out.glob("*.html"):
    h = f.read_text(encoding="utf-8")
    for a, b in TXT: h = h.replace(a, b)
    f.write_text(h, encoding="utf-8")

j = (out / "app.js").read_text(encoding="utf-8")
# prices ×3.65 → nearest 5 QAR
j = re.sub(r'"price": (\d+)', lambda m: '"price": ' + str(int(round(int(m.group(1)) * 3.65 / 5.0) * 5)), j)
j = j.replace("var money=function(n){return '$'+(Math.round(n*100)/100).toFixed(2).replace(/\\.00$/,'');};", "var money=function(n){return 'QAR '+(Math.round(n*100)/100).toFixed(2).replace(/\\.00$/,'');};")
j = j.replace("ship=(sub-disc)>=60||sub===0?0:6", "ship=(sub-disc)>=200||sub===0?0:15")
j = j.replace("btn.textContent=pay==='card'?'Processing…':'Redirecting to PayPal…'", "btn.textContent=pay==='card'?'Processing…':pay==='paypal'?'Redirecting to QPay…':'Placing order…'")
j = j.replace("pay:pay==='card'?'Card •••• '+cn.value.slice(-4):'PayPal'", "pay:pay==='card'?'Card •••• '+cn.value.slice(-4):pay==='paypal'?'QPay debit':'Cash on delivery'")
j = j.replace("(pay==='card'?'paid by card':'paid with PayPal')", "(pay==='card'?'paid by card':pay==='paypal'?'paid with QPay':'cash on delivery')")
j = j.replace("Ships in 1–2 working days.", "Delivered today if ordered before 14:00.")
j = j.replace("In the live build this step runs on Stripe or PayPal with real receipts.", "In the live build this step runs on Tap / Skipcash / QPay with real receipts.")
j = j.replace("if(pay==='card'&&(", "if(pay==='cod'){} else if(pay==='card'&&(")
j = j.replace("'97460027117'", "'97460027117'").replace("15550100199", "97460027117")
j = j.replace("Maison Cacao", "Bait Al Cacao").replace("hand-finished in Brussels", "hand-finished in Doha")
for a_, b_ in [("Marie L. · Brussels", "Maryam A. · West Bay"), ("Tom H. · Antwerp", "Tariq H. · Al Wakrah"), ("Arrived next day, perfectly packed, nothing melted.", "Arrived the same afternoon, perfectly packed, nothing melted."), ("<b>Ships</b> in 1–2 working days · <b>Free delivery</b> over $60", "<b>Same-day delivery</b> in Doha before 14:00 · <b>Free delivery</b> over QAR 200")]:
    j = j.replace(a_, b_).replace("MC-'+new Date()", "BC-'+new Date()")
(out / "app.js").write_text(j, encoding="utf-8")
# checkout: show/hide COD panel via existing tab logic — add a COD panel
ck = (out / "checkout.html").read_text(encoding="utf-8")
ck = ck.replace('<div class="card-ui" id="paypalui" style="display:none">', '<div class="card-ui" id="codui" style="display:none"><p style="font-size:14px;color:var(--mute)">Pay the driver in cash or by card machine on delivery. Available inside Doha only.</p></div><div class="card-ui" id="paypalui" style="display:none">')
(out / "checkout.html").write_text(ck, encoding="utf-8")
j = (out / "app.js").read_text(encoding="utf-8")
j = j.replace("$('#paypalui').style.display=pay==='paypal'?'block':'none';", "$('#paypalui').style.display=pay==='paypal'?'block':'none'; var cu=$('#codui'); if(cu) cu.style.display=pay==='cod'?'block':'none';")
(out / "app.js").write_text(j, encoding="utf-8")
left = [w for w in ["Maison", "Brussels", "Sablon", "PayPal", "Stripe", "$", "Belgium", "15550100199"] if any(w in p.read_text(encoding="utf-8") for p in list(out.glob("*.html")) + [out / "app.js"])]
print("qstore built; leftovers:", left)

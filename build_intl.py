"""Builds intl/ (Upwork version) from the Qatar demos: USD prices, English only, no Qatar, minimal Ignitro.
Run from repo root: python build_intl.py
"""
import re, shutil, pathlib
root = pathlib.Path(__file__).parent
out = root / "intl"
if out.exists(): shutil.rmtree(out)
for site in ["salon", "contracting", "store"]:
    shutil.copytree(root / site, out / site, ignore=shutil.ignore_patterns("_parts.py", "__pycache__"))

PHONE_DISPLAY = "+1 (555) 010-0199"; PHONE_WA = "15550100199"

COMMON = [
    ("+974 6002 7117", PHONE_DISPLAY), ("+974 60027117", PHONE_DISPLAY), ("97460027117", PHONE_WA),
    ("Doha, Qatar", "Springfield"), (", Doha", ", Springfield"), ("Doha", "Springfield"), ("Qatar's", "the city's"), ("Qatar", "the city"),
    ("QAR ", "$"), ("QAR", "$"),
    ("family=Playfair+Display:wght@600;700&family=Inter:wght@400;600;700;800&family=Tajawal:wght@400;700&display=swap", "family=Playfair+Display:wght@600;700&family=Inter:wght@400;600;700;800&display=swap"),
    ("family=Inter:wght@400;600;700;800;900&family=Cairo:wght@400;700;900&display=swap", "family=Inter:wght@400;600;700;800;900&display=swap"),
    ("family=Marcellus&family=Inter:wght@400;600;700;800&family=Cairo:wght@400;700;900&display=swap", "family=Marcellus&family=Inter:wght@400;600;700;800&display=swap"),
    ('<button class="lang" id="lang">عربي</button>', ""),
    ("Arabic + English, ", ""), ("Arabic + English · ", ""), ("Arabic + English", "English"),
    ("output=embed", "output=embed"),
]
SALON = [
    ("Ladies Salon, Al Sadd, Springfield", "Ladies Salon, Midtown"),
    ("Ladies-only salon in Al Sadd, Springfield.", "Ladies-only salon in Midtown."),
    ("Ladies only · Al Sadd, Springfield", "Ladies only · Midtown"),
    ("Where Springfield's women come to feel like themselves again.", "Where the city's women come to feel like themselves again."),
    ("Al Sadd Street, Building 14, 1st floor, Springfield", "214 Maple Avenue, 2nd floor, Midtown"),
    ("Al Sadd Street, Building 14, Springfield", "214 Maple Avenue, Midtown"),
    ("years in Al Sadd", "years in Midtown"),
    ("Saturday to Thursday 10:00–21:00 · Friday 14:00–21:00", "Monday to Saturday 10:00–20:00 · Sunday 12:00–18:00"),
    ("Sat–Thu 10:00–21:00", "Mon–Sat 10:00–20:00"),
    ("Moroccan bath", "Body scrub &amp; steam"), ("Moroccan bath and massage", "body scrubs and massage"),
    ("hair to henna", "hair to hands"), ("nails and henna", "nails and a trial"),
    ("hello@noorbeauty.qa", "hello@noorbeautylounge.com"),
    ("maps?q=Al+Sadd+Street,+Springfield,+the city&output=embed", "maps?q=Maple+Avenue+Midtown&output=embed"),
    # prices
    ("from $120", "from $35"), ("from $80", "from $25"), ("from $150", "from $45"), ("Packages from $1,500", "Packages from $420"),
    ("<span>120</span>", "<span>35</span>"), ("<span>70</span>", "<span>20</span>"), ("<span>from 280</span>", "<span>from 80</span>"),
    ("<span>from 450</span>", "<span>from 130</span>"), ("<span>from 600</span>", "<span>from 170</span>"), ("<span>180</span>", "<span>50</span>"),
    ("<span>80</span>", "<span>25</span>"), ("<span>100</span>", "<span>30</span>"), ("<span>140</span>", "<span>40</span>"),
    ("<span>250</span>", "<span>70</span>"), ("<span>15</span>", "<span>5</span>"), ("<span>150</span>", "<span>45</span>"),
    ("<span>260</span>", "<span>75</span>"), ("<span>220</span>", "<span>65</span>"), ("<span>280</span>", "<span>80</span>"),
    ("<span>300</span>", "<span>85</span>"), ("<span>1,500</span>", "<span>420</span>"), ("<span>2,400</span>", "<span>680</span>"), ("<span>450</span>", "<span>130</span>"),
    ("All prices in Qatari Riyal and include consultation.", "All prices in USD and include consultation."),
    ('Demo website built by <a href="https://portfolio.getignitro.com">Ignitro</a> — Noor Beauty Lounge is a fictional business. Your own 3-page site like this: $699, live in 5 days. WhatsApp "WEBSITE" to +1 (555) 010-0199.', "Portfolio demo — Noor Beauty Lounge is a fictional business. A 3-page site like this: $100, live in 5 days."),
]
CONTRACTING = [
    ("Al Reem Contracting & Trading — Civil, MEP & Fit-out, Springfield", "Al Reem Contracting — Civil, MEP & Fit-out"),
    ("Grade B contractor in Springfield:", "Licensed general contractor:"), ("Grade B contractor in Springfield since 2012.", "Licensed general contractor since 2012."),
    ("Street 45, Industrial Area, Springfield · Sat–Thu 7:00–18:00", "45 Commerce Drive, Eastside · Mon–Fri 7:00–18:00"),
    ("Street 45, Gate 12, Industrial Area, Springfield", "45 Commerce Drive, Gate 12, Eastside"),
    ("Street 45, Industrial Area, Springfield", "45 Commerce Drive, Eastside"),
    ("Saturday to Thursday 7:00–18:00", "Monday to Friday 7:00–18:00"),
    ("info@alreemqatar.com", "info@alreemcontracting.com"),
    ("Grade B · Industrial Area, Springfield", "Licensed &amp; insured · Eastside"),
    ("across the city — 140 projects", "across the region — 140 projects"),
    ("Kahramaa and Civil Defence approvals handled by us.", "Utility connections and fire-marshal sign-off handled by us."),
    ("Kahramaa connections and load upgrades", "Utility connections and load upgrades"),
    ("Fire-fighting and Civil Defence certificate", "Fire suppression and fire-marshal certificate"),
    ("Ashghal and municipality approvals", "City permits and inspections"),
    ("Mall and landlord approvals", "Landlord and mall approvals"),
    ("Same-day delivery inside Springfield", "Same-day delivery inside the city"),
    ("from our Industrial Area yard, delivered same-day inside Springfield", "from our Eastside yard, delivered same-day inside the city"),
    ("Logistics warehouse, Birkat Al Awamer", "Logistics warehouse, Eastside"), ("Office fit-out, West Bay", "Office fit-out, Downtown"),
    ("Villa compound, Al Wakrah", "Townhouse row, Lakeview"), ("6 villas · structure to handover", "6 units · structure to handover"),
    ("Clinic MEP, Al Sadd", "Clinic MEP, Midtown"), ("HVAC + electrical + fire, MOPH approved", "HVAC + electrical + fire, health-department approved"),
    ("Showroom, Salwa Road", "Showroom, Route 9"), ("Boundary walls &amp; roads, Al Khor", "Site works &amp; access roads, North Park"), ("2.1 km · Ashghal approved", "2.1 km · city approved"),
    ("Thirteen years, one Industrial Area yard, 140 finished projects.", "Thirteen years, one Eastside yard, 140 finished projects."),
    ("a materials yard on Street 45.", "a materials yard on Commerce Drive."),
    ("We are a Grade B contractor registered with Ashghal and the Ministry of Municipality, ISO 9001 certified, and insured for every site we enter.", "We are a licensed general contractor, ISO 9001 certified, bonded and insured for every site we enter."),
    ("Civil engineer, 20 years in the city. Signs every quote personally.", "Civil engineer, 20 years in the trade. Signs every quote personally."),
    ("Kahramaa-approved; 300+ connections completed.", "Master electrician; 300+ connections completed."),
    ("Eng. Khalid Al-Reem", "Eng. Khalid Reem"), ("Eng. Priya Nair", "Eng. Priya Nair"),
    ("CR 12345 · Grade B contractor · ISO 9001", "License #12345 · Bonded &amp; insured · ISO 9001"),
    ("Al Reem Contracting &amp; Trading W.L.L.", "Al Reem Contracting LLC"), ("Al Reem Contracting &amp; Trading", "Al Reem Contracting"),
    ("for the city's contractors, developers and facility owners since 2012.", "for contractors, developers and facility owners since 2012."),
    ("e.g. Al Wakrah", "e.g. Lakeview"),
    ("maps?q=Industrial+Area,+Springfield,+the city&output=embed", "maps?q=Commerce+Drive&output=embed"),
    ('Demo website built by <a href="https://portfolio.getignitro.com">Ignitro</a> — Al Reem Contracting is a fictional company. Your own 5-page site like this: $899, live in 5 days. WhatsApp "WEBSITE" to +1 (555) 010-0199.', "Portfolio demo — Al Reem Contracting is a fictional company. A 5-page site like this: $180, live in 5 days."),
    ("Contracting &amp; Trading", "Contracting"),
]
STORE = [
    ("Dukkan Sweets — Cakes, Chocolate & Fresh Bakes, Al Wakrah", "Dukkan Sweets — Cakes, Chocolate & Fresh Bakes"),
    ("for same-day delivery in Springfield.", "for same-day delivery."),
    ("Free delivery in Springfield on orders over $150 · Order before 2pm for same-day", "Free delivery on orders over $40 · Order before 2pm for same-day"),
    ("Al Wakrah · since 2015", "Old Town · since 2015"),
    ("Order before 2pm, anywhere in Springfield and Al Wakrah.", "Order before 2pm, anywhere in the city."),
    ("Delivery (free over 150)", "Delivery (free over $40)"),
    ("Al Wakrah Souq, Shop 22, Al Wakrah", "Old Town Market, Unit 22"), ("Al Wakrah Souq, Shop 22", "Old Town Market, Unit 22"),
    ("Same-day delivery in Springfield before 2pm", "Same-day delivery before 2pm"),
    ("from our kitchen in Al Wakrah. Family-run since 2015. All products halal, no alcohol in any recipe.", "from our kitchen in Old Town. Family-run since 2015."),
    ("a two-metre counter in Al Wakrah Souq", "a six-foot counter in Old Town Market"),
    ("majlis trays, branded hampers and Eid boxes", "party trays, branded hampers and holiday boxes"),
    ("hello@dukkansweets.qa", "hello@dukkansweets.com"),
    ("Family-run sweets kitchen in Al Wakrah.", "Family-run sweets kitchen in Old Town."),
    ("maps?q=Al+Wakrah+Souq,+the city&output=embed", "maps?q=Old+Town+Market&output=embed"),
    ("e.g. Al Sadd", "e.g. Midtown"),
    ('Demo online store built by <a href="https://portfolio.getignitro.com">Ignitro</a> — Dukkan Sweets is a fictional business; orders here go to a demo WhatsApp. Your own store like this: $1,999. WhatsApp "WEBSITE" to +1 (555) 010-0199.', "Portfolio demo — Dukkan Sweets is a fictional business; orders go to a demo number. A store like this: $360."),
]
STORE_JS = [
    ("var del=sub>=150||sub===0?0:15", "var del=sub>=40||sub===0?0:5"), ("'QAR '", "'$'"), ("QAR '", "$'"), ("'Delivery: '+(del?'QAR 15':'Free')", "'Delivery: '+(del?'$5':'Free')"),
    ("'TOTAL: QAR '", "'TOTAL: $'"), ("' = QAR '", "' = $'"), ("'97460027117'", "'" + PHONE_WA + "'"),
]
PRICE_MAP = {"220": "60", "140": "40", "120": "35", "45": "12", "60": "18", "55": "15", "65": "18", "70": "20", "250": "70"}

def strip_arabic(h):
    h = re.sub(r'<span class="ar">.*?</span>', '', h, flags=re.S)
    h = re.sub(r'<span class="en">(.*?)</span>', r'\1', h, flags=re.S)
    return h

def apply(text, pairs):
    for a, b in pairs:
        text = text.replace(a, b)
    return text

for site, extra in [("salon", SALON), ("contracting", CONTRACTING), ("store", STORE)]:
    for f in (out / site).glob("*.html"):
        h = f.read_text(encoding="utf-8")
        h = strip_arabic(h)
        h = apply(h, extra)      # site-specific first (matches Qatar wording)
        h = apply(h, COMMON)
        h = apply(h, extra)      # second pass for strings that only match after COMMON
        h = h.replace('lang="en"', 'lang="en"')
        # safety: any leftover Arabic characters
        if re.search(r'[؀-ۿ]', h): print("ARABIC LEFT in", f)
        for bad in ["Qatar", "Doha", "QAR", "974", ".qa", "Kahramaa", "Ashghal", "Al Sadd", "Al Wakrah", "Industrial Area", "Ignitro"]:
            if bad in h: print(f"  '{bad}' left in {f.name}")
        f.write_text(h, encoding="utf-8")
    for f in (out / site).glob("*.js"):
        j = f.read_text(encoding="utf-8")
        j = re.sub(r",ar:'[^']*'", "", j); j = re.sub(r",dar:'[^']*'", "", j)
        if site == "store": j = re.sub(r"price:(\d+)", lambda m: "price:" + PRICE_MAP.get(m.group(1), m.group(1)), j)
        j = apply(j, STORE_JS if site == "store" else [("'97460027117'", "'" + PHONE_WA + "'")])
        j = j.replace("— demo by Ignitro", "— portfolio demo").replace("— demo store by Ignitro", "— portfolio demo")
        j = re.sub(r"'[^']*[؀-ۿ][^']*'", "''", j)   # drop any Arabic string literal
        j = j.replace("'QAR 15'", "'$5'").replace("QAR", "$")
        f.write_text(j, encoding="utf-8")
    for f in (out / site).glob("*.css"):
        c = f.read_text(encoding="utf-8").replace("— demo by Ignitro", "— portfolio demo").replace("— demo store by Ignitro", "— portfolio demo")
        f.write_text(c, encoding="utf-8")

HUB = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Website demos</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Inter,system-ui,sans-serif;background:#FDFCFA;color:#161310;padding:40px 20px 60px}
.wrap{max-width:1000px;margin:0 auto}.eyebrow{font-size:12px;letter-spacing:3px;text-transform:uppercase;font-weight:800;color:#6C2BD9}
h1{font-size:clamp(30px,5vw,48px);font-weight:900;letter-spacing:-1px;margin:10px 0 8px}p.lead{color:#4a463f;font-size:17px;max-width:640px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:34px}
a.card{display:block;background:#fff;border:1px solid #E9E4DB;border-radius:18px;padding:22px;text-decoration:none;color:inherit;box-shadow:0 10px 30px rgba(22,19,16,.05);transition:transform .15s}
a.card:hover{transform:translateY(-3px)}.card .t{font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#F07800}
.card h2{font-size:22px;font-weight:900;margin:8px 0 6px}.card p{color:#4a463f;font-size:14px}.card .pr{display:inline-block;margin-top:14px;background:#161310;color:#fff;font-weight:800;font-size:13px;padding:7px 12px;border-radius:999px}
.cta{margin-top:40px;background:#161310;color:#fff;border-radius:18px;padding:26px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.cta b{font-size:20px}.cta span.btn{background:#14a800;color:#fff;font-weight:900;padding:12px 20px;border-radius:999px}
.foot{margin-top:30px;font-size:12px;color:#8a8478}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<div class="eyebrow">Website demos</div>
<h1>Three demo websites. Three prices. Tap and try them on your phone.</h1>
<p class="lead">Every demo is a real working site: mobile-first, WhatsApp button, Google Maps, contact form, fast static hosting. The businesses are fictional. Yours would carry your name, photos and colours.</p>
<div class="grid">
  <a class="card" href="salon/"><div class="t">Basic · 3 pages</div><h2>Noor Beauty Lounge</h2><p>Salon. Home, services with prices, WhatsApp booking form.</p><span class="pr">$100 · live in 5 days</span></a>
  <a class="card" href="contracting/"><div class="t">Starter · 5 pages</div><h2>Al Reem Contracting</h2><p>Contractor. Services, project gallery, team page, quote form.</p><span class="pr">$180</span></a>
  <a class="card" href="store/"><div class="t">Online store</div><h2>Dukkan Sweets</h2><p>Cakes and bakes: catalogue, cart, delivery rules, checkout to WhatsApp.</p><span class="pr">$360</span></a>
</div>
<div class="cta"><div><b>Want one like these?</b><div style="opacity:.8;margin-top:4px">3 pages · mobile-first · live in 5 days · from $100</div></div><span class="btn">Message me on Upwork</span></div>
<div class="foot">Portfolio demos · fictional businesses · built and hosted by a small studio.</div>
</div></body></html>
'''
(out / "index.html").write_text(HUB, encoding="utf-8")
print("intl built")

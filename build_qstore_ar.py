"""Adds the Arabic layer to estore/ (Qatar gateway store). Run after build_qstore.py.
Arabic is Claude-drafted — [verify — native speaker] before wide sharing."""
import re, json, pathlib
root = pathlib.Path(__file__).parent
out = root / "estore"

# ---------- HTML strings: exact English → Arabic ----------
T = {
 # nav / header / ship line
 "Home": "الرئيسية", "Shop": "المتجر", "About": "من نحن", "Contact": "تواصل", "Policies": "السياسات", "Account": "حسابي", "Cart": "السلة",
 "Free delivery in Doha over QAR 200 · Same-day before 14:00 · Code WELCOME10 for 10% off your first order": "توصيل مجاني في الدوحة للطلبات فوق ٢٠٠ ر.ق · في نفس اليوم قبل الثانية ظهرًا · كود WELCOME10 لخصم ١٠٪ على طلبك الأول",
 # home
 "The Pearl, Doha · since 2015": "اللؤلؤة، الدوحة · منذ ٢٠١٥",
 "Chocolate made in Doha, the way it should be.": "شوكولاتة صُنعت في الدوحة، كما ينبغي أن تكون.",
 "Pralines, truffles and tablets from our own kitchen at The Pearl — boxed the morning they are made and at your door the same day.": "برالين وترافل وألواح من مطبخنا في اللؤلؤة — تُعبّأ صباح صنعها وتصلك في اليوم نفسه.",
 "Shop the range": "تسوّق التشكيلة", "Gifts &amp; corporate": "هدايا وشركات", "Signatures &amp; new arrivals": "المميزة والجديد", "All 40 products →": "كل المنتجات الأربعين ←",
 "Same-day in Doha": "في نفس اليوم بالدوحة", "Order before 14:00. Cold-packed, always.": "اطلب قبل الثانية ظهرًا. تعبئة مبرّدة دائمًا.",
 "Secure checkout": "دفع آمن", "Card, QPay debit or cash on delivery. We never see your card number.": "بطاقة أو QPay أو الدفع عند الاستلام. لا نرى رقم بطاقتك أبدًا.",
 "14-day returns": "إرجاع خلال ١٤ يومًا", "Unopened goods, no questions.": "للمنتجات غير المفتوحة، بلا أسئلة.",
 "Made in Doha": "صُنع في الدوحة", "Our kitchen, our recipes, our people.": "مطبخنا، وصفاتنا، فريقنا.",
 "10% off your first order": "خصم ١٠٪ على طلبك الأول", "Join the list — one email a month, never more.": "انضم للقائمة — رسالة واحدة شهريًا فقط.", "Join": "اشترك",
 # shop
 "All": "الكل", "Pralines": "برالين", "Truffles": "ترافل", "Tablets": "ألواح", "Pastries": "حلويات", "Gifts": "هدايا", "Pantry": "المؤن",
 "♥ Wishlist": "♥ المفضلة", "Featured": "المميزة", "Price: low to high": "السعر: من الأقل", "Price: high to low": "السعر: من الأعلى", "Name A–Z": "الاسم أ–ي",
 "You may also like": "قد يعجبك أيضًا",
 # cart
 "Your cart": "سلتك", "Subtotal": "المجموع", "Discount": "الخصم", "Delivery (free over QAR 200)": "التوصيل (مجاني فوق ٢٠٠ ر.ق)", "Delivery": "التوصيل", "Total": "الإجمالي", "Apply": "تطبيق", "Checkout": "إتمام الطلب",
 # checkout
 "1 · Contact &amp; delivery": "١ · التواصل والتوصيل", "Full name": "الاسم الكامل", "Email": "البريد الإلكتروني", "Address": "العنوان", "City": "المدينة", "City / area": "المدينة / المنطقة", "Zone / street no.": "المنطقة / رقم الشارع",
 "2 · Payment": "٢ · الدفع", "💳 Card": "💳 بطاقة", "QPay debit": "QPay بطاقة خصم", "Cash on delivery": "الدفع عند الاستلام", "Card number": "رقم البطاقة", "Expiry": "الانتهاء", "CVC": "رمز الأمان",
 "Pay now": "ادفع الآن", "Order summary": "ملخص الطلب",
 "Pay the driver in cash or by card machine on delivery. Available inside Doha only.": "ادفع للسائق نقدًا أو بجهاز البطاقة عند الاستلام. داخل الدوحة فقط.",
 "You'll be redirected to QPay to approve the payment with your Qatar debit card, then returned here.": "سيتم تحويلك إلى QPay لاعتماد الدفع ببطاقة الخصم القطرية ثم العودة إلى هنا.",
 "Demo mode: use any 16 digits, any future date, any CVC. No money moves. Live build: Tap / Skipcash for cards, QPay for debit, cash on delivery.": "وضع تجريبي: أدخل أي ١٦ رقمًا وأي تاريخ مستقبلي وأي رمز أمان. لا يتم خصم أي مبلغ. النسخة الحقيقية: Tap / Skipcash للبطاقات، QPay للخصم، والدفع عند الاستلام.",
 # account
 "Sign in": "تسجيل الدخول", "Demo sign-in — any email works, nothing is stored outside your browser.": "تسجيل تجريبي — أي بريد يعمل، ولا يُحفظ شيء خارج متصفحك.", "Name": "الاسم",
 "Your orders and saved items are below.": "طلباتك والعناصر المحفوظة أدناه.", "Sign out": "تسجيل الخروج", "Order history": "سجل الطلبات", "Wishlist": "المفضلة",
 # about
 "Our story": "قصتنا", "A Pearl kiosk that turned into a kitchen.": "كشك في اللؤلؤة تحوّل إلى مطبخ.",
 "Bait Al Cacao began in 2015 as a kiosk at Porto Arabia, selling pralines made at home by two sisters. Today the kitchen employs nine, delivers across Doha, and still tempers every batch by hand.": "بدأ بيت الكاكاو عام ٢٠١٥ ككشك في بورتو أرابيا يبيع برالين من صنع شقيقتين في المنزل. اليوم يعمل في المطبخ تسعة أشخاص، ونوصّل في أنحاء الدوحة، وما زلنا نُلطّف كل دفعة يدويًا.",
 "We buy cocoa directly from three cooperatives in Ecuador and Ghana, pay above Fairtrade minimums, and print the origin on every box. Everything is halal; no alcohol in any recipe.": "نشتري الكاكاو مباشرة من ثلاث تعاونيات في الإكوادور وغانا، وندفع فوق حدود التجارة العادلة، ونطبع المنشأ على كل علبة. كل منتجاتنا حلال، ولا كحول في أي وصفة.",
 "founded at The Pearl": "التأسيس في اللؤلؤة", "chocolatiers and bakers": "صانعو شوكولاتة وخبّازون", "direct-trade origins": "مناشئ تجارة مباشرة", "from 1,100 Google reviews": "من ١١٠٠ مراجعة على جوجل",
 # contact
 "Subject": "الموضوع", "Order question": "استفسار عن طلب", "Corporate order": "طلب شركات", "Wholesale": "جملة", "Other": "أخرى", "Message": "الرسالة", "Send": "إرسال",
 "Boutique &amp; atelier": "المتجر والمطبخ", "Porto Arabia, Parcel 4, The Pearl, Doha": "بورتو أرابيا، قطعة ٤، اللؤلؤة، الدوحة", "Hours": "ساعات العمل",
 "Saturday to Thursday 10:00–22:00 · Friday 14:00–22:00": "السبت–الخميس ١٠:٠٠–٢٢:٠٠ · الجمعة ١٤:٠٠–٢٢:٠٠", "Phone / WhatsApp": "هاتف / واتساب",
 # policies
 "Shipping": "التوصيل", "Returns": "الإرجاع", "Privacy": "الخصوصية", "Cookies": "ملفات تعريف الارتباط", "Terms": "الشروط",
 "Orders placed before 14:00 are delivered the same day in Doha; Al Wakrah, Lusail and Al Khor next day. Free delivery on orders over QAR 200; otherwise QAR 15. All orders are cold-packed at no charge.": "الطلبات قبل الثانية ظهرًا تُوصَّل في اليوم نفسه داخل الدوحة؛ الوكرة ولوسيل والخور في اليوم التالي. التوصيل مجاني للطلبات فوق ٢٠٠ ر.ق، وإلا ١٥ ر.ق. جميع الطلبات تُعبّأ مبرّدة دون رسوم.",
 "Unopened goods may be returned within 14 days of delivery for a full refund. Made-to-order pastries and personalised gifts are excluded. Damaged in transit? Send a photo within 48 hours and we replace it.": "يمكن إرجاع المنتجات غير المفتوحة خلال ١٤ يومًا من التوصيل لاسترداد كامل المبلغ. تُستثنى الحلويات المصنوعة حسب الطلب والهدايا المخصصة. تضرر أثناء التوصيل؟ أرسل صورة خلال ٤٨ ساعة ونستبدله.",
 "We store your name, address and order history to fulfil orders and, if you opt in, to send one newsletter a month. Card details are processed by Tap / Skipcash or QPay and never stored by us. You can request deletion at any time at hello@baitalcacao.qa.": "نحفظ اسمك وعنوانك وسجل طلباتك لتنفيذ الطلبات، ولإرسال نشرة شهرية واحدة إن اخترت ذلك. بيانات البطاقة تُعالج عبر Tap / Skipcash أو QPay ولا نخزنها أبدًا. يمكنك طلب الحذف في أي وقت عبر hello@baitalcacao.qa.",
 "Essential cookies run the cart and checkout. Analytics cookies are set only if you accept them in the banner.": "الملفات الأساسية تشغّل السلة والدفع. ملفات التحليلات تُفعّل فقط إذا وافقت عليها في الشريط.",
 "Prices in Qatari Riyal. No VAT applicable in Qatar.": "الأسعار بالريال القطري. لا تُطبق ضريبة قيمة مضافة في قطر.",
 "Allergens: all products are made in an atelier that handles nuts, milk, gluten, soy and eggs.": "مسببات الحساسية: جميع المنتجات تُصنع في مطبخ يتعامل مع المكسرات والحليب والغلوتين والصويا والبيض.",
 "Corporate, Eid and wedding orders require 48 hours' notice and a 50% deposit.": "طلبات الشركات والعيد والأعراس تتطلب إشعارًا قبل ٤٨ ساعة وعربونًا ٥٠٪.",
 # footer / cookie
 "Chocolatier at The Pearl, Doha, since 2015. Pralines, truffles, tablets and pastries, made in our own atelier.": "صانع شوكولاتة في اللؤلؤة، الدوحة، منذ ٢٠١٥. برالين وترافل وألواح وحلويات من مطبخنا.",
 "Help": "المساعدة", "Visit": "زورونا",
 "We use cookies for the cart and basic analytics. No tracking across sites.": "نستخدم ملفات تعريف الارتباط للسلة والتحليلات الأساسية فقط. لا تتبّع عبر المواقع.", "Essential only": "الأساسية فقط", "Accept": "موافق",
}
def wrap(en, ar): return f'<span class="en">{en}</span><span class="ar">{ar}</span>'
# longest first so multi-word phrases win over single words
keys = sorted(T, key=len, reverse=True)
for f in out.glob("*.html"):
    h = f.read_text(encoding="utf-8")
    for en in keys:
        ar = T[en]; w = wrap(en, ar)
        # tag text boundaries only: >EN< ; also option/label/button text
        h = h.replace(f">{en}<", f">{w}<")
    # option elements can't hold spans → use plain Arabic swap via data attr (keep English, add title)
    h = re.sub(r'<option([^>]*)><span class="en">(.*?)</span><span class="ar">(.*?)</span></option>', r'<option\1>\2</option>', h)
    # header: language button + fonts + css hooks
    h = h.replace('family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;600;700;800&display=swap', 'family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;600;700;800&family=Cairo:wght@400;700;900&display=swap')
    h = h.replace('<div class="right"><a class="icon" href="account.html">', '<div class="right"><button class="lang" id="lang">عربي</button><a class="icon" href="account.html">')
    h = h.replace('<html lang="en">', '<html lang="en">')
    # footer credit bilingual
    h = h.replace('Bait Al Cacao is a fictional business; payments are simulated. The live build runs on Tap / Skipcash / QPay with cash on delivery. A store like this: QAR 3,399, delivered in 14 days. WhatsApp "WEBSITE" to +974 6002 7117.',
                  wrap('Bait Al Cacao is a fictional business; payments are simulated. The live build runs on Tap / Skipcash / QPay with cash on delivery. A store like this: QAR 3,399, delivered in 14 days. WhatsApp "WEBSITE" to +974 6002 7117.',
                       'بيت الكاكاو اسم افتراضي؛ الدفع تجريبي. النسخة الحقيقية تعمل عبر Tap / Skipcash / QPay مع الدفع عند الاستلام. متجر مثل هذا: ٣٣٩٩ ر.ق خلال ١٤ يومًا. واتساب "WEBSITE" إلى ٦٠٠٢ ٧١١٧.'))
    f.write_text(h, encoding="utf-8")

css = (out / "styles.css").read_text(encoding="utf-8")
css += '''
/* Arabic layer */
body.ar{direction:rtl;font-family:'Cairo','Inter',sans-serif}body.ar h1,body.ar h2,body.ar h3{font-family:'Cairo',sans-serif;font-weight:900}
.en,.ar{display:inline}body.ar .en{display:none}body:not(.ar) .ar{display:none}
.lang{font-size:12px;font-weight:800;border:1.5px solid var(--cocoa);border-radius:999px;padding:8px 12px;background:none;color:var(--cocoa)}
body.ar .badge{left:auto;right:10px}body.ar .wish{right:auto;left:10px}body.ar .wa{right:auto;left:18px}body.ar .toast{font-family:'Cairo',sans-serif}
'''
(out / "styles.css").write_text(css, encoding="utf-8")

# ---------- JS: Arabic product names/descriptions + UI strings + toggle ----------
FL = {"Dark 70%": "داكنة ٧٠٪", "Milk 38%": "بالحليب ٣٨٪", "Hazelnut": "بندق", "Sea Salt": "ملح بحري", "Pistachio": "فستق", "Orange Peel": "قشر برتقال", "Speculoos": "سبيكولوس", "Raspberry": "توت", "Champagne": "شامبانيا (خالٍ من الكحول)", "Espresso": "إسبريسو", "Salted Caramel": "كراميل مملّح", "Raspberry Rose": "توت وورد", "Praliné Crunch": "برالين مقرمش", "Matcha": "ماتشا"}
NAMES = {
 "Gâteau au Chocolat · serves 10": ("كيكة الشوكولاتة · تكفي ١٠", "ثلاث طبقات، غاناش داكن، ورود كريمة. تُحضّر عند الطلب."),
 "Fraisier · serves 12": ("فريزييه · تكفي ١٢", "جينواز وفراولة وكريم موسلين. تُحضّر عند الطلب."),
 "Sablés au Chocolat · box of 12": ("سابليه بالشوكولاتة · علبة ١٢", "شورت بريد بالزبدة ورقائق الشوكولاتة، يُخبز كل صباح."),
 "Cupcakes de Fête · box of 6": ("كب كيك احتفالي · علبة ٦", "فانيليا وشوكولاتة، بألوانك عند الطلب."),
 "Cupcakes de Fête · box of 12": ("كب كيك احتفالي · علبة ١٢", "فانيليا وشوكولاتة، بألوانك عند الطلب."),
 "Beignets Glacés · box of 6": ("دونات مغلّف · علبة ٦", "شوكولاتة وفانيليا ورشّات."),
 "Crêpes aux Fraises · box of 4": ("كريب بالفراولة · علبة ٤", "كريمة طازجة وفراولة، يُحضّر عند الطلب."),
 "Tiramisu · 4 parts": ("تيراميسو · ٤ قطع", "مشبع بالقهوة مع ماسكربوني وكاكاو. خالٍ من الكحول."),
 "Discovery Gift Set": ("طقم هدية الاكتشاف", "برالين ٩ ولوحان وعلبة ترافل بشريط."),
 "Grand Gift Hamper": ("سلة الهدايا الكبرى", "برالين ٢٤ وأربعة ألواح وعلبتا ترافل وبطاقة مكتوبة بخط اليد."),
 "Corporate Box · 20 units": ("علبة الشركات · ٢٠ وحدة", "عشرون علبة برالين ٩ بشعاركم على الغلاف. بإشعار ٤٨ ساعة."),
 "Wedding Favour Set · 50 units": ("طقم توزيعات الأعراس · ٥٠ وحدة", "خمسون علبة بقطعتين، بشريط بألوانكم."),
 "Advent Calendar": ("تقويم الشتاء", "٢٤ بابًا، ٢٤ برالين. يُشحن من ١ نوفمبر."),
 "Easter Egg · 300 g": ("بيضة شوكولاتة · ٣٠٠ غ", "بيضة حليب مرسومة يدويًا محشوة بمصغّرات البرالين."),
 "Hot Chocolate Flakes · 250 g": ("رقائق شوكولاتة ساخنة · ٢٥٠ غ", "رقائق كوفرتور حقيقية. ملعقتان لكل كوب."),
 "Cocoa Nibs · 200 g": ("حبيبات كاكاو · ٢٠٠ غ", "محمصة وغير محلّاة، للخبز والأطباق."),
 "Baking Couverture · 1 kg": ("كوفرتور للخبز · ١ كجم", "داكنة ٦٤٪ على شكل أقراص، للمحترفين وهواة الخبز."),
 "Praliné Spread · 300 g": ("سبريد برالين · ٣٠٠ غ", "برالين بندق، بدون زيت نخيل."),
 "Chocolate Fondue Kit": ("طقم فوندو الشوكولاتة", "٥٠٠ غ كوفرتور وقدر سيراميك وأربع شوكات."),
 "Tasting Flight · 6 origins": ("رحلة التذوق · ٦ مناشئ", "ست مربعات ٢٠ غ مع بطاقة تذوق."),
 "Drinking Chocolate Gift Tin · 500 g": ("علبة هدية شوكولاتة للشرب · ٥٠٠ غ", "رقائق وملعقة خشبية وبطاقة الوصفة في علبة تذكارية."),
}
def arabic_for(name, cat):
    if name in NAMES: return NAMES[name]
    m = re.match(r"Signature Praliné Box · (\d+) pieces", name)
    if m: return (f"علبة برالين مميزة · {m.group(1)} قطعة", "بندق وكراميل بملح البحر وفستق وداكنة ٧٠٪، تُنهى يدويًا في الدوحة.")
    m = re.match(r"Tablet · (.+) · 100 g", name)
    if m: return (f"لوح شوكولاتة · {FL.get(m.group(1), m.group(1))} · ١٠٠ غ", "كوفرتور أحادي المنشأ، مُلطّف يدويًا. يُكسر بنقاء ويذوب ببطء.")
    m = re.match(r"Truffle Selection · (.+) · 12 pcs", name)
    if m: return (f"تشكيلة ترافل · {FL.get(m.group(1), m.group(1))} · ١٢ قطعة", "غاناش مغلّف بالكاكاو، يُعبّأ صباح صنعه.")
    return (name, "")
js = (out / "app.js").read_text(encoding="utf-8")
prods = json.loads(re.search(r"var P=(\[.*?\]), CATS=", js, re.S).group(1))
AR = {p["id"]: list(arabic_for(p["name"], p["cat"])) for p in prods}
UI = {"Add": "أضف", "Added ✓": "تمت الإضافة ✓", "Added to cart": "أُضيف إلى السلة", "Saved to wishlist": "حُفظ في المفضلة", "Removed from wishlist": "أُزيل من المفضلة",
      "Nothing matches. Try another word.": "لا نتائج. جرّب كلمة أخرى.", "Your cart is empty.": "سلتك فارغة.", "Remove": "حذف", "products": "منتجات", "of": "من",
      "Add to cart": "أضف إلى السلة", "Buy now": "اشترِ الآن", "Reviews": "المراجعات", "reviews": "مراجعة", "Free": "مجانًا", "Check the card details": "تحقق من بيانات البطاقة",
      "Processing…": "جارٍ المعالجة…", "Redirecting to QPay…": "جارٍ التحويل إلى QPay…", "Placing order…": "جارٍ إرسال الطلب…", "Order confirmed": "تم تأكيد الطلب",
      "View order history": "عرض سجل الطلبات", "Continue shopping": "متابعة التسوق", "No orders yet.": "لا طلبات بعد.", "Nothing saved yet. Tap ♡ on any product.": "لا شيء محفوظ بعد. اضغط ♡ على أي منتج.",
      "Signed in (demo)": "تم تسجيل الدخول (تجريبي)", "Thanks — this is a demo, nothing was sent.": "شكرًا — هذا عرض تجريبي، لم يُرسل شيء.", "10% off applied": "تم تطبيق خصم ١٠٪", "Code not recognised": "الكود غير معروف",
      "paid by card": "مدفوع بالبطاقة", "paid with QPay": "مدفوع عبر QPay", "cash on delivery": "الدفع عند الاستلام", "Delivered today if ordered before 14:00.": "يُوصَّل اليوم إذا طُلب قبل الثانية ظهرًا.",
      "A confirmation email goes to ": "رسالة تأكيد إلى ", "Demo mode — no money moved. In the live build this step runs on Tap / Skipcash / QPay with real receipts.": "وضع تجريبي — لم يُخصم أي مبلغ. في النسخة الحقيقية تعمل هذه الخطوة عبر Tap / Skipcash / QPay بإيصالات حقيقية.",
      "Only ": "بقي ", " left": " فقط", "Ships": "التوصيل", "in stock": "متوفر"}
inject = "var AR=" + json.dumps(AR, ensure_ascii=False) + ";P.forEach(function(p){var a=AR[p.id];if(a){p.ar=a[0];p.dar=a[1];}});var UI=" + json.dumps(UI, ensure_ascii=False) + ";\n" \
  "var body=document.body;try{if(localStorage.getItem('lang')==='ar')body.classList.add('ar');}catch(e){}var isAr=function(){return body.classList.contains('ar');};var t=function(s){return isAr()&&UI[s]?UI[s]:s;};var nm=function(p){return isAr()&&p.ar?p.ar:p.name;};var ds=function(p){return isAr()&&p.dar?p.dar:p.desc;};\n" \
  "(function(){var b=document.getElementById('lang');if(!b)return;b.textContent=isAr()?'EN':'عربي';b.onclick=function(){var ar=!isAr();try{localStorage.setItem('lang',ar?'ar':'en');}catch(e){}location.reload();};})();\n"
js = js.replace("  var P=", "  var P=", 1)
js = re.sub(r"(  var K=\{cart:)", inject + r"\1", js, count=1)
# swap strings in render code
reps = [("'+p.name+'", "'+nm(p)+'"), ("'+p.desc+'", "'+ds(p)+'"), ("'+it.p.name+'", "'+nm(it.p)+'"),
        ("'<div class=\"low\">Only '+p.stock+' left</div>'", "'<div class=\"low\">'+t('Only ')+p.stock+t(' left')+'</div>'"),
        ("\">Add</button>", "\">'+t('Add')+'</button>"), ("b.textContent='Added ✓'", "b.textContent=t('Added ✓')"), ("b.textContent='Add'", "b.textContent=t('Add')"),
        ("toast('Added to cart')", "toast(t('Added to cart'))"), ("toast(i<0?'Saved to wishlist':'Removed from wishlist')", "toast(t(i<0?'Saved to wishlist':'Removed from wishlist'))"),
        ("'<div class=\"empty\">Nothing matches. Try another word.</div>'", "'<div class=\"empty\">'+t('Nothing matches. Try another word.')+'</div>'"),
        ("c.textContent=list.length+' of '+P.length+' products'", "c.textContent=list.length+' '+t('of')+' '+P.length+' '+t('products')"),
        ("'<h1>'+p.name+'</h1>", "'<h1>'+nm(p)+'</h1>"), ("<p class=\"d\">'+p.desc+'</p>", "<p class=\"d\">'+ds(p)+'</p>"),
        ("id=\"addp\">Add to cart</button>", "id=\"addp\">'+t('Add to cart')+'</button>"), ("id=\"buy\">Buy now</button>", "id=\"buy\">'+t('Buy now')+'</button>"),
        ("4.9 · 128 reviews", "4.9 · 128 '+t('reviews')+'"), ("margin-bottom:8px\">Reviews</h3>", "margin-bottom:8px\">'+t('Reviews')+'</h3>"),
        ("'<div class=\"empty\">Your cart is empty. <a href=\"shop.html\" style=\"color:var(--gold);font-weight:800\">Shop</a></div>'", "'<div class=\"empty\">'+t('Your cart is empty.')+' <a href=\"shop.html\" style=\"color:var(--gold);font-weight:800\">'+t('Shop')+'</a></div>'"),
        ("'\">Remove</button></div>'", "'\">'+t('Remove')+'</button></div>'"), ("f('shipc',t.ship?money(t.ship):'Free')", "f('shipc',t.ship?money(t.ship):(document.body.classList.contains('ar')?'مجانًا':'Free'))"),
        ("toast('Check the card details')", "toast(t('Check the card details'))"), ("btn.textContent=pay==='card'?'Processing…':pay==='paypal'?'Redirecting to QPay…':'Placing order…'", "btn.textContent=t(pay==='card'?'Processing…':pay==='paypal'?'Redirecting to QPay…':'Placing order…')"),
        ("<h2>Order confirmed</h2>", "<h2>'+t('Order confirmed')+'</h2>"), ("(pay==='card'?'paid by card':pay==='paypal'?'paid with QPay':'cash on delivery')", "t(pay==='card'?'paid by card':pay==='paypal'?'paid with QPay':'cash on delivery')"),
        ("<br>A confirmation email goes to '+v('email')+'. Delivered today if ordered before 14:00.", "<br>'+t('A confirmation email goes to ')+v('email')+'. '+t('Delivered today if ordered before 14:00.')+'"),
        ("<div class=\"demo-note\">Demo mode — no money moved. In the live build this step runs on Tap / Skipcash / QPay with real receipts.</div>", "<div class=\"demo-note\">'+t('Demo mode — no money moved. In the live build this step runs on Tap / Skipcash / QPay with real receipts.')+'</div>"),
        ("href=\"account.html\">View order history</a>", "href=\"account.html\">'+t('View order history')+'</a>"), ("href=\"shop.html\">Continue shopping</a>", "href=\"shop.html\">'+t('Continue shopping')+'</a>"),
        ("'<div class=\"empty\">No orders yet.</div>'", "'<div class=\"empty\">'+t('No orders yet.')+'</div>'"), ("'<div class=\"empty\">Nothing saved yet. Tap ♡ on any product.</div>'", "'<div class=\"empty\">'+t('Nothing saved yet. Tap ♡ on any product.')+'</div>'"),
        ("toast('Signed in (demo)')", "toast(t('Signed in (demo)'))"), ("toast('Thanks — this is a demo, nothing was sent.')", "toast(t('Thanks — this is a demo, nothing was sent.'))"),
        ("toast('10% off applied')", "toast(t('10% off applied'))"), ("toast('Code not recognised')", "toast(t('Code not recognised'))"),
        ("<b>Same-day delivery</b> in Doha before 14:00 · <b>Free delivery</b> over QAR 200 · <b>Returns</b> 14 days on unopened goods · <b>Stock</b> '+(p.stock<=5?'only '+p.stock+' left':'in stock')+'",
         "'+(isAr()?'<b>توصيل في نفس اليوم</b> بالدوحة قبل الثانية ظهرًا · <b>توصيل مجاني</b> فوق ٢٠٠ ر.ق · <b>إرجاع</b> خلال ١٤ يومًا للمنتجات غير المفتوحة · <b>المخزون</b> '+(p.stock<=5?'بقي '+p.stock+' فقط':'متوفر'):'<b>Same-day delivery</b> in Doha before 14:00 · <b>Free delivery</b> over QAR 200 · <b>Returns</b> 14 days on unopened goods · <b>Stock</b> '+(p.stock<=5?'only '+p.stock+' left':'in stock'))+'"),
       ]
miss = [a for a, b in reps if a not in js]
for a, b in reps: js = js.replace(a, b)
(out / "app.js").write_text(js, encoding="utf-8")
print("arabic layer added; unmatched JS patterns:", len(miss), miss[:3])

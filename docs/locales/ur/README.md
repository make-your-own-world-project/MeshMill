<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

<!-- localization-navigation:start -->
<p align="center">
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/README.md">English</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ar/README.md">العربية</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/bn/README.md">বাংলা</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/de/README.md">Deutsch</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/el/README.md">Ελληνικά</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/es/README.md">Español</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fa/README.md">فارسی</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fr/README.md">Français</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ga/README.md">Gaeilge</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hi/README.md">हिन्दी</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hu/README.md">Magyar</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/id/README.md">Bahasa Indonesia</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/it/README.md">Italiano</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ja/README.md">日本語</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ko/README.md">한국어</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/nl/README.md">Nederlands</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pl/README.md">Polski</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pt/README.md">Português</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ro/README.md">Română</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ru/README.md">Русский</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/sr/README.md">Српски</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/th/README.md">ไทย</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/tr/README.md">Türkçe</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/uk/README.md">Українська</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ur/README.md">اردو</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/vi/README.md">Tiếng Việt</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/zh-CN/README.md">简体中文</a>
</p>
<!-- localization-navigation:end -->

MeshMill ایک مخصوص ڈیسک ٹاپ ایپلی کیشن ہے جو بہت بڑے سائز، زیادہ کثافت (dense) یا پیچیدہ میش جیومیٹری کو
قابلِ انتظام بنانے کے لیے استعمال ہوتی ہے۔ یہ تیز رفتار معائنے، کثافت کے تجزیے، مخصوص حصے کے انتخاب (regional selection)، تراشنے (cropping)، حذف کرنے،
اور کنٹرولڈ میش ریڈکشن (میش کا حجم کم کرنے) کی سہولت فراہم کرتی ہے، جس کے لیے کسی اکاؤنٹ یا جیومیٹری کو اپ لوڈ کرنے کی ضرورت نہیں ہوتی۔

GPU- ایکسلریٹڈ اوپن جی ایل رینڈرنگ ویو پورٹ نیویگیشن، ہارڈویئر چننے، کثافت کا تصور، (OpenGL)
اور انٹرایکٹو معائنہ ذمہ دار۔ میش کمی فی الحال الگ الگ مقامی CPU کارکنوں میں چلتی ہے،
جیومیٹری کے طویل حسابات کو انٹرفیس سے دور رکھنا۔

MeshMill مختلف ذرائع سے حاصل کردہ میشز کے ساتھ کام کرتی ہے، جیسے کہ 3D اسکینرز، CAD اور ماڈلنگ ایکسپورٹس، ری کنسٹرکشن پائپ لائنز،
تخلیق کردہ جیومیٹری، اور دیگر STL ذرائع۔ یہ جیومیٹری کو بعد کے مراحل کے ایڈیٹرز،
مینوفیکچرنگ ٹولز اور دیگر میش ورک فلو کے لیے تیار کرتی ہے۔ عام مقصد کی ماڈلنگ، مجسمہ سازی (sculpting)، اینیمیشن،
مواد (materials) اور سین (scene) کی تخلیق اس کے دائرہ کار میں شامل نہیں ہیں۔

## ڈاؤن لوڈ

اپنا آپریٹنگ سسٹم منتخب کریں۔ ہر پیکج خود ساختہ ہے۔ Python، Node.js، اور دیگر
ترقی کے انحصار کی ضرورت نہیں ہے.

| سسٹم | تجویز کردہ ڈاؤن لوڈ | حیثیت |
| --- | --- | --- |
| **ونڈوز x64** | **[ونڈوز انسٹالر ڈاؤن لوڈ کریں][windows-installer]** | تائید شدہ رہائی | <!-- Windows Windows -->
| Windows x64، کوئی انسٹالیشن نہیں | [پورٹ ایبل زپ ڈاؤن لوڈ کریں][windows-portable] | تائید شدہ رہائی |
| لینکس x86-64 | [linux-preview][linux-preview] | ابتدائی جانچ کا پیش نظارہ | <!-- Linux Linux -->
| macOS ایپل سلکان | [ایپل سلیکون کا پیش نظارہ ڈاؤن لوڈ کریں][mac-arm-preview] | ابتدائی جانچ کا پیش نظارہ |
| macOS انٹیل | [انٹیل میک کا پیش نظارہ ڈاؤن لوڈ کریں][mac-intel-preview] | ابتدائی جانچ کا پیش نظارہ |

**زیادہ تر ونڈوز صارفین کو ونڈوز انسٹالر کا انتخاب کرنا چاہیے۔** پورٹیبل زپ صرف اس وقت استعمال کریں جب آپ ایسا کریں۔ <!-- Windows Windows -->
MeshMill انسٹال نہیں کرنا چاہتے یا ایپلی کیشنز کو انسٹال کرنے کی اجازت نہیں ہے۔

لینکس اور میکوس پیکجز غیر دستخط شدہ ابتدائی پیش نظارہ ہیں۔ وہ خودکار مقامی تعمیرات کو پاس کرتے ہیں۔ <!-- Linux macOS -->
پیکیجڈ سموک ٹیسٹ، لیکن پھر بھی حقیقی ہارڈ ویئر ٹیسٹنگ کی ضرورت ہے۔ پڑھیں
[Linux اور macOS پیش نظارہ نوٹس](../../PLATFORM_TESTING.md) انسٹال کرنے سے پہلے۔

Windows SmartScreen یا macOS گیٹ کیپر غیر دستخط شدہ پیکجوں کے بارے میں خبردار کر سکتا ہے۔
سپورٹ شدہ ونڈوز ریلیز کے ساتھ ایک اختیاری نمونہ میش شامل کیا گیا ہے: [STL][sample-mesh]۔ <!-- Windows -->
پرانے ورژن اور ڈاؤن لوڈ چیکسمس [GitHub Releases][all-releases] پر دستیاب ہیں۔

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.2/MeshMill-0.1.2-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.2/MeshMill-0.1.2-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.2/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## فوری آغاز

1. ایک STL کھولیں۔
2. اسے Shaded، Density، Wireframe، یا Vertices ڈسپلے موڈ میں دیکھیں۔
3. معیار کی سطح، الگورتھم، اور ٹارگٹ ٹرائینگل کاؤنٹ (target triangle count) کا انتخاب کریں۔
4. نتیجہ اخذ کرنے کے لیے **Optimize** منتخب کریں۔
5. اصل اور آپٹمائزڈ میشز (meshes) کا موازنہ کریں، پھر عمل کو حتمی شکل دینے کے لیے **Apply** منتخب کریں۔
6. **Save current state** منتخب کریں یا `Ctrl+S` دبائیں۔

MeshMill کبھی بھی صرف اس وجہ سے آپٹیمائزیشن شروع نہیں کرتا کہ کوئی فائل یا سیٹنگ تبدیل ہوئی ہے۔

## صلاحیتیں

- بائنری اور ASCII ان پٹ، بائنری آؤٹ پٹ (STL) (STL)
- کثافت میں توازن رکھنے والی، شکل اور ٹوپولوجی کو برقرار رکھنے والی کمی (reduction) (Fast QEM)
- GPU- ایکسلریٹڈ اوپن جی ایل ویو پورٹ، ہارڈویئر چننا، اور کثافت کا تصور (OpenGL)
- میش میں کمی کے لیے مقامی پس منظر جیومیٹری ورکرز
- شیڈڈ (shaded)، کثافت، وائر فریم، اور ورٹیکس (vertex) ڈسپلے موڈز
- مثلثوں کی مقررہ حد کے بجائے جیومیٹری سے اخذ کردہ خودکار اہداف
- پولی گان کا انتخاب بمعہ اضافی کثیر-خطہ (multi-region) انتخاب
- صرف منتخب حصے کو تراشنا (crop)، حذف کرنا، یا بہتر بنانا (optimize)
- کیش شدہ اصل، پچھلے اور موجودہ میش (mesh) کا موازنہ
- جیومیٹری میں کی گئی تبدیلیوں کے لیے ان ڈو (undo) اور ری ڈو (redo) کی سہولت
- ابعاد میں تبدیلی (drift)، کمی کا تناسب، اور آؤٹ پٹ کا تخمینی سائز
- ملی میٹر، سینٹی میٹر، میٹر، انچ اور فٹ میں پیمائش کا ڈسپلے
- میموری اور جیومیٹری کی سرگرمی سے متعلق میٹرکس (اعداد و شمار) (CPU) (GPU)
- محدود جائزہ (overview) لوڈنگ جب بائنری فائل مقررہ میموری بجٹ سے تجاوز کر جائے (STL)
- GUI اور کمانڈ لائن ایپلی کیشنز
- مقامی پروسیسنگ جس میں اکاؤنٹ، ٹیلی میٹری، اپ لوڈ یا کلاؤڈ پر انحصار کی ضرورت نہیں

## جیومیٹری کو کم کرنے سے پہلے اس کا معائنہ کریں۔

شیڈڈ ڈسپلے سطح اور سلائیٹ کا صاف نظارہ فراہم کرتا ہے۔ یہ موازنہ کرنے کے لیے مفید ہے۔
اصلاحی پاس کو لاگو کرنے سے پہلے شکل کا تحفظ۔

! (MeshMill)

عمودی ڈسپلے اصل پوائنٹ کی تقسیم کو ظاہر کرتا ہے۔ گھنے اسکین والے علاقے، ویرل علاقے، اور
نمونے لینے میں اچانک تبدیلیاں جیومیٹری کو تبدیل کیے بغیر نظر آتی ہیں۔ توسیع شدہ میٹرکس پینل
میش کے ساتھ کام کرتے ہوئے CPU، میموری، GPU، اور جیومیٹری پروسیسنگ کی سرگرمی کو ٹریک کرتا ہے۔

! (MeshMill)

وائر فریم ڈسپلے مثلث کی ساخت کو براہ راست دکھاتا ہے۔ یہ غیر ضروری کثافت کی شناخت میں مدد کرتا ہے،
فاسد مثلث، اور وہ علاقے جہاں سادگی کافی جیومیٹری کو ہٹا سکتی ہے۔

! (MeshMill)

## میش کثافت کا تجزیہ کریں۔

کثافت ڈسپلے پورے ماڈل میں متعلقہ مقامی کثافت کا نقشہ بناتا ہے۔ ویران علاقے ٹھنڈے رہتے ہیں۔
تیزی سے گھنے علاقے روشن رنگوں سے گزرتے ہیں، جس سے ناہموار نمونے لینے کو ایک نظر میں نظر آتا ہے۔

! (MeshMill)

عارضی اصلاح کا جائزہ لیتے وقت کثافت دستیاب رہتی ہے۔ ٹول باکس رپورٹ کرتا ہے۔
الگورتھم، ہدف، نتیجے میں مثلث اور عمودی شمار، کمی فیصد، طول و عرض، اور
پاس لاگو ہونے سے پہلے تخمینہ شدہ آؤٹ پٹ سائز۔

![MeshMill Density ڈسپلے ایک عارضی اصلاح دکھا رہا ہے]

سرکلر میگنیفائر کے ذریعے کسی علاقے کا معائنہ کرنے کے لیے ماؤس کے دائیں بٹن کو تھامیں۔ بڑھا ہوا نظارہ
پوائنٹر پر مرکوز رہتا ہے اور کیمرہ کی مرکزی پوزیشن کو تبدیل کیے بغیر مقامی کثافت کو ظاہر کرتا ہے۔

![ویو پورٹ میگنیفائر کے ساتھ میش مل کثافت ڈسپلے] (MeshMill)

## ویو کنٹرولز (View controls)

| ان پٹ | عمل |
| --- | --- |
| مڈل ڈریگ (Middle-drag) | مدار میں گھمانا (Orbit) |
| Shift + مڈل ڈریگ | پین (Pan) |
| ماؤس کا پہیہ (Mouse wheel) | پوائنٹر کی جانب زوم کرنا |
| Ctrl + ماؤس کا پہیہ | گھڑی کی سمت یا مخالف سمت گھمانا |
| تیر والی کیز (Arrow keys) | ویو سینٹر (view center) کے گرد گھومنا |
| Ctrl + تیر والی کیز | پین (Pan) |
| Ctrl + Shift + اوپر/نیچے (Up/Down) | زوم (Zoom) |
| Ctrl + Shift + Left/Right | رول |
| `F1` / `F2` / `F3` / `F4` | سایہ دار / کثافت / وائر فریم / عمودی |
| دائیں ماؤس ہولڈ | میگنیفائر |
| شفٹ + بائیں کلک | رولر پوائنٹس شامل کریں یا ہٹا دیں |
| Ctrl + بائیں گھسیٹیں | ایک انتخابی کثیرالاضلاع بنائیں |
| `Ctrl+C` | محفوظ کردہ انتخاب میں کثیرالاضلاع شامل کریں |
| `Ctrl+X` | انتخاب کے لیے تراشیں |
| `Ctrl+Space` | انتخاب کو بہتر بنائیں |
| `Delete` | انتخاب کو حذف کریں |
| `Escape` | فعال انتخاب یا حکمران کو صاف کریں |
| `Ctrl+Z` / `Ctrl+Y` | کالعدم / دوبارہ کریں |
| `Ctrl+S` | موجودہ میش حالت کو محفوظ کریں |

معیاری ویو کیز چھ کلیدی نیویگیشن بلاک کی پیروی کرتی ہیں:

| کلید | دیکھیں | Ctrl + کلید |
| --- | --- | --- |
| `Insert` | بائیں | موجودہ واقفیت کو بائیں کے طور پر سیٹ کریں |
| `Home` | سامنے | موجودہ واقفیت کو فرنٹ کے طور پر سیٹ کریں |
| `Page Up` | دائیں | موجودہ واقفیت کو دائیں کے طور پر سیٹ کریں |
| `Delete` | جب کوئی انتخاب موجود نہ ہو تو اوپر | موجودہ واقفیت کو ٹاپ کے طور پر سیٹ کریں |
| `End` | واپس | موجودہ واقفیت کو بطور واپس سیٹ کریں |
| `Page Down` | نیچے | موجودہ واقفیت کو نیچے کے طور پر سیٹ کریں |

کسی منظر کو محفوظ کرنے سے اس کے مخالف منظر کو بھی اپ ڈیٹ کیا جاتا ہے۔ بائیں اور دائیں، سامنے اور پیچھے، اور اوپر اور نیچے
جوڑا رہنا. تصدیقی ڈائیلاگ میں، **محفوظ کریں** پہلے سے طے شدہ عمل ہے، لہذا Enter محفوظ کرتا ہے۔
واقفیت اوپر اور نیچے دونوں نظاروں کے اوپر فرنٹ ظاہر ہوتا ہے۔

شارٹ کٹس کو سیٹنگز میں تبدیل یا ری سیٹ کیا جا سکتا ہے۔

## سلیکشن ورک فلو

کثیرالاضلاع کھینچنے کے لیے Ctrl کو دبائے رکھیں اور بائیں گھسیٹیں۔ اس کی شکل بدلنے کے لیے کونوں کو گھسیٹیں، ایک کو شامل کرنے کے لیے ایک کنارے پر بائیں طرف کلک کریں۔
پوائنٹ، یا کسی کنارے کو ہٹانے کے لیے دائیں کلک کریں۔ `Ctrl+C` کے ساتھ مزید علاقے شامل کریں۔ کیمرے کو منتقل کرنے سے چھپ جاتا ہے۔
منتخب جیومیٹری کو برقرار رکھتے ہوئے اسکرین اسپیس کا کثیرالاضلاع۔

ایک فعال انتخاب کے ساتھ اصلاح صرف اس انتخاب کو متاثر کرتی ہے۔ نتیجہ عارضی رہتا ہے۔
**درخواست** منتخب ہونے تک۔ **منسوخ** عارضی نتیجہ کو مسترد کرتا ہے اور انتخاب کو برقرار رکھتا ہے۔
ایک اور ترتیب کو آزمایا جا سکتا ہے۔ کاٹنا اور حذف کرنا معمول کے ناقابل عمل میش ایڈیٹس بن جاتا ہے۔

سلیکشن پینل مجموعی طور پر منتخب کردہ چوٹیوں، مثلثوں، میش شیئر، تخمینہ کی رپورٹ کرتا ہے۔
سائز، اور طول و عرض. اس کے اعمال تراشتے ہیں، شامل کرتے ہیں، بہتر بناتے ہیں، حذف کرتے ہیں، پیچھے ہٹتے ہیں، یا برقرار رکھے ہوئے کو صاف کرتے ہیں۔
ارد گرد کے جیومیٹری کو چھپائے بغیر انتخاب۔

! (MeshMill)

## بڑی جالیاں

بائنری STL مختص کرنے سے پہلے، MeshMill اپنی تخمینی ورکنگ میموری کا موازنہ کنفیگر شدہ کے ساتھ کرتا ہے۔
میموری بجٹ. بجٹ کے اوپر ایک فائل ایک پابند، صرف پڑھنے کے جائزہ کے طور پر کھلتی ہے۔ جائزہ رپورٹس
مکمل ماخذ مثلث شمار لیکن ترمیم اور برآمد کو غیر فعال کرتا ہے کیونکہ یہ ایک نمونہ ہے، مکمل نہیں۔
اعتراض انڈیکسڈ، زوم پر منحصر آؤٹ آف کور پروسیسنگ کی منصوبہ بندی کی گئی ہے۔
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md)۔

## کمانڈ لائن

`MeshMillCLI.exe` دونوں ریلیز پیکجوں میں شامل ہے:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

تمام اختیارات کے لیے `.\MeshMillCLI.exe --help` چلائیں۔ MeshMill اپنی ان پٹ فائل کو اوور رائٹ کرنے سے انکار کرتا ہے۔

## نمونہ جیومیٹری

ترقی کے نمونے کے دو ورژن دستیاب ہیں۔ نمونہ کے ساتھ ایک جامع میش ہے ۔
بے کار جیومیٹری اور مختلف کثافت کی جان بوجھ کر تہہ۔ یہ سکینر کے بغیر لوگوں کو دیتا ہے۔
الگورتھم کا موازنہ کرنے، کثافت کا معائنہ کرنے، علاقائی آپریشنز کی مشق کرنے کے لیے حقیقت پسندانہ حقیقت،
اور روڈ میپ کی خصوصیات تیار کرنا۔ MeshMill کو اسکین شدہ ان پٹ کی ضرورت نہیں ہے۔

| فائل | مثلث | سائز | ڈلیوری | کے لیے بہترین |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 11.9 MiB | نارمل گٹ | فوری تشخیص، CI، اور کنٹرول سیکھنا |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196.8 ایم آئی بی | Git LFS | گھنے ماخذ جیومیٹری اور بڑے میش کارکردگی کی جانچ |

چھوٹے نمونے کو ہر عام کلون کے ساتھ ڈاؤن لوڈ کیا جاتا ہے۔ اچھوتا اصل اختیاری ہے اور
Git LFS کے ذریعے منظم کیا گیا ہے لہذا یہ عام ذخیرہ کی تاریخ کو نہیں بڑھاتا ہے۔ GitHub ڈیسک ٹاپ پر مشتمل ہے۔
Git LFS کمانڈ لائن صارفین Git LFS انسٹال کر سکتے ہیں اور چلا سکتے ہیں:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

ٹیگ شدہ ریلیز اصل STL کو ان لوگوں کے لیے براہ راست ڈاؤن لوڈ کے طور پر بھی شائع کرتی ہیں جو Git استعمال نہیں کرتے ہیں۔
اصل، طول و عرض اور چیکسم کے لیے [`samples/README.md`](../../../samples/README.md) دیکھیں۔

الگورتھم کے شراکت داروں کو بھی پڑھنا چاہئے۔
[الگورتھم ٹیسٹنگ گائیڈ](docs/ALGORITHM_TESTING.md) کمی کا موازنہ کرنے یا تبدیل کرنے سے پہلے
سلوک

## STL یونٹس

STL کسی یونٹ کو انکوڈ نہیں کرتا ہے۔ ماڈل یونٹس کو تبدیل کرنے سے لیبلز اور پیمائشیں بغیر پیمانہ بدل جاتی ہیں۔
محفوظ کردہ نقاط۔ وہ یونٹ منتخب کریں جو ماخذ جیومیٹری کو بیان کرتی ہے۔

## رازداری

MeshMill مقامی فائلوں کو پڑھتا اور لکھتا ہے۔ اس میں کوئی اکاؤنٹ، ٹیلی میٹری، اپ لوڈ، اشتہار، یا شامل نہیں ہے۔
کلاؤڈ پروسیسنگ کی خصوصیت۔ موجودہ GPU میٹرکس کا نفاذ مقامی Windows کارکردگی کا استعمال کرتا ہے
کاؤنٹر Linux اور macOS کے لیے مساوی مقامی میٹرکس فراہم کنندگان کا منصوبہ بنایا گیا ہے۔

تشخیصی خرابیوں کا سراغ لگانے کے لیے، ڈویلپر اس کے ساتھ GUI شروع کر سکتے ہیں۔
`--diagnostic-log <local-file.jsonl>` لاگ ان پٹ روٹنگ اور کیمرہ اسٹیٹ کو مقامی طور پر ریکارڈ کرتا ہے اور ہے۔
عام استعمال کے دوران غیر فعال.

## ترقی اور رہائی

مقامی UI متن اور دستاویزات ابتدائی طور پر بیرونی مشین ترجمہ کے ساتھ تیار کیے جاتے ہیں۔
خدمات اور ساختی نقصان کے لیے خود بخود جانچ پڑتال کی جاتی ہے۔ مشینی ترجمہ اب بھی ہو سکتا ہے۔
غیر فطری یا غلط۔ مقامی بولنے والوں کو ترجمے کے ذریعے جائزہ لینے اور درست کرنے کی ترغیب دی جاتی ہے۔
شراکت کا عمل.

- [شریک کرنا](CONTRIBUTING.md)
- [ریلیز کا عمل](RELEASING.md)
- [روڈ میپ](ROADMAP.md)
- [ٹربل شوٹنگ](docs/TROUBLESHOOTING.md)
- [فریق ثالث کے نوٹس](THIRD_PARTY_NOTICES.md)

## MeshMill کی حمایت کریں۔

MeshMill آزادانہ طور پر تیار اور برقرار رکھا گیا ہے۔ پڑھیں
[اس کام کی حمایت کیوں اہم ہے](SUPPORT.md)، یا اس کے ذریعے مسلسل ترقی کی حمایت
[مجھے ایک کافی خریدیں](https://buymeacoffee.com/tednv)۔

MeshMill GNU جنرل پبلک لائسنس، ورژن 3 یا اس کے بعد کے تحت لائسنس یافتہ ہے۔ دیکھیں
[`LICENSE`](../../../LICENSE)۔

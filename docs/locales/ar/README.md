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

يُعد MeshMill تطبيقاً سطحياً متخصصاً يهدف إلى جعل التعامل مع هندسة الشبكات (mesh geometry)
أمراً سهلاً وميسوراً، خاصةً تلك الشبكات الضخمة أو الكثيفة أو المعقدة. يوفر التطبيق إمكانيات الفحص السريع، وتحليل الكثافة، وتحديد المناطق، والقص، والحذف،
وتقليل كثافة الشبكة (mesh reduction) بشكل مُحكَم، كل ذلك دون الحاجة إلى إنشاء حساب أو رفع ملفات الهندسة.

يحافظ عرض OpenGL المُسرَّع بواسطة GPU على التنقل في إطار العرض، واختيار الأجهزة، وتصور الكثافة،
والتفتيش التفاعلي سريع الاستجابة. يعمل تقليل الشبكة حاليًا في عمال وحدة المعالجة المركزية الأصليين المنفصلين، (CPU)
إبقاء الحسابات الهندسية الطويلة بعيدًا عن الواجهة.

تعمل MeshMill مع شبكات من الماسحات الضوئية ثلاثية الأبعاد، وCAD وتصدير النماذج، وخطوط أنابيب إعادة الإعمار، (3D)
والأشكال الهندسية المُنشأة برمجياً، ومصادر أخرى خاصة بـ STL. كما يقوم بإعداد البيانات الهندسية لتكون جاهزة لبرامج التحرير اللاحقة،
وأدوات التصنيع، وسير عمل معالجة الشبكات الأخرى. أما مهام النمذجة العامة، والنحت الرقمي، والتحريك،
وإعداد الخامات (materials)، وإنشاء المشاهد، فهي تقع خارج نطاق عمل هذا التطبيق.

## تنزيل

اختر نظام التشغيل الخاص بك. كل حزمة مكتفية ذاتيا. بايثون، Node.js، وغيرها <!-- Python -->
تبعيات التنمية ليست مطلوبة.

| النظام | التنزيل الموصى به | الحالة |
| --- | --- | --- |
| **ويندوز x64** | **[تحميل مثبت الويندوز][windows-installer]** | الإصدار المدعوم | <!-- Windows Windows -->
| ويندوز x64، بدون تثبيت | [تحميل ملف ZIP المحمول][windows-portable] | الإصدار المدعوم | <!-- Windows -->
| لينكس x86- 64 | [تنزيل معاينة لينكس][linux-preview] | معاينة الاختبار المبكر | <!-- Linux Linux -->
| ماك أبل السيليكون | [تحميل معاينة Apple silicon][mac-arm-preview] | معاينة الاختبار المبكر | <!-- macOS -->
| ماك إنتل | [تنزيل معاينة Intel Mac][mac-intel-preview] | معاينة الاختبار المبكر | <!-- macOS -->

**يجب على معظم مستخدمي Windows اختيار برنامج تثبيت Windows.** استخدم ملف ZIP المحمول فقط عندما تفعل ذلك
لا تريد تثبيت MeshMill أو ليس لديك إذن لتثبيت التطبيقات.

تعد حزم Linux وmacOS بمثابة معاينات مبكرة غير موقعة. إنهم يجتازون بنيات أصلية آلية و
اختبارات الدخان المعبأة، ولكنها لا تزال بحاجة إلى اختبار الأجهزة الحقيقية. اقرأ
[ملاحظات معاينة Linux وmacOS](../../PLATFORM_TESTING.md) قبل تثبيتها.

قد يحذر Windows SmartScreen أو macOS Gatekeeper من الحزم غير الموقعة.
تم تضمين نموذج شبكة اختياري مع إصدار Windows المدعوم: [STL][sample-mesh].
تتوفر الإصدارات الأقدم والمجاميع الاختبارية للتنزيل على [إصدارات GitHub][all-releases].

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## البدء السريع

1. افتح STL.
2. افحص النموذج في وضع العرض المظلل (Shaded) أو الكثافة (Density) أو الهيكل السلكي (Wireframe) أو الرؤوس (Vertices).
3. اختر مستوى الجودة والخوارزمية والعدد المستهدف للمثلثات.
4. اختر **Optimize** (تحسين) لحساب النتيجة.
5. قارن بين الشبكات (meshes) الأصلية والمُحسَّنة، ثم اختر **Apply** (تطبيق) لاعتماد العملية.
6. اختر **Save current state** (حفظ الحالة الحالية) أو اضغط على `Ctrl+S`.

لا يبدأ MeshMill عملية التحسين لمجرد تغيير ملف أو إعداد ما.

## القدرات

- إدخال بصيغتي Binary وASCII، وإخراج بصيغة Binary (STL) (STL)
- تقليل البيانات مع الحفاظ على الكثافة والشكل والطوبولوجيا (Fast QEM)
- منفذ عرض OpenGL المُسرَّع بواسطة وحدة معالجة الرسومات، واختيار الأجهزة، وتصور الكثافة (GPU)
- عمال هندسة الخلفية الأصلية لتقليل الشبكة
- أوضاع العرض: المظلل (Shaded)، والكثافة (Density)، والهيكل السلكي (Wireframe)، والرؤوس (Vertex)
- أهداف تلقائية مستمدة من الهندسة (الشكل) بدلاً من حد ثابت لعدد المثلثات
- تحديد المضلعات مع إمكانية التحديد التراكمي لمناطق متعددة
- قص أو حذف أو تحسين المنطقة المحددة فقط
- مقارنة بين الشبكة (mesh) الأصلية والسابقة والحالية (المخزنة مؤقتاً)
- التراجع عن التغييرات الهندسية المعتمدة وإعادة تطبيقها
- انحراف الأبعاد، ونسبة التقليل، وحجم الإخراج التقديري
- وحدات العرض: المليمتر، والسنتيمتر، والمتر، والبوصة، والقدم
- مقاييس البيانات، والذاكرة، والمخرجات، والنشاط الهندسي (CPU) (GPU)
- تحميل نظرة عامة محدودة النطاق عند تجاوز ملف الإدخال لميزانية الذاكرة المحددة (STL)
- تطبيقات بواجهة رسومية (GUI) وتطبيقات سطر الأوامر
- معالجة محلية دون الحاجة إلى حساب مستخدم أو إرسال بيانات (telemetry) أو رفع ملفات أو الاعتماد على السحابة

## افحص الشكل الهندسي قبل تصغيره

توفر الشاشة المظللة رؤية واضحة للسطح والصورة الظلية. ومن المفيد للمقارنة
الحفاظ على الشكل قبل تطبيق تمرير التحسين.

![منفذ العرض المظلل MeshMill يُظهر عينة الشبكة المجمعة](../../images/meshmill-shaded.png)

تعرض شاشة القمم توزيع النقاط الفعلي. مناطق المسح الكثيفة والمناطق المتفرقة و
تظهر التغييرات المفاجئة في أخذ العينات دون تغيير الشكل الهندسي. لوحة المقاييس الموسعة
يتتبع نشاط وحدة المعالجة المركزية والذاكرة ووحدة معالجة الرسومات والهندسة أثناء العمل مع الشبكة. (GPU) (CPU)

![عرض MeshMill Vertices بمقاييس أداء موسعة](../../images/meshmill-vertices.png)

تعرض شاشة Wireframe بنية المثلث مباشرةً. يساعد على تحديد الكثافة غير الضرورية،
التثليث غير المنتظم، والمناطق التي يمكن أن يزيل فيها التبسيط هندسة كبيرة.

![شاشة عرض MeshMill Wireframe تُظهر الاختلاف في كثافة المثلث](../../images/meshmill-wireframe.png)

## تحليل كثافة الشبكة

تقوم شاشة عرض الكثافة بتعيين الكثافة المحلية النسبية عبر النموذج. مناطق متفرقة تبقى باردة بينما
تتحرك المناطق ذات الكثافة المتزايدة عبر الألوان الأكثر سطوعًا، مما يجعل العينات غير المتساوية مرئية في لمحة.

![عرض كثافة MeshMill يوضح كثافة الشبكة النسبية](../../images/meshmill-density.png)

تظل الكثافة متاحة أثناء تقييم التحسين المؤقت. يُبلغ مربع الأدوات عن
الخوارزمية، الهدف، عدد المثلثات والرؤوس الناتجة، نسبة التخفيض، الأبعاد، و
حجم الإخراج المقدر قبل تطبيق التمرير.

![شاشة عرض كثافة MeshMill تعرض تحسينًا مؤقتًا](../../images/meshmill-density-overview.png)

اضغط مع الاستمرار على زر الفأرة الأيمن لتفقد المنطقة من خلال المكبر الدائري. المنظر المكبر
يبقى متمركزًا على المؤشر ويكشف عن الكثافة المحلية دون تغيير موضع الكاميرا الرئيسي.

![عرض كثافة MeshMill مع مكبر إطار العرض](../../images/meshmill-density-zoom.png)

## عناصر التحكم في العرض

| الإدخال | الإجراء |
| --- | --- |
| السحب بزر الفأرة الأوسط | الدوران (Orbit) |
| Shift + السحب بزر الفأرة الأوسط | التحريك (Pan) |
| عجلة الفأرة | التكبير/التصغير باتجاه المؤشر |
| Ctrl + عجلة الفأرة | التدوير مع عقارب الساعة أو عكسها |
| مفاتيح الأسهم | الدوران حول مركز العرض |
| Ctrl + مفاتيح الأسهم | التحريك (Pan) |
| Ctrl + Shift + سهم لأعلى/لأسفل | التكبير/التصغير |
| Ctrl + Shift + سهم لليسار/لليمين | تدوير (Roll) |
| `F1` / `F2` / `F3` / `F4` | تظليل / كثافة / هيكل سلكي / رؤوس |
| الضغط المستمر بزر الفأرة الأيمن | أداة التكبير |
| Shift + النقر بزر الفأرة الأيسر | إضافة أو إزالة نقاط المسطرة |
| Ctrl + السحب بزر الفأرة الأيسر | رسم مضلع التحديد |
| `Ctrl+C` | إضافة المضلع إلى التحديد المحفوظ |
| `Ctrl+X` | القص حسب التحديد |
| `Ctrl+Space` | تحسين التحديد |
| `Delete` | حذف التحديد |
| `Escape` | مسح التحديد النشط أو المسطرة |
| `Ctrl+Z` / `Ctrl+Y` | تراجع / إعادة |
| `Ctrl+S` | حفظ حالة الشبكة (Mesh) الحالية |

تتبع مفاتيح العرض القياسية مجموعة مفاتيح التنقل المكونة من ستة مفاتيح:

| المفتاح | العرض | Ctrl + المفتاح |
| --- | --- | --- |
| `Insert` | يسار | تعيين الاتجاه الحالي كـ "يسار" |
| `Home` | أمامي | تعيين الاتجاه الحالي كاتجاه أمامي |
| `Page Up` | أيمن | تعيين الاتجاه الحالي كاتجاه أيمن |
| `Delete` | علوي (عند عدم وجود تحديد) | تعيين الاتجاه الحالي كاتجاه علوي |
| `End` | خلفي | تعيين الاتجاه الحالي كاتجاه خلفي |
| `Page Down` | سفلي | تعيين الاتجاه الحالي كاتجاه سفلي |

يؤدي حفظ العرض أيضًا إلى تحديث العرض المقابل له؛ حيث تظل كل من الأوضاع (أيسر/أيمن)، و(أمامي/خلفي)، و(علوي/سفلي)
مقترنة ببعضها. في مربع حوار التأكيد، يكون خيار **حفظ (Save)** هو الإجراء الافتراضي، لذا فإن الضغط على مفتاح Enter يحفظ
الاتجاه. يظهر الاتجاه الأمامي في الجزء العلوي من كل من العرضين العلوي والسفلي.

يمكن تغيير الاختصارات أو إعادة تعيينها من خلال الإعدادات.

## سير عمل التحديد

اضغط باستمرار على مفتاح Ctrl واسحب بزر الفأرة الأيسر لرسم مضلع. اسحب الزوايا لتغيير شكل المضلع، وانقر بزر الفأرة الأيسر على أحد الأضلاع لإضافة
نقطة، أو انقر بزر الفأرة الأيمن على الضلع لإزالة نقطة. أضف المزيد من المناطق باستخدام `Ctrl+C`. يؤدي تحريك الكاميرا إلى إخفاء
المضلع المرتبط بمساحة الشاشة مع الاحتفاظ بالعناصر الهندسية المحددة.

تؤثر عملية التحسين -عند وجود تحديد نشط- على ذلك التحديد فقط. وتظل النتيجة مؤقتة
إلى حين اختيار **تطبيق (Apply)**. يؤدي خيار **إلغاء (Cancel)** إلى تجاهل النتيجة المؤقتة والاحتفاظ بالتحديد،
مما يتيح تجربة إعداد آخر. وتصبح عمليات القص والحذف بمثابة تعديلات عادية على الشبكة (mesh) يمكن التراجع عنها.

تُبلغ لوحة التحديد عن القمم المحددة التراكمية والمثلثات وحصة الشبكة المقدرة
الحجم والأبعاد. يتم اقتصاص إجراءاتها أو إضافتها أو تحسينها أو حذفها أو التراجع عنها أو مسح ما تم الاحتفاظ به
التحديد دون إخفاء الهندسة المحيطة.

![MeshMill يُظهر التحديد الإقليمي المحتفظ به وإحصائيات الشكل الهندسي الخاصة به](../../images/meshmill-crop-selection.png)

## الشبكات الكبيرة

قبل تخصيص موارد لـ STL، يقوم MeshMill بمقارنة الذاكرة التشغيلية المقدرة بـ
ميزانية الذاكرة المحددة. يُفتح الملف الذي يتجاوز الميزانية كعرض عام (overview) محدود للقراءة فقط. ويوضح هذا العرض
العدد الكامل للمثلثات في المصدر الأصلي، ولكنه يعطل التحرير والتصدير لأنه يمثل عينة وليس
الكائن الكامل. ومن المخطط دعم المعالجة المفهرسة والمعتمدة على مستوى التكبير (zoom-dependent) والتي لا تتطلب تحميل البيانات بالكامل في الذاكرة (out-of-core processing) في
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## سطر الأوامر

يتم تضمين `MeshMillCLI.exe` في كلتا حزمتي الإصدار:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

قم بتشغيل `.\MeshMillCLI.exe --help` للاطلاع على كافة الخيارات. يرفض MeshMill الكتابة فوق ملف الإدخال الخاص به.

## عينة هندسية

تتوفر نسختان من عينة التطوير. العينة عبارة عن شبكة مركبة تحتوي على
طبقات متعمدة من الهندسة المكررة وكثافة متفاوتة. وهي توفر للأشخاص الذين لا يملكون ماسحاً ضوئياً
نموذجاً واقعياً لمقارنة الخوارزميات، وفحص الكثافة، وتجربة العمليات الإقليمية (المحلية)،
وتطوير ميزات خارطة الطريق. لا يتطلب MeshMill بيانات إدخال ممسوحة ضوئياً.

| الملف | المثلثات | الحجم | طريقة التنزيل | الأنسب لـ |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 11.9 ميجابايت | Git عادي | التقييم السريع، والتكامل المستمر (CI)، وتعلم عناصر التحكم |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196.8 ميجا بايت | Git LFS | اختبار هندسة المصدر الكثيف وأداء الشبكة الكبيرة |

يتم تنزيل العينة الأصغر مع كل نسخة عادية. الأصل الذي لم يمسه هو اختياري و
تتم إدارتها من خلال Git LFS بحيث لا تؤدي إلى تضخيم سجل المستودع العادي. يتضمن سطح المكتب GitHub
Git LFS. يمكن لمستخدمي سطر الأوامر تثبيت Git LFS وتشغيل:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

تنشر الإصدارات الموسومة أيضًا STL الأصلي كتنزيل مباشر للأشخاص الذين لا يستخدمون Git.
راجع [`samples/README.md`](../../../samples/README.md) لمعرفة المصدر والأبعاد والمجاميع الاختبارية.

يجب على المساهمين في الخوارزمية أيضًا قراءة
[دليل اختبار الخوارزمية] (docs/ALGORITHM_TESTING.md) قبل مقارنة التخفيض أو تغييره
السلوك.

## وحدات STL

STL لا يقوم بتشفير الوحدة. يؤدي تغيير وحدات النموذج إلى تغيير التسميات والقياسات دون تغيير الحجم
الإحداثيات المحفوظة. حدد الوحدة التي تصف هندسة المصدر.

## الخصوصية

يقوم MeshMill بقراءة وكتابة الملفات المحلية. لا يحتوي على أي حساب أو قياس عن بعد أو تحميل أو إعلان أو
ميزة المعالجة السحابية. يستخدم تطبيق مقاييس GPU الحالي أداء Windows المحلي
عدادات. تم التخطيط لموفري المقاييس الأصلية المكافئين لـ Linux وmacOS.

لاستكشاف الأخطاء وإصلاحها التشخيصية، يمكن للمطورين بدء تشغيل واجهة المستخدم الرسومية باستخدام
`--diagnostic-log <local-file.jsonl>`. يسجل السجل توجيه الإدخال وحالة الكاميرا محليًا
تعطيل أثناء الاستخدام العادي.

## التطوير والإفراج

يتم إنتاج نص ووثائق واجهة المستخدم المترجمة في البداية باستخدام ترجمة آلية خارجية
الخدمات والتحقق تلقائيا من الأضرار الهيكلية. الترجمة الآلية لا تزال متاحة
غير طبيعي أو غير صحيح. يتم تشجيع المتحدثين الأصليين على مراجعة الترجمات وتصحيحها من خلال
عملية المساهمة.

- [مساهمة](CONTRIBUTING.md)
- [عملية الإصدار](RELEASING.md)
- [خريطة الطريق](ROADMAP.md)
- [استكشاف الأخطاء وإصلاحها](docs/TROUBLESHOOTING.md)
- [إشعارات الطرف الثالث](THIRD_PARTY_NOTICES.md)

## دعم MeshMill

تم تطوير وصيانة MeshMill بشكل مستقل. اقرأ
[لماذا يهم دعم هذا العمل](SUPPORT.md)، أو دعم التطوير المستمر من خلال
[اشتري لي قهوة](https://buymeacoffee.com/tednv).

MeshMill مرخص بموجب رخصة جنو العامة، الإصدار 3 أو الأحدث. انظر
[`LICENSE`](../../../LICENSE).

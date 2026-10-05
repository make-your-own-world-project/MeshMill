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

MeshMill เป็นแอปพลิเคชันบนเดสก์ท็อปที่ออกแบบมาเพื่อจัดการกับรูปทรงตาข่าย (mesh geometry)
ที่มีขนาดใหญ่เกินไป มีความหนาแน่นสูง หรือมีความซับซ้อน ให้สามารถจัดการได้ง่ายขึ้น โดยรองรับการตรวจสอบอย่างรวดเร็ว การวิเคราะห์ความหนาแน่น การเลือกพื้นที่เฉพาะ การตัดส่วนเกิน การลบ
และการลดจำนวนตาข่าย (mesh reduction) แบบควบคุมได้ โดยไม่จำเป็นต้องมีบัญชีผู้ใช้หรืออัปโหลดข้อมูลรูปทรงขึ้นระบบ

การเรนเดอร์ OpenGL ที่เร่งด้วย GPU ช่วยให้การนำทางวิวพอร์ต การเลือกฮาร์ดแวร์ การแสดงภาพความหนาแน่น
และการตอบสนองการตรวจสอบเชิงโต้ตอบ การลดตาข่ายปัจจุบันทำงานในผู้ปฏิบัติงาน CPU ดั้งเดิมที่แยกจากกัน
ทำให้การคำนวณทางเรขาคณิตแบบยาวอยู่ห่างจากอินเทอร์เฟซ

MeshMill ทำงานร่วมกับตาข่ายจากเครื่องสแกน 3D, CAD และการส่งออกการสร้างแบบจำลอง ท่อส่งการก่อสร้างใหม่
รูปทรงที่สร้างขึ้นด้วยโปรแกรม และแหล่งข้อมูลอื่นๆ ที่เข้ากันได้กับ STL โปรแกรมนี้ช่วยเตรียมข้อมูลรูปทรงสำหรับนำไปใช้ในขั้นตอนถัดไป
เช่น เครื่องมือสำหรับการผลิต และเวิร์กโฟลว์อื่นๆ ที่เกี่ยวข้องกับตาข่าย ทั้งนี้ ฟังก์ชันการสร้างโมเดลทั่วไป การปั้นโมเดล (sculpting) แอนิเมชัน
การกำหนดวัสดุ และการสร้างฉาก (scene creation) ไม่รวมอยู่ในขอบเขตการทำงานของโปรแกรมนี้

## ดาวน์โหลด

เลือกระบบปฏิบัติการของคุณ ทุกแพ็คเกจมีอยู่ในตัวเอง Python, Node.js และอื่นๆ
ไม่จำเป็นต้องพึ่งพาการพัฒนา

| ระบบ | แนะนำดาวน์โหลด | สถานะ |
| --- | --- | --- |
| **วินโดวส์ x64** | **[ดาวน์โหลดตัวติดตั้ง Windows][windows-installer]** | รุ่นที่รองรับ | <!-- Windows -->
| Windows x64 ไม่มีการติดตั้ง | [ดาวน์โหลด ZIP แบบพกพา][windows-portable] | รุ่นที่รองรับ |
| Linux x86-64 | [ดาวน์โหลดตัวอย่าง Linux][linux-preview] | ตัวอย่างการทดสอบเบื้องต้น |
| macOS แอปเปิ้ลซิลิคอน | [ดาวน์โหลดตัวอย่าง Apple Silicon][mac-arm-preview] | ตัวอย่างการทดสอบเบื้องต้น |
| macOS อินเทล | [ดาวน์โหลดตัวอย่าง Intel Mac][mac-intel-preview] | ตัวอย่างการทดสอบเบื้องต้น |

**ผู้ใช้ Windows ส่วนใหญ่ควรเลือกตัวติดตั้ง Windows** ใช้ ZIP แบบพกพาเฉพาะเมื่อคุณเลือกเท่านั้น
ไม่ต้องการติดตั้ง MeshMill หรือไม่ได้รับอนุญาตให้ติดตั้งแอปพลิเคชัน

แพ็คเกจ Linux และ macOS เป็นตัวอย่างก่อนกำหนดที่ไม่ได้ลงนาม พวกเขาผ่านการสร้างเนทิฟอัตโนมัติและ
การทดสอบควันแบบแพ็กเกจ แต่ยังต้องมีการทดสอบฮาร์ดแวร์จริง อ่าน
[บันทึกการแสดงตัวอย่าง Linux และ macOS](../../PLATFORM_TESTING.md) ก่อนทำการติดตั้ง

Windows SmartScreen หรือ macOS Gatekeeper อาจเตือนเกี่ยวกับแพ็คเกจที่ไม่ได้ลงนาม
ตัวอย่าง mesh ที่เป็นตัวเลือกจะรวมอยู่ใน Windows รุ่นที่รองรับ: [STL][sample-mesh]
เวอร์ชันเก่าและการตรวจสอบการดาวน์โหลดมีอยู่ใน [GitHub Releases][all-releases]

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## การเริ่มต้นใช้งานอย่างรวดเร็ว

1. เปิด STL ขึ้นมา
2. ตรวจสอบชิ้นงานในโหมดการแสดงผลแบบ Shaded, Density, Wireframe หรือ Vertices
3. เลือกระดับคุณภาพ อัลกอริทึม และจำนวนรูปสามเหลี่ยม (triangle count) ที่ต้องการ
4. เลือก **Optimize** เพื่อคำนวณผลลัพธ์
5. เปรียบเทียบ mesh ต้นฉบับกับ mesh ที่ผ่านการปรับปรุงประสิทธิภาพแล้ว จากนั้นเลือก **Apply** เพื่อยืนยันการดำเนินการ
6. เลือก **Save current state** หรือกด `Ctrl+S`

MeshMill จะไม่เริ่มกระบวนการปรับปรุงประสิทธิภาพเพียงเพราะมีการเปลี่ยนแปลงไฟล์หรือการตั้งค่าเท่านั้น

## ขีดความสามารถ

- รองรับอินพุต STL ทั้งรูปแบบ Binary และ ASCII และเอาต์พุต STL แบบ Binary
- การลดทอนข้อมูล Fast QEM โดยรักษาสมดุลความหนาแน่น รูปทรง และโทโพโลยี
- วิวพอร์ต OpenGL ที่เร่งด้วย GPU การเลือกฮาร์ดแวร์ และการแสดงภาพความหนาแน่น
- ผู้ปฏิบัติงานเรขาคณิตพื้นหลังดั้งเดิมสำหรับการลดตาข่าย
- โหมดการแสดงผลแบบ Shaded, Density, Wireframe และ Vertex
- กำหนดเป้าหมายอัตโนมัติโดยอิงจากรูปทรงเรขาคณิต แทนการกำหนดจำนวนสามเหลี่ยมสูงสุดแบบตายตัว
- การเลือกรูปหลายเหลี่ยม (Polygon) พร้อมความสามารถในการเลือกหลายพื้นที่แบบสะสม
- ตัด (Crop) ลบ หรือปรับปรุงประสิทธิภาพ (Optimize) เฉพาะพื้นที่ที่เลือก
- เปรียบเทียบ Mesh ต้นฉบับ, Mesh ก่อนหน้า และ Mesh ปัจจุบันที่เก็บไว้ในแคช
- ยกเลิก (Undo) และทำซ้ำ (Redo) การเปลี่ยนแปลงรูปทรงเรขาคณิตที่ยืนยันแล้ว
- แสดงค่าความคลาดเคลื่อนของมิติ (Dimension drift) เปอร์เซ็นต์การลดทอน และขนาดเอาต์พุตโดยประมาณ
- หน่วยแสดงผลแบบมิลลิเมตร เซนติเมตร เมตร นิ้ว และฟุต
- ตัวชี้วัดข้อมูล CPU, หน่วยความจำ, GPU และกิจกรรมเกี่ยวกับรูปทรงเรขาคณิต
- การโหลดภาพรวมแบบจำกัดขอบเขต เมื่อไฟล์ STL (Binary) มีขนาดเกินกว่างบประมาณหน่วยความจำที่กำหนดไว้
- แอปพลิเคชันทั้งแบบ GUI และ Command-line
- ประมวลผลภายในเครื่องโดยไม่ต้องใช้บัญชีผู้ใช้ ไม่มีการส่งข้อมูลทางไกล (Telemetry) ไม่ต้องอัปโหลด และไม่ขึ้นกับระบบคลาวด์

## ตรวจสอบรูปทรงก่อนที่จะลดขนาดลง

จอแสดงผลแบบแรเงาให้มุมมองที่สะอาดตาของพื้นผิวและภาพเงา เป็นประโยชน์ในการเปรียบเทียบ
การเก็บรักษารูปร่างก่อนที่จะใช้บัตรผ่านการปรับให้เหมาะสม

![วิวพอร์ตที่แรเงา MeshMill แสดง mesh ตัวอย่างที่รวมมา](../../images/meshmill-shaded.png)

จอแสดงผล Vertices จะแสดงการกระจายจุดตามจริง ขอบเขตการสแกนหนาแน่น พื้นที่กระจัดกระจาย และ
การเปลี่ยนแปลงอย่างฉับพลันในการสุ่มตัวอย่างสามารถมองเห็นได้โดยไม่ต้องเปลี่ยนรูปทรงเรขาคณิต แผงเมตริกที่ขยาย
ติดตามกิจกรรม CPU, หน่วยความจำ, GPU และการประมวลผลทางเรขาคณิตในขณะที่ทำงานกับเมช

![MeshMill Vertices แสดงผลพร้อมการวัดประสิทธิภาพที่ขยาย](../../images/meshmill-vertices.png)

จอแสดงผล Wireframe จะแสดงโครงสร้างสามเหลี่ยมโดยตรง ช่วยระบุความหนาแน่นที่ไม่จำเป็น
สามเหลี่ยมที่ไม่ปกติ และบริเวณที่การทำให้ง่ายขึ้นสามารถลบรูปทรงเรขาคณิตที่สำคัญได้

![จอแสดงผล MeshMill Wireframe แสดงความแปรผันของความหนาแน่นของสามเหลี่ยม](../../images/meshmill-wireframe.png)

## วิเคราะห์ความหนาแน่นของตาข่าย

การแสดงความหนาแน่นจะแมปความหนาแน่นเฉพาะที่สัมพัทธ์ในแบบจำลอง พื้นที่กระจัดกระจายยังคงเย็นในขณะที่
บริเวณที่มีความหนาแน่นมากขึ้นจะเคลื่อนที่ผ่านสีที่สว่างกว่า ทำให้มองเห็นตัวอย่างที่ไม่สม่ำเสมอได้อย่างรวดเร็ว

![จอแสดงผลความหนาแน่นของ MeshMill แสดงความหนาแน่นของตาข่ายสัมพัทธ์](../../images/meshmill-density.png)

ความหนาแน่นยังคงมีอยู่ในขณะที่ประเมินการปรับให้เหมาะสมชั่วคราว กล่องเครื่องมือรายงาน
อัลกอริธึม เป้าหมาย การนับสามเหลี่ยมและจุดยอดผลลัพธ์ เปอร์เซ็นต์การลด ขนาด และ
ขนาดเอาต์พุตโดยประมาณก่อนใช้พาส

![การแสดงผลความหนาแน่นของ MeshMill แสดงการปรับให้เหมาะสมชั่วคราว](../../images/meshmill-density-overview.png)

กดปุ่มเมาส์ขวาค้างไว้เพื่อตรวจสอบพื้นที่ผ่านแว่นขยายแบบวงกลม มุมมองที่ขยาย
จะอยู่ตรงกลางตัวชี้และแสดงความหนาแน่นในพื้นที่โดยไม่ต้องเปลี่ยนตำแหน่งกล้องหลัก

![การแสดงความหนาแน่นของ MeshMill พร้อมแว่นขยายวิวพอร์ต](../../images/meshmill-density-zoom.png)

## การควบคุมมุมมอง

| อินพุต | การทำงาน |
| --- | --- |
| ลากด้วยปุ่มกลางเมาส์ | หมุนมุมมอง (Orbit) |
| Shift + ลากด้วยปุ่มกลางเมาส์ | เลื่อนมุมมอง (Pan) |
| ลูกกลิ้งเมาส์ | ซูมเข้า/ออกไปยังตำแหน่งตัวชี้เมาส์ |
| Ctrl + ลูกกลิ้งเมาส์ | หมุนตามเข็มหรือทวนเข็มนาฬิกา |
| ปุ่มลูกศร | หมุนมุมมองรอบจุดศูนย์กลางของมุมมอง |
| Ctrl + ปุ่มลูกศร | เลื่อนมุมมอง (Pan) |
| Ctrl + Shift + ขึ้น/ลง | ซูม |
| Ctrl + Shift + ซ้าย/ขวา | ม้วน |
| `F1` / `F2` / `F3` / `F4` | แรเงา / ความหนาแน่น / โครงร่าง / จุดยอด |
| กดเมาส์ขวา | แว่นขยาย |
| Shift + คลิกซ้าย | เพิ่มหรือลบจุดไม้บรรทัด |
| Ctrl + ลากซ้าย | วาดรูปหลายเหลี่ยมแบบเลือก |
| `Ctrl+C` | เพิ่มรูปหลายเหลี่ยมในส่วนที่เลือกที่บันทึกไว้ |
| `Ctrl+X` | ครอบตัดส่วนที่เลือก |
| `Ctrl+Space` | ปรับการเลือกให้เหมาะสม |
| `Delete` | ลบส่วนที่เลือก |
| `Escape` | ล้างส่วนที่เลือกหรือไม้บรรทัดที่ใช้งานอยู่ |
| `Ctrl+Z` / `Ctrl+Y` | เลิกทำ / ทำซ้ำ |
| `Ctrl+S` | บันทึกสถานะตาข่ายปัจจุบัน |

ปุ่มมุมมองมาตรฐานเป็นไปตามบล็อกการนำทางหกปุ่ม:

| คีย์ | ดู | Ctrl + ปุ่ม |
| --- | --- | --- |
| `Insert` | ซ้าย | ตั้งค่าการวางแนวปัจจุบันเป็นซ้าย |
| `Home` | ด้านหน้า | ตั้งค่าการวางแนวปัจจุบันเป็น Front |
| `Page Up` | ขวา | ตั้งค่าการวางแนวปัจจุบันเป็นขวา |
| `Delete` | บนสุดเมื่อไม่มีการเลือก | ตั้งค่าการวางแนวปัจจุบันเป็นด้านบน |
| `End` | กลับ | ตั้งค่าการวางแนวปัจจุบันเป็น กลับ |
| `Page Down` | ด้านล่าง | ตั้งค่าการวางแนวปัจจุบันเป็นด้านล่าง |

การบันทึกมุมมองยังอัปเดตมุมมองตรงกันข้ามด้วย ซ้ายและขวา หน้าและหลัง และบนและล่าง
ยังคงจับคู่กัน ในกล่องโต้ตอบการยืนยัน **บันทึก** คือการดำเนินการเริ่มต้น ดังนั้น Enter จะบันทึก
ปฐมนิเทศ ด้านหน้าปรากฏที่ด้านบนของทั้งมุมมองด้านบนและด้านล่าง

ทางลัดสามารถเปลี่ยนแปลงหรือรีเซ็ตได้ในการตั้งค่า

## ขั้นตอนการคัดเลือก

กด Ctrl ค้างไว้แล้วลากซ้ายเพื่อวาดรูปหลายเหลี่ยม ลากมุมเพื่อปรับรูปร่าง คลิกซ้ายที่ขอบเพื่อเพิ่ม
ชี้หรือคลิกขวาที่ขอบเพื่อลบออก เพิ่มภูมิภาคด้วย `Ctrl+C` การเคลื่อนย้ายที่ซ่อนกล้อง
รูปหลายเหลี่ยมพื้นที่หน้าจอในขณะที่ยังคงรูปทรงที่เลือกไว้

การเพิ่มประสิทธิภาพด้วยการเลือกที่ใช้งานอยู่จะส่งผลต่อการเลือกนั้นเท่านั้น ผลลัพธ์ยังคงเป็นแบบชั่วคราว
จนกว่าจะเลือก **สมัคร** **ยกเลิก** ละทิ้งผลลัพธ์ชั่วคราวและคงการเลือกไว้เช่นนั้น
สามารถลองใช้การกำหนดค่าอื่นได้ การดำเนินการครอบตัดและลบกลายเป็นการแก้ไขเมชตามปกติที่ไม่สามารถยกเลิกได้

แผงการเลือกจะรายงานจุดยอดที่เลือกสะสม สามเหลี่ยม ส่วนแบ่งเมช โดยประมาณ
ขนาดและมิติข้อมูล การดำเนินการครอบตัด เพิ่ม เพิ่มประสิทธิภาพ ลบ ถอยกลับ หรือล้างข้อมูลที่เก็บไว้
การเลือกโดยไม่ซ่อนรูปทรงเรขาคณิตโดยรอบ

![MeshMill แสดงการเลือกภูมิภาคที่ยังคงอยู่และสถิติทางเรขาคณิต](../../images/meshmill-crop-selection.png)

## ตาข่ายขนาดใหญ่

ก่อนที่จะจัดสรรไบนารี STL นั้น MeshMill จะเปรียบเทียบหน่วยความจำการทำงานโดยประมาณกับที่กำหนดค่าไว้
งบประมาณหน่วยความจำ ไฟล์ที่สูงกว่างบประมาณจะเปิดเป็นภาพรวมแบบมีขอบเขตแบบอ่านอย่างเดียว รายงานภาพรวม
จำนวนสามเหลี่ยมแหล่งที่มาเต็ม แต่ปิดใช้งานการแก้ไขและส่งออกเนื่องจากเป็นตัวอย่าง ไม่ใช่ทั้งหมด
วัตถุ มีการวางแผนการประมวลผลนอกคอร์ที่ขึ้นอยู่กับการซูมตามดัชนี
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md)

## บรรทัดคำสั่ง

`MeshMillCLI.exe` รวมอยู่ในแพ็คเกจการเปิดตัวทั้งสอง:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

รัน `.\MeshMillCLI.exe --help` สำหรับตัวเลือกทั้งหมด MeshMill ปฏิเสธที่จะเขียนทับไฟล์อินพุต

## ตัวอย่างเรขาคณิต

มีตัวอย่างการพัฒนาสองเวอร์ชันให้เลือก ตัวอย่างเป็นตาข่ายคอมโพสิตที่มี
ชั้นตั้งใจของเรขาคณิตซ้ำซ้อนและความหนาแน่นที่แตกต่างกัน มันทำให้คนที่ไม่มีเครื่องสแกนมี
เครื่องมือติดตั้งที่เหมือนจริงสำหรับการเปรียบเทียบอัลกอริธึม การตรวจสอบความหนาแน่น การดำเนินการในระดับภูมิภาค
และพัฒนาคุณลักษณะแผนงาน MeshMill ไม่ต้องการอินพุตที่สแกน

| ไฟล์ | สามเหลี่ยม | ขนาด | จัดส่ง | ดีที่สุดสำหรับ |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 11.9 MiB | Git ปกติ | การประเมินอย่างรวดเร็ว CI และการเรียนรู้การควบคุม |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196.8 MiB | Git LFS | Testing dense source geometry and large-mesh performance |

ตัวอย่างที่มีขนาดเล็กจะถูกดาวน์โหลดพร้อมกับโคลนปกติทุกตัว ต้นฉบับที่ไม่มีใครแตะต้องเป็นทางเลือกและ
จัดการผ่าน Git LFS จึงไม่ทำให้ประวัติพื้นที่เก็บข้อมูลทั่วไปเพิ่มขึ้น เดสก์ท็อป GitHub ประกอบด้วย
Git LFS. ผู้ใช้บรรทัดคำสั่งสามารถติดตั้ง Git LFS และรัน:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

การเผยแพร่ที่ติดแท็กยังเผยแพร่ STL ดั้งเดิมเป็นการดาวน์โหลดโดยตรงสำหรับผู้ที่ไม่ได้ใช้ Git
ดูที่ [`samples/README.md`](../../../samples/README.md) สำหรับแหล่งที่มา ขนาด และผลรวมตรวจสอบ

ผู้ร่วมให้ข้อมูลอัลกอริทึมควรอ่าน
[คู่มือการทดสอบอัลกอริทึม](docs/ALGORITHM_TESTING.md) ก่อนการเปรียบเทียบหรือเปลี่ยนแปลงการลด
พฤติกรรม

## หน่วย STL

STL ไม่ได้เข้ารหัสยูนิต การเปลี่ยนหน่วยแบบจำลองจะเปลี่ยนป้ายกำกับและการวัดโดยไม่ต้องปรับขนาด
พิกัดที่บันทึกไว้ เลือกหน่วยที่อธิบายเรขาคณิตของแหล่งที่มา

## ความเป็นส่วนตัว

MeshMill อ่านและเขียนไฟล์ในเครื่อง ไม่มีบัญชี การวัดและส่งข้อมูลทางไกล การอัปโหลด การโฆษณา หรือ
คุณสมบัติการประมวลผลบนคลาวด์ การใช้งานเมทริก GPU ปัจจุบันใช้ประสิทธิภาพการทำงาน Windows แบบโลคัล
เคาน์เตอร์ ผู้ให้บริการเมทริกดั้งเดิมที่เทียบเท่าได้รับการวางแผนสำหรับ Linux และ macOS

สำหรับการแก้ไขปัญหาการวินิจฉัย นักพัฒนาสามารถเริ่ม GUI ได้
`--diagnostic-log <local-file.jsonl>`. บันทึกจะบันทึกเส้นทางอินพุตและสถานะของกล้องในเครื่องและเป็น
ปิดการใช้งานระหว่างการใช้งานปกติ

## การพัฒนาและการเปิดตัว

ข้อความและเอกสาร UI ที่แปลแล้วนั้นเริ่มแรกด้วยการแปลด้วยเครื่องภายนอก
บริการและตรวจสอบความเสียหายของโครงสร้างโดยอัตโนมัติ เครื่องแปลภาษาก็ยังทำได้
ผิดธรรมชาติหรือไม่ถูกต้อง เจ้าของภาษาได้รับการสนับสนุนให้ตรวจสอบและแก้ไขคำแปลผ่าน
กระบวนการบริจาค

- [มีส่วนร่วม](CONTRIBUTING.md)
- [ขั้นตอนการเผยแพร่](RELEASING.md)
- [โรดแมป](ROADMAP.md)
- [การแก้ไขปัญหา](docs/TROUBLESHOOTING.md)
- [ประกาศของบุคคลที่สาม](THIRD_PARTY_NOTICES.md)

## รองรับ MeshMill

MeshMill ได้รับการพัฒนาและบำรุงรักษาอย่างอิสระ อ่าน
[เหตุใดจึงสนับสนุนงานนี้](SUPPORT.md) หรือสนับสนุนการพัฒนาอย่างต่อเนื่องผ่าน
[ซื้อกาแฟให้ฉัน](https://buymeacoffee.com/tednv)

MeshMill ได้รับอนุญาตภายใต้ GNU General Public License เวอร์ชัน 3 หรือใหม่กว่า ดูสิ
[`LICENSE`](../../../LICENSE)

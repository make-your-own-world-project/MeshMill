# Peta jalan MeshMill

## Dukungan platform

Windows adalah platform paket awal. Arsitektur aplikasi dan format mesh adalah
lintas platform, dan rilis mendatang harus menambahkan paket asli Linux dan macOS. Pekerjaan platform
mencakup pengemasan, integrasi aplikasi, metrik perangkat keras, perilaku sistem file, dan otomatisasi
pengujian rilis sambil mempertahankan proyek yang sama dan alur kerja STL di setiap sistem yang didukung.

- Tambahkan paket Linux x86-64 dan cakupan CI.
- Tambahkan paket silikon Apple macOS dan x86-64, penandatanganan, notaris, dan cakupan CI.
- Tambahkan penyedia metrik CPU, memori, dan GPU asli platform di belakang antarmuka bersama.
- Simpan pengaturan tersimpan, pemetaan keyboard, perilaku baris perintah, dan data proyek tetap portabel.

Peta jalan ini mencatat pekerjaan yang direncanakan. Itu tidak menjelaskan fitur dalam rilis saat ini.

## Ruang lingkup

MeshMill mengelola geometri, kepadatan mesh, kepadatan titik, optimasi, pembersihan, validasi, dan STL
pertukaran sehingga file mesh besar atau berat tetap berguna dalam alur kerja pengeditan hilir.

Pemodelan untuk keperluan umum, pemahatan, lukisan, animasi, rendering, komposisi adegan, material,
kecurangan, dan sistem pembuatan konten lainnya berada di luar peta jalan ini. Sintesis terdistribusi berlaku
ke operasi manajemen mesh MeshMill dan tidak memperluas produk ke editor umum.

## Geometri referensi

Jaring komposit yang dibundel adalah perlengkapan pengembangan umum untuk algoritma dan peta jalan saat ini
bekerja. Lapisannya yang sengaja dibuat berlebihan dan kepadatannya yang tidak merata mendukung perbandingan yang berulang
kualitas pengurangan, analisis kepadatan, penanganan tumpang tindih, operasi regional, pemrosesan di luar inti,
dan sintesis masa depan. Implementasi peta jalan harus melaporkan hasil terhadap pertandingan ini dan skala kecil
jerat regresi yang dibuat khusus, dibandingkan mengoptimalkan perilaku untuk satu model saja.

## Ruang kerja multi-STL dan sintesis statistik

Ruang kerja harus menerima beberapa input STL sebagai objek sumber yang terpisah dan terlihat secara independen.
MeshMill harus menyelaraskan sumber-sumber tersebut, mengukur kesesuaian geometrisnya, dan mensintesis sumber yang dapat digunakan
mesh tanpa mempertahankan duplikat permukaan internal atau geometri tumpang tindih yang berulang.

Perilaku yang direncanakan:

- menambah, menghapus, menyembunyikan, mengisolasi, menyusun ulang, dan memeriksa beberapa sumber STL dalam satu ruang kerja;
- mempertahankan identitas sumber, unit, transformasi, batasan, resolusi, dan riwayat operasi;
- menyediakan registrasi otomatis dengan kontrol penyelarasan manual dan kualitas kesesuaian yang terukur;
- mempartisi sumber ke dalam wilayah spasial sebelum dibandingkan sehingga masukan yang besar tetap dibatasi;
- menganalisis hunian, jarak permukaan terdekat, kesesuaian normal, kepadatan lokal, varians, dan
  jumlah observasi di seluruh wilayah yang tumpang tindih;
- mengklasifikasikan permukaan yang cocok, permukaan yang bertentangan, kebisingan pemindaian, celah, dan geometri unik;
- mengkonsolidasikan permukaan yang disepakati secara statistik menjadi permukaan yang representatif dengan rekaman
  kepercayaan diri alih-alih menumpuk segitiga duplikat;
- menghapus geometri tertutup, bertepatan, dan bersama yang tidak memberikan kontribusi detail bentuk eksterior;
- mempertahankan geometri sumber yang tidak tumpang tindih dan mengekspos wilayah yang ambigu untuk tinjauan visual;
- mengizinkan pembobotan per sumber dan per wilayah ketika satu pemindaian lebih bersih atau lebih detail;
- memvalidasi kedap air, batas, normal, dimensi, dan topologi setelah sintesis;
- mencatat asal sumber dan parameter sintesis sehingga jaring gabungan dapat direproduksi;
- pratinjau jumlah segitiga yang diharapkan, batas, penghapusan tumpang tindih, dan distribusi keyakinan sebelumnya
  melakukan hasil sintesis.

Alur kerja ini harus menggunakan indeks spasial out-of-core dan model unit kerja yang direncanakan untuk skala besar
jerat. Perbandingan statistik dan konsolidasi yang tumpang tindih juga harus dapat didistribusikan ke seluruh daerah
atau node MeshMill jarak jauh.

## Sintesis terdistribusi

Klaster MeshMill harus mengoordinasikan beberapa node yang beroperasi secara paralel di beberapa node
stasiun kerja. Sebuah node dapat memeriksa, memilih, mengurangi, memvalidasi, memperbaiki, atau menggabungkan wilayah yang ditetapkan atau
satuan kerja. Kontribusi tetap dibuat versinya secara independen hingga dikaji dan digabungkan
menjadi versi objek bersama.

Sistem harus mendukung:

- kontribusi bersamaan dari beberapa operator dan node otomatis;
- masukan, parameter, ketergantungan, dan keluaran unit kerja yang deterministik;
- penjadwalan sadar kemampuan berdasarkan CPU, GPU, memori, algoritma, dan beban saat ini;
- partisi jerat, wilayah, tahapan validasi, dan tahapan sintesis yang sadar akan ketergantungan;
- antrian yang tahan lama dengan jeda, melanjutkan, pembatalan, coba lagi, penugasan ulang, dan pemulihan kegagalan;
- artefak yang ditujukan pada konten dan pemeriksaan integritas antar node;
- sintesis yang dapat direproduksi dari serangkaian rekaman versi kontribusi yang diterima;
- stasiun kerja offline atau terhubung sesekali yang dapat disinkronkan nanti;
- operasi lokal-pertama dengan kontrol eksplisit atas node yang berpartisipasi dan data proyek bersama.

## Kolaborasi berversi

Setiap kontribusi harus mencatat versi objek induknya, wilayah atau unit kerja yang dipilih, operasi,
parameter, identitas node, stempel waktu, dependensi, hasil validasi, dan checksum keluaran.

Perilaku kolaborasi yang direncanakan:

- proyek berisi objek, cabang, pos pemeriksaan, kontribusi, dan versi sintesis;
- kontributor dapat bekerja dari versi induk yang sama tanpa saling menimpa;
- kontribusi yang tidak tumpang tindih dapat digabungkan secara otomatis setelah validasi;
- geometri yang tumpang tindih atau ketergantungan yang tidak kompatibel menciptakan konflik yang jelas;
- konflik memberikan perbandingan visual, pilihan tingkat wilayah, rebase, pemutaran ulang, dan penyelesaian manual;
- status peninjauan termasuk tertunda, diterima, ditolak, digantikan, bertentangan, dan digabungkan;
- manifes sintesis akhir mengidentifikasi setiap kontribusi dan ketergantungan yang digabungkan.

## UI Koordinasi

Aplikasi desktop harus mengelola pekerjaan terdistribusi tanpa memerlukan baris perintah terpisah
atau alur kerja administrasi server. Tampilan yang direncanakan meliputi:

- **Proyek:** objek, cabang, versi, kontributor, dan status sintesis.
- **Cluster:** workstation dan node yang terhubung, kemampuan, kesehatan, beban, dan tugas saat ini.
- **Antrian:** unit kerja yang tertunda, aktif, dijeda, diblokir, gagal, dan diselesaikan.
- **Kontribusi:** penulis, node, versi induk, wilayah yang terpengaruh, parameter, pemeriksaan, dan status peninjauan.
- **Bandingkan:** tampilan 3D yang disinkronkan, perbedaan geometri, metrik, dan pemeriksaan batas.
- **Konflik:** wilayah yang tumpang tindih, konflik ketergantungan, pilihan resolusi, dan hasil validasi.
- **Sintesis:** grafik ketergantungan, kemajuan agregat, versi kontribusi yang dipilih, dan hasil akhir.
- **Histori:** grafik cabang, pos pemeriksaan, penggabungan, versi sintesis, dan manifes reproduktifitas.

Area pandang harus menunjukkan kepemilikan, wilayah yang ditetapkan, pekerjaan yang telah selesai, perubahan yang tertunda, konflik,
dan perbedaan versi tanpa mengubah mesh yang mendasarinya.

## Koordinasi dan transportasi

Fase desain pertama harus menentukan batasan protokol sebelum memilih transport. Protokol
harus memisahkan metadata koordinasi dari artefak mesh besar, mendukung transfer yang dapat dilanjutkan, dan
tetap dapat digunakan di jaringan lokal tanpa akun eksternal atau layanan yang dihosting.

Konsep koordinasi yang diperlukan:

- pemilihan koordinator atau koordinator yang dipilih secara eksplisit;
- penemuan simpul dan pendaftaran simpul manual;
- sesi yang diautentikasi dan otorisasi cakupan proyek;
- sewa dan detak jantung untuk kepemilikan pekerjaan;
- penyerahan karya idempoten dan penerimaan hasilnya;
- negosiasi versi antara rilis MeshMill yang berbeda;
- peristiwa terstruktur untuk kemajuan, log, validasi, kegagalan, dan percobaan ulang;
- pemulihan setelah gangguan koordinator, workstation, jaringan, atau node.

## Fase pengiriman

### Fase 0: pemrosesan mesh besar di luar inti

Indeks, streaming, cache, unit kerja, dan kontrak keselamatan didokumentasikan dalam
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Perkirakan jumlah segitiga dan memori kerja sebelum mengalokasikan mesh lengkap.
- Buka file biner STL yang berukuran besar sebagai ikhtisar navigasi berbatas dan sampelnya merata.
- Partisi geometri resolusi penuh menjadi kubus spasial dengan batas tumpang tindih deterministik.
- Membaca, menganalisis, dan mengoptimalkan kubus independen secara bersamaan dalam CPU dan batas memori.
- Streaming tingkat area pandang kasar hingga halus alih-alih memerlukan mesh lengkap di memori.
- Gambarkan status kubus langsung di area pandang: antri, membaca, memproses, selesai, dan gagal.
- Tampilkan kemajuan per kubus dengan mengisi setiap kubus dan pertahankan tampilan seluruh objek tingkat tinggi.
- Kumpulkan kubus yang diproses dengan validasi batas, penghapusan duplikat, dan pengaturan yang dapat direproduksi.
- Perluas penjadwal kubus lokal ke unit kerja sintesis terdistribusi di fase selanjutnya.

### Tahap 1: landasan lokal berversi

- Tentukan format objek, operasi, kontribusi, cabang, dan manifes.
- Tambahkan ruang kerja multi-STL dengan visibilitas, transformasi, metadata, dan asal per sumber.
- Tambahkan metrik kualitas pendaftaran dan klasifikasi tumpang tindih spasial.
- Sintesis permukaan yang selaras secara statistik sambil menghapus geometri duplikat dan tertutup.
- Tambahkan tinjauan visual untuk konflik, kesenjangan, keyakinan, dan geometri unik pada satu sumber.
- Pertahankan riwayat lokal di seluruh sesi aplikasi.
- Tambahkan mesh visual dan perbandingan wilayah.
- Jadikan operasi bersifat deterministik dan dapat direproduksi secara independen.

### Fase 2: node lokal yang terkoordinasi

- Jalankan node pekerja di satu stasiun kerja.
- Tambahkan antrian, pelaporan kemampuan, penugasan kerja, dan pembatalan.
- Tampilkan node dan status unit kerja di UI MeshMill.
- Validasi partisi dan perakitan hasil secara lokal.

### Fase 3: sintesis multi-workstation

- Tambahkan penemuan dan pendaftaran LAN yang diautentikasi.
- Transfer masukan dan hasil pekerjaan yang ditujukan pada konten dengan dukungan resume.
- Koordinasikan pekerjaan bersamaan di beberapa stasiun kerja.
- Pulihkan tugas setelah kegagalan node atau jaringan.

### Fase 4: pembuatan versi kolaboratif

- Tambahkan kontributor, cabang, status ulasan, dan izin.
- Gabungkan kontribusi yang tidak tumpang tindih.
- Mendeteksi dan menyelesaikan konflik yang tumpang tindih atau ketergantungan.
- Sintesiskan kontribusi yang dipilih ke dalam versi objek yang dapat direproduksi.

### Fase 5: pengerasan produksi

- Tambahkan tes kompatibilitas protokol dan penanganan versi campuran.
- Tambahkan pengujian audit, integritas, korupsi, interupsi, dan pemulihan.
- Penjadwalan benchmark, partisi, transfer, penggabungan, dan kinerja sintesis.
- Penyebaran dokumen, pencadangan, migrasi, dan pemulihan insiden.

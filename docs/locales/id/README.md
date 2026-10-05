<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

MeshMill adalah aplikasi desktop khusus untuk mengolah geometri mesh yang berukuran sangat besar, padat, atau rumit
agar lebih mudah dikelola. Aplikasi ini menyediakan fitur inspeksi cepat, analisis kepadatan, pemilihan area, pemotongan, penghapusan,
serta pengurangan mesh secara terkontrol tanpa perlu membuat akun atau mengunggah geometri.

Render OpenGL yang dipercepat GPU menjaga navigasi area pandang, pemilihan perangkat keras, visualisasi kepadatan,
dan inspeksi interaktif responsif. Pengurangan mesh saat ini berjalan di pekerja CPU asli yang terpisah,
menjauhkan perhitungan geometri panjang dari antarmuka.

MeshMill dapat memproses mesh dari pemindai 3D, hasil ekspor CAD dan pemodelan, alur kerja rekonstruksi,
geometri yang dihasilkan secara prosedural, dan sumber STL lainnya. Aplikasi ini menyiapkan geometri untuk editor tahap selanjutnya,
perangkat manufaktur, dan alur kerja mesh lainnya. Pemodelan umum, pemahatan (sculpting), animasi,
pengaturan material, dan pembuatan adegan berada di luar cakupan aplikasi ini.

## Unduh

Pilih sistem operasi Anda. Setiap paket mandiri. Python, Node.js, dan lainnya
ketergantungan pengembangan tidak diperlukan.

| Sistem | Unduhan yang disarankan | Status |
| --- | --- | --- |
| **Windows x64** | **[Unduh penginstal Windows][windows-installer]** | Rilis yang didukung |
| Windows x64, tanpa instalasi | [Unduh ZIP portabel][windows-portable] | Rilis yang didukung |
| Linux x86-64 | [Unduh pratinjau Linux][linux-preview] | Pratinjau pengujian awal |
| macOS Apple silikon | [Unduh pratinjau silikon Apple][mac-arm-preview] | Pratinjau pengujian awal |
| macOS Intel | [Unduh pratinjau Intel Mac][mac-intel-preview] | Pratinjau pengujian awal |

**Sebagian besar pengguna Windows sebaiknya memilih penginstal Windows.** Gunakan ZIP portabel hanya jika Anda memilihnya
tidak ingin MeshMill diinstal atau tidak memiliki izin untuk menginstal aplikasi.

Paket Linux dan macOS adalah pratinjau awal yang tidak ditandatangani. Mereka melewati build asli otomatis dan
pengujian asap yang dikemas, namun masih memerlukan pengujian perangkat keras yang sebenarnya. Baca
[Catatan pratinjau Linux dan macOS](../../PLATFORM_TESTING.md) sebelum menginstalnya.

Windows SmartScreen atau macOS Gatekeeper mungkin memperingatkan tentang paket yang tidak ditandatangani. Checksum dan
optional [sample mesh][sample-mesh] are available with the releases. [Browse all releases and
checksums][all-releases] only if you need an older version or want to verify a download.

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## Panduan cepat

1. Buka STL.
2. Periksa dalam mode tampilan Shaded, Density, Wireframe, atau Vertices.
3. Pilih tingkat kualitas, algoritma, dan target jumlah segitiga.
4. Pilih **Optimize** untuk menghitung hasilnya.
5. Bandingkan mesh asli dan yang telah dioptimalkan, lalu pilih **Apply** untuk menerapkan proses tersebut.
6. Pilih **Save current state** atau tekan `Ctrl+S`.

MeshMill tidak akan memulai optimisasi hanya karena adanya perubahan pada file atau pengaturan.

## Kemampuan

- Input STL biner dan ASCII, output STL biner
- Reduksi Fast QEM yang menjaga keseimbangan kepadatan, bentuk, dan topologi
- Area pandang OpenGL yang dipercepat GPU, pemilihan perangkat keras, dan visualisasi kepadatan
- Pekerja geometri latar belakang asli untuk pengurangan mesh
- Mode tampilan *shaded* (berbayang), kepadatan, *wireframe*, dan verteks
- Target otomatis yang diturunkan dari geometri, bukan batas jumlah segitiga yang tetap
- Seleksi poligon dengan fitur pemilihan multi-wilayah secara aditif
- Memotong (*crop*), menghapus, atau mengoptimalkan hanya wilayah yang dipilih
- Perbandingan *mesh* asli, sebelumnya, dan saat ini yang disimpan dalam *cache*
- Fitur *undo* dan *redo* untuk perubahan geometri yang telah diterapkan
- Pergeseran dimensi, persentase reduksi, dan estimasi ukuran output
- Satuan tampilan milimeter, sentimeter, meter, inci, dan kaki
- Metrik CPU, memori, GPU, dan aktivitas geometri
- Pemuatan tampilan ringkasan terbatas saat STL biner melebihi batas alokasi memori yang dikonfigurasi
- Aplikasi berbasis GUI dan baris perintah (*command-line*)
- Pemrosesan lokal tanpa ketergantungan pada akun, telemetri, unggahan, atau *cloud*

## Periksa geometri sebelum menguranginya

Layar Berbayang memberikan tampilan permukaan dan siluet yang bersih. Hal ini berguna untuk membandingkan
pelestarian bentuk sebelum menerapkan izin pengoptimalan.

![Area pandang berbayang MeshMill yang menampilkan mesh sampel yang dibundel](../../images/meshmill-shaded.png)

Tampilan Vertices memperlihatkan distribusi titik sebenarnya. Daerah pemindaian padat, daerah jarang, dan
perubahan mendadak dalam pengambilan sampel terlihat tanpa mengubah geometri. Panel metrik diperluas
melacak aktivitas CPU, memori, GPU, dan pemrosesan geometri saat bekerja dengan mesh.

![Tampilan Vertices MeshMill dengan metrik kinerja yang diperluas](../../images/meshmill-vertices.png)

Tampilan Wireframe menunjukkan struktur segitiga secara langsung. Ini membantu mengidentifikasi kepadatan yang tidak perlu,
triangulasi tidak teratur, dan wilayah di mana penyederhanaan dapat menghilangkan geometri substansial.

![Tampilan Wireframe MeshMill menunjukkan variasi kepadatan segitiga](../../images/meshmill-wireframe.png)

## Analisis kepadatan mesh

Tampilan Kepadatan memetakan kepadatan lokal relatif di seluruh model. Daerah yang jarang tetap sejuk
wilayah yang semakin padat bergerak melalui warna-warna yang lebih cerah, membuat pengambilan sampel yang tidak merata terlihat secara sekilas.

![Tampilan kepadatan MeshMill menunjukkan kepadatan mesh relatif](../../images/meshmill-density.png)

Kepadatan tetap tersedia saat mengevaluasi pengoptimalan sementara. Kotak alat melaporkan
algoritma, target, jumlah segitiga dan titik sudut yang dihasilkan, persentase pengurangan, dimensi, dan
perkiraan ukuran keluaran sebelum izin diterapkan.

![Tampilan Kepadatan MeshMill menunjukkan pengoptimalan sementara](../../images/meshmill-density-overview.png)

Tahan tombol kanan mouse untuk memeriksa suatu wilayah melalui kaca pembesar melingkar. Tampilan yang diperbesar
tetap terpusat pada penunjuk dan menampilkan kepadatan lokal tanpa mengubah posisi kamera utama.

![Tampilan Kepadatan MeshMill dengan kaca pembesar area pandang](../../images/meshmill-density-zoom.png)

## Kontrol tampilan

| Input | Tindakan |
| --- | --- |
| Seret dengan tombol tengah mouse | Orbit |
| Shift + seret dengan tombol tengah mouse | Geser (Pan) |
| Roda mouse | Zoom ke arah penunjuk |
| Ctrl + roda mouse | Putar searah atau berlawanan arah jarum jam |
| Tombol panah | Orbit mengelilingi pusat tampilan |
| Ctrl + tombol panah | Geser (Pan) |
| Ctrl + Shift + Atas/Bawah | Zoom |
| Ctrl + Shift + Kiri/Kanan | Gulung |
| `F1` / `F2` / `F3` / `F4` | Berbayang / Kepadatan / Wireframe / Simpul |
| Tahan mouse kanan | Kaca Pembesar |
| Shift + klik kiri | Menambah atau menghapus titik penggaris |
| Ctrl + seret ke kiri | Gambarlah poligon pilihan |
| `Ctrl+C` | Tambahkan poligon ke pilihan yang disimpan |
| `Ctrl+X` | Pangkas ke pilihan |
| `Ctrl+Space` | Optimalkan pilihan |
| `Delete` | Hapus pilihan |
| `Escape` | Hapus pilihan aktif atau penggaris |
| `Ctrl+Z` / `Ctrl+Y` | Batalkan / ulangi |
| `Ctrl+S` | Simpan status mesh saat ini |

Tombol tampilan standar mengikuti blok navigasi enam tombol:

| Kunci | Lihat | Ctrl + tombol |
| --- | --- | --- |
| `Insert` | Kiri | Tetapkan orientasi saat ini sebagai Kiri |
| `Home` | Depan | Tetapkan orientasi saat ini sebagai Depan |
| `Page Up` | Benar | Tetapkan orientasi saat ini sebagai Kanan |
| `Delete` | Teratas bila tidak ada pilihan | Tetapkan orientasi saat ini sebagai Atas |
| `End` | Kembali | Tetapkan orientasi saat ini sebagai Kembali |
| `Page Down` | Bawah | Tetapkan orientasi saat ini sebagai Bawah |

Menyimpan tampilan juga memperbarui tampilan sebaliknya. Kiri dan Kanan, Depan dan Belakang, serta Atas dan Bawah
tetap berpasangan. Dalam dialog konfirmasi, **Simpan** adalah tindakan default, jadi Enter akan menyimpan
orientasi. Depan muncul di bagian atas tampilan Atas dan Bawah.

Pintasan dapat diubah atau diatur ulang di Pengaturan.

## Alur kerja seleksi

Tahan Ctrl dan seret ke kiri untuk menggambar poligon. Seret sudut untuk membentuknya kembali, klik kiri salah satu tepinya untuk menambahkan a
titik, atau klik kanan tepi untuk menghapusnya. Tambahkan lebih banyak wilayah dengan `Ctrl+C`. Memindahkan kamera menyembunyikan
poligon ruang layar sambil mempertahankan geometri yang dipilih.

Optimasi dengan pilihan aktif hanya mempengaruhi pilihan tersebut. Hasilnya masih bersifat sementara
hingga **Terapkan** dipilih. **Batal** membuang hasil sementara dan mempertahankan pilihan tersebut
konfigurasi lain dapat dicoba. Operasi potong dan hapus menjadi pengeditan mesh normal yang tidak dapat dilakukan.

Panel seleksi melaporkan simpul, segitiga, bagian mesh yang dipilih secara kumulatif, perkiraan
ukuran, dan dimensi. Tindakannya memotong, menambah, mengoptimalkan, menghapus, mundur, atau menghapus yang disimpan
seleksi tanpa menyembunyikan geometri di sekitarnya.

![MeshMill menampilkan seleksi regional yang dipertahankan dan statistik geometrinya](../../images/meshmill-crop-selection.png)

## Jerat besar

Sebelum mengalokasikan biner STL, MeshMill membandingkan perkiraan memori kerja dengan yang dikonfigurasi
anggaran memori. File yang melebihi anggaran akan terbuka sebagai ikhtisar terbatas dan hanya dapat dibaca. Laporan ikhtisar
jumlah segitiga sumber lengkap tetapi menonaktifkan pengeditan dan ekspor karena ini adalah sampel, bukan keseluruhan
objek. Pemrosesan out-of-core yang terindeks dan bergantung pada zoom direncanakan
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Baris perintah

`MeshMillCLI.exe` disertakan dalam kedua paket rilis:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Jalankan `.\MeshMillCLI.exe --help` untuk semua opsi. MeshMill menolak untuk menimpa file masukannya.

## Contoh geometri

Tersedia dua versi sampel pengembangan. Sampelnya adalah mesh komposit dengan
lapisan geometri redundan yang disengaja dan kepadatan bervariasi. Ini memberi orang tanpa pemindai a
perlengkapan realistis untuk membandingkan algoritme, memeriksa kepadatan, menjalankan operasi regional,
dan mengembangkan fitur peta jalan. MeshMill tidak memerlukan input yang dipindai.

| Berkas | Segitiga | Ukuran | Pengiriman | Terbaik untuk |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Git Biasa | Evaluasi cepat, CI, dan mempelajari kontrol |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MiB | Git LFS | Menguji geometri sumber padat dan kinerja mesh besar |

Sampel yang lebih kecil diunduh dengan setiap klon normal. Dokumen asli yang belum tersentuh adalah opsional dan
dikelola melalui Git LFS sehingga tidak menambah riwayat repositori biasa. GitHub Desktop termasuk
Git LFS. Pengguna baris perintah dapat menginstal Git LFS dan menjalankan:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Rilis yang diberi tag juga menerbitkan STL asli sebagai unduhan langsung untuk orang yang tidak menggunakan Git.
Lihat [`samples/README.md`](../../../samples/README.md) untuk asal, dimensi, dan checksum.

Kontributor algoritma juga harus membaca
[panduan pengujian algoritma](docs/ALGORITHM_TESTING.md) sebelum membandingkan atau mengubah pengurangan
perilaku.

## Unit STL

STL tidak mengkodekan unit. Mengubah unit Model mengubah label dan pengukuran tanpa penskalaan
koordinat yang disimpan. Pilih unit yang menggambarkan geometri sumber.

## Privasi

MeshMill membaca dan menulis file lokal. Tidak berisi akun, telemetri, unggahan, iklan, atau
fitur pemrosesan cloud. Implementasi metrik GPU saat ini menggunakan performa Windows lokal
penghitung. Penyedia metrik asli yang setara direncanakan untuk Linux dan macOS.

Untuk pemecahan masalah diagnostik, pengembang dapat memulai GUI dengan
`--diagnostic-log <local-file.jsonl>`. Log mencatat perutean input dan status kamera secara lokal dan terkini
dinonaktifkan selama penggunaan normal.

## Pengembangan dan rilis

Teks dan dokumentasi UI yang dilokalkan pada awalnya diproduksi dengan terjemahan mesin eksternal
layanan dan diperiksa secara otomatis untuk kerusakan struktural. Terjemahan mesin masih bisa
tidak wajar atau tidak benar. Penutur asli didorong untuk meninjau dan mengoreksi terjemahannya
proses kontribusi.

- [Berkontribusi](CONTRIBUTING.md)
- [Proses rilis](RELEASING.md)
- [Peta Jalan](ROADMAP.md)
- [Pemecahan Masalah](docs/TROUBLESHOOTING.md)
- [Pemberitahuan pihak ketiga](THIRD_PARTY_NOTICES.md)

## Mendukung MeshMill

MeshMill dikembangkan dan dipelihara secara independen. Baca
[mengapa mendukung pekerjaan ini penting](SUPPORT.md), atau mendukung pengembangan berkelanjutan
[Belikan Saya Kopi](https://buymeacoffee.com/tednv).

MeshMill dilisensikan di bawah Lisensi Publik Umum GNU, versi 3 atau lebih baru. Lihat
[`LICENSE`](../../../LICENSE).

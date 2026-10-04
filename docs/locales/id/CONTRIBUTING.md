# Berkontribusi

Kontribusi diterima melalui penerbitan dan permintaan penarikan.

## Ruang lingkup proyek

MeshMill membuat file mesh berukuran besar, padat, atau sulit dikelola untuk pengeditan hilir dan
alur kerja produksi. Kontribusi harus meningkatkan pemeriksaan geometri, mesh dan kepadatan titik
manajemen, pengoptimalan, seleksi, pemotongan, pembersihan, validasi, pertukaran STL, kinerja,
atau koordinasi operasi tersebut.

Proyek ini tidak mencakup pemodelan, pemahatan, lukisan, animasi, rendering,
komposisi adegan, material, tali-temali, atau sistem pembuatan konten lainnya. Proposal yang memperkenalkan
fitur-fitur tersebut berada di luar cakupan proyek.

Fitur-fitur baru harus menjaga aplikasi tetap fokus, mempertahankan alur kerja langsung yang mengubah sumber
geometri menjadi jerat yang dapat dikelola, dan hindari mengubah kontrol pendukung menjadi pengeditan umum
lingkungan.

## Lokalisasi

Teks sumber UI bahasa Inggris disimpan di `locales/en-US.json`. Metadata lokal disimpan di
`locales/manifest.json`. Katalog UI yang diterjemahkan menggunakan kunci stabil dan nama file yang sama
`<locale>.json`. Dokumentasi yang diterjemahkan menggunakan nama file root yang cocok di bawah
`docs/locales/<locale>/`.

Setelah mengubah label, keterangan alat, dialog, atau teks lain yang terlihat oleh pengguna, jalankan:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Tinjau perubahan sumber dan kunci yang dibuat ulang secara bersamaan.

## Perubahan geometri dan algoritma

Gunakan geometri sampel yang dibundel saat mengubah pengoptimalan, analisis kepadatan, pemilihan, pemotongan,
penanganan file besar, atau perilaku perbandingan area pandang. Ini sengaja berisi lapisan yang berlebihan
dan kepadatan yang tidak merata, sehingga hasil yang bermanfaat akan meningkatkan pengelolaan tanpa menyembunyikan distorsi,
membuang batas-batas yang bermakna, atau secara diam-diam menghapus geometri yang dipertahankan oleh algoritma lain.

Catat input, algoritme, pengaturan, jumlah segitiga, dimensi, penyimpangan dimensi, waktu yang berlalu,
dan tangkapan layar yang relevan untuk perbandingan. Uji perlengkapan Git normal yang lebih kecil dan, ketika
perubahan menyangkut geometri besar atau berlapis, perlengkapan Git LFS asli. Jangan menyetel algoritma
untuk perlengkapan ini saja. Tambahkan kasus sintetik kecil untuk makhluk invarian atau regresi tertentu
diuji.

Lihat [Pengujian dan kontribusi algoritma](docs/ALGORITHM_TESTING.md) untuk daftar periksa perbandingan.

## Pengaturan pengembangan

1. Instal Python 3.12 64-bit di Windows.
2. Membuat dan mengaktifkan lingkungan virtual.
3. Instal `requirements-dev.txt`.
4. Jalankan `python meshmill.py` untuk GUI atau `python meshmill.py --help` untuk penggunaan CLI.
5. Jalankan `python -m py_compile meshmill.py` sebelum mengirimkan perubahan.

Simpan mesh pribadi, file executable yang dihasilkan, tangkapan layar yang berisi informasi pribadi, dan lokal
membangun direktori dari komitmen. Geometri uji yang dapat didistribusikan ulang termasuk dalam `samples/` dengan miliknya
sumber, lisensi, dimensi, dan metode pembuatan didokumentasikan. File sumber baru harus menggunakan
Pengidentifikasi SPDX `GPL-3.0-or-later`.

Pangkas setiap tangkapan layar dokumentasi ke konten aplikasi MeshMill. Jangan sertakan
bilah tugas, jendela chrome yang tidak terkait, notifikasi, detail akun, jalur pribadi, atau latar belakang
konten desktop.

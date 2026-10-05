# Melepaskan MeshMill

Alur rilis stabil membangun artefak Windows pada runner Windows yang dihosting GitHub. Terpisah
alur kerja manual membuat pratinjau silikon Linux x86-64 dan macOS Intel/Apple yang tidak ditandatangani pada versi asli
Pelari yang dihosting GitHub. Pengguna akhir tidak menginstal Python, Node.js, atau dependensi.

Sebelum membuat, segarkan dan validasi katalog sumber pelokalan:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Sebelum rilis publik pertama

1. Selesaikan dan validasi terjemahan aplikasi dan dokumentasi yang direncanakan.
2. Tinjau pemberitahuan GPL dan pihak ketiga.
3. Uji instalasi, peluncuran, pemuatan STL, pengoptimalan, ekspor, dan penghapusan instalasi secara bersih
   Akun Windows atau mesin virtual.
4. Jalankan CI terhadap `samples/sample-scan.stl`. Periksa setiap tangkapan layar dokumentasi dan potong
   bilah tugas, jendela chrome yang bukan bagian dari MeshMill, notifikasi, jalur pribadi, akun
   detail, dan konten desktop yang tidak terkait sebelum dipublikasikan.
5. Konfigurasikan pembuat Git lokal repositori dengan alamat tanpa balasan GitHub akun sebelum
   komitmen pertama. Konfirmasikan dengan `git config --local --get user.email`.
6. Konfigurasikan rahasia penandatanganan Authenticode opsional:
   - `WINDOWS_CERTIFICATE_BASE64`: Sertifikat PFX berkode Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: kata sandi PFX.

Tanpa sertifikat penandatanganan, file yang dihasilkan masih berfungsi, namun Windows SmartScreen mungkin ditampilkan
peringatan penerbit tidak dikenal. Jangan mendeskripsikan bangunan yang tidak ditandatangani sebagai bangunan yang ditandatangani atau dipercaya.

## Pemindaian asli dan Git LFS

`samples/original-scan.stl` dilacak melalui Git LFS karena melebihi 100 MiB normal GitHub
batas berkas. Sebelum penerapan pertama, verifikasi:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Filter harus `lfs`, dan ID objek penunjuk harus cocok dengan `samples/SHA256SUMS.txt`. Rilis
alur kerja memeriksa konten LFS dan menerbitkan STL asli sebagai aset rilis terpisah. penggunaan CI
sampel Git normal yang lebih kecil dan tidak mengunduh objek LFS.

## Uji versi rilis tanpa penerbitan

Buka **Tindakan**, pilih **Lepaskan**, pilih **Jalankan alur kerja**, dan masukkan versi numerik seperti
`0.1.0`. Proses manual mengunggah artefak alur kerja untuk pengujian tetapi tidak membuat GitHub publik
Lepaskan.

## Publikasikan rilis

Dari cabang `main` yang bersih dan ditinjau:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Tag memulai alur kerja rilis. Itu:

1. menginstal dependensi build yang disematkan;
2. menghasilkan metadata versi Windows yang cocok;
3. membangun executable GUI dan CLI mandiri;
4. menandatangani executable ketika rahasia penandatanganan dikonfigurasi;
5. membuat penginstal Inno Setup per pengguna;
6. menandatangani penginstal saat dikonfigurasi;
7. membuat file checksum ZIP dan SHA-256 portabel;
8. mengunggah artefak alur kerja;
9. membuat Rilis GitHub untuk tag yang didorong.

Verifikasi penginstal dan arsip portabel pada sistem Windows yang bersih sebelum mengumumkan rilisnya.
Pertahankan sumber yang sesuai dengan setiap biner terdistribusi yang tersedia di bawah tag rilis yang sama.
Konfirmasikan bahwa tombol GitHub mengarah ke URL repositori publik final sebelum memberi tag pada yang pertama
rilis.

## Bangun pratinjau Linux dan macOS

Buka **Tindakan**, pilih **Pembuatan pratinjau platform**, dan pilih **Jalankan alur kerja**. Masukkan pratinjau
versi seperti `0.2.0-preview.1`.

Biarkan **Publikasikan prarilis GitHub publik** untuk dijalankan pertama kali. Alur kerja dibuat dan diuji:

- Linux x86-64 di Ubuntu 22.04;
- macOS x86-64 pada pelari Intel;
- macOS arm64 pada pelari silikon Apple.

Unduh artefak alur kerja dan periksa checksum dan lognya. Jalankan kembali alur kerja dengan
penerbitan diaktifkan hanya setelah setiap pekerjaan build berhasil. Pratinjau macOS yang diterbitkan ditandatangani secara ad-hoc,
tidak diaktakan oleh Apple. Jelaskan mereka sebagai versi pratinjau dan tautkan penguji ke dalamnya
`docs/PLATFORM_TESTING.md` dan formulir masalah **Tes pratinjau platform**.

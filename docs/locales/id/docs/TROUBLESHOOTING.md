# Pemecahan masalah

## Windows memblokir unduhan

Pembangunan komunitas yang tidak ditandatangani dapat memicu Microsoft Defender SmartScreen. Bandingkan yang diunduh
hash SHA-256 file dengan `SHA256SUMS.txt` dari Rilis GitHub yang sama. Rilis yang ditandatangani mengidentifikasi
penerbitnya di properti file Windows.

## Pembuatan portabel tidak dimulai

Ekstrak ZIP lengkap sebelum menjalankan `MeshMill.exe`. Direktori `_internal` harus tetap berada di sebelahnya
untuk kedua executable. Jangan jalankan file yang dapat dieksekusi dari dalam penampil ZIP.

## STL besar terbuka sebagai ikhtisar

Perkiraan set kerja melebihi anggaran memori di Pengaturan. Mode ikhtisar sengaja
hanya baca. Tingkatkan anggaran hanya bila mesin memiliki cukup memori yang tersedia, atau kurangi
mesh sebelum membukanya untuk diedit.

## Tampilan standar tidak disimpan

Tekan pintasan tampilan yang dimodifikasi Ctrl, lalu pilih **Simpan** atau tekan Enter di konfirmasi
dialog. Menyimpan satu tampilan juga memperbarui tampilan sebaliknya. Baris status melaporkan tampilan yang disimpan.

## Pintasan navigasi tidak merespons

Tutup dialog modal apa pun terlebih dahulu. Tinjau atau setel ulang pintasan di Pengaturan jika sudah disesuaikan. Itu
pintasan tampilan default menggunakan Sisipkan, Beranda, Halaman Atas, Hapus, Akhiri, dan Halaman Bawah.

## Buat log diagnostik orientasi lokal

Pencatatan log diagnostik dinonaktifkan secara default. Untuk merekam perutean keyboard dan status kamera secara lokal:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Log mungkin berisi jalur file yang dibuka. Tinjau dan edit sebelum dibagikan. Geometri mesh tidak
ditulis ke log.

## Laporkan masalah

Sertakan versi MeshMill, versi Windows, model GPU, jumlah segitiga mesh, tindakan tepat
urutannya, dan apakah paket penginstal atau portabel digunakan. Gunakan sampel yang dapat didistribusikan ulang
jaring jika memungkinkan. Jangan lampirkan pindaian pribadi atau log diagnostik tanpa meninjaunya terlebih dahulu.

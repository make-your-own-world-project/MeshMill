# Pengujian dan kontribusi algoritma

Algoritme MeshMill harus membuat geometri yang sulit dapat dikelola sekaligus menjaga efeknya tetap terlihat,
terukur, dan dapat dibalik sebelum suatu hasil diterapkan.

## Perlengkapan referensi

Gunakan kedua versi gabungan geometri sampel komposit:

- `samples/sample-scan.stl` adalah perlengkapan Git normal yang lebih kecil untuk pengembangan rutin, otomatis
  pemeriksaan, dan mempelajari kontrolnya.
- `samples/original-scan.stl` adalah perlengkapan Git LFS lengkap untuk perilaku file besar, lapisan berlebihan,
  kepadatan yang tidak merata, tumpang tindih, dan kinerja kerja.

Daerah yang berlebihan dan padat merupakan karakteristik pengujian yang disengaja. Sebuah tes mungkin menargetkan mereka, tapi
tidak boleh berasumsi bahwa setiap permukaan yang tumpang tindih dapat dibuang. Tambahkan jaring sintetis padat bila a
perubahan memerlukan batas, kelengkungan, topologi, kepadatan, atau invarian tumpang tindih yang diketahui.

## Daftar periksa perbandingan

Untuk perubahan algoritma atau parameter, catat:

- Versi MeshMill atau komit;
- perlengkapan input dan checksum;
- algoritma, preset kualitas, target, dan pengaturan lanjutan;
- jumlah segitiga dan titik sudut asli dan hasil;
- persentase reduksi, dimensi, dan penyimpangan dimensi;
- waktu yang berlalu dan memori puncak ketika kinerja relevan;
- tangkapan layar dari tampilan tersimpan dan mode tampilan yang sama;
- batas yang terlihat, lubang, perpotongan diri, tumpang tindih, atau perubahan distorsi;
- apakah hasilnya berasal dari operasi keseluruhan atau hanya seleksi.

Bandingkan dengan perilaku saat ini pada target yang sama, tidak hanya dengan preset lain dengan a
jumlah keluaran yang berbeda. Periksa tampilan bayangan, kepadatan, gambar rangka, dan simpul jika memungkinkan.

## Panduan penerimaan

Perubahan pengoptimalan harus menghindari perubahan dimensi yang tidak terduga, inversi permukaan yang nyata,
keretakan antar wilayah yang diproses, hilangnya batas-batas yang berarti, dan regresi kualitas yang besar di a
jumlah keluaran serupa. Perubahan yang berorientasi pada kepadatan harus menunjukkan bahwa konsentrasi yang dihilangkan memang demikian
tidak membawa kelengkungan atau topologi yang berguna.

Hasil kinerja harus mengidentifikasi prosesor, kapasitas memori, perangkat keras grafis, pengoperasian
sistem, ukuran input, dan apakah data sudah di-cache. Validasi struktural dan tangkapan layar
mendukung peninjauan tetapi tidak menggantikan pemeriksaan oleh kontributor yang memahami geometri sumber.

## Tes regresi

Lebih menyukai pengujian deterministik dengan toleransi eksplisit. Jaga agar perlengkapan baru cukup kecil untuk Git normal,
mendokumentasikan asal dan lisensinya, dan menggunakan geometri sintetis ketika data sumber sebenarnya tidak diperlukan.
Pengujian harus mencakup pembatalan dan pemulihan status ketika suatu operasi dapat mengubah geometri.

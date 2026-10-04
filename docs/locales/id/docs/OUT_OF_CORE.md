# Arsitektur mesh out-of-core

Perlindungan file besar MeshMill saat ini memperkirakan memori kerja sebelum mengalokasikan memori yang lengkap
jala. File yang melebihi anggaran yang dikonfigurasi dapat dibuka sebagai ikhtisar navigasi terbatas. Sebuah
ikhtisar adalah sampel geometri, terlihat teridentifikasi, dan tidak dapat diedit atau diekspor sebagai
padahal itu sumber lengkapnya.

Detail yang benar-benar bergantung pada zoom memerlukan indeks spasial yang persisten. Desain di bawah mendefinisikan hal itu
tahap implementasi selanjutnya.

## Format indeks

Setiap mesh sumber menerima direktori `.meshmill-index` berversi yang berisi:

- `manifest.json`, dengan ukuran sumber, waktu modifikasi, hash konten sampel, batasan,
  jumlah segitiga, versi indeks, presisi koordinat, dan deskripsi level;
- ubin spasial ditangani oleh tingkat oktree dan kode Morton;
- jaring tampilan kasar untuk setiap ubin induk yang ditempati;
- catatan segitiga resolusi penuh di ubin daun; Dan
- kepemilikan batas dan metadata yang tumpang tindih yang digunakan selama operasi dan perakitan regional.

Pembuatan indeks membaca sumber secara berurutan dalam blok yang dibatasi. Ia menulis ubin berjalan sementara dan
menerbitkan manifes secara atom setelah setiap file yang diperlukan lolos validasi. Terganggu atau
indeks basi terdeteksi dari manifesnya dan dapat dilanjutkan atau dibangun kembali tanpa membuka secara penuh
jala dalam memori.

## Streaming area pandang

Area pandang memilih ubin menggunakan frustum kamera dan kesalahan ruang layar. Ubin induk yang kasar adalah
ditampilkan terlebih dahulu. Ubin anak yang terlihat menggantikannya saat kamera bergerak mendekat, saat berada di luar layar dan
ubin berdampak rendah tetap kasar. RAM dan VRAM memiliki anggaran independen dan paling jarang digunakan
cache. Melepaskan detail tidak pernah melepaskan representasi keseluruhan objek yang kasar.

Penjadwal mencatat status ubin berikut: antri, membaca, memproses, mengunggah, menetap, gagal,
dan dibatalkan. Area pandang dapat mewarnai kubus berdasarkan status dan mengisi setiap kubus sesuai proporsinya
kemajuan. Pembatalan akan menghapus sebagian hasil dan membiarkan representasi lengkap terakhir tetap aktif.

## Pemrosesan dan kapasitas

Unit kerja lokal adalah ubin ditambah tumpang tindih deterministik yang diperlukan oleh pengoperasiannya. Konkurensi
dibatasi oleh RAM yang tersedia saat ini, persentase memori yang dikonfigurasi, jumlah prosesor logis, dan
ukuran unit kerja yang diukur. Unggahan dan tampilan GPU memiliki anggaran VRAM terpisah. Dilaporkan paralel
kapasitas merupakan perkiraan sampai ubin yang representatif telah diukur.

Operasi mempertahankan satu pemilik untuk setiap elemen batas. Majelis memvalidasi batas-batas bersama,
menghapus duplikat, memeriksa jumlah dan batasan, dan mencatat parameter persis yang digunakan. Pekerjaan yang sama
unit dan format hasil nantinya dapat dijadwalkan di seluruh node sintesis terdistribusi.

## Aturan keselamatan

- Sampel global diberi label sebagai ikhtisar, bukan detail area pandang resolusi penuh.
- Ikhtisar tidak dapat menimpa atau mengekspor sebagai mesh sumber lengkap.
- Permintaan muatan penuh yang melebihi anggaran saat ini memerlukan pilihan yang jelas.
- Pembuatan indeks, pemrosesan ubin, dan perakitan tetap dapat dibatalkan dan mempertahankan yang sebelumnya
  keadaan lengkap.
- Nilai kapasitas merupakan perkiraan dan mengidentifikasi apakah nilai tersebut menggambarkan mesin saat ini atau yang direncanakan
  eksekusi ubin paralel.

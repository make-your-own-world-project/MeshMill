# Algoritma testi ve katkısı

MeshMill algoritmaları zor geometriyi yönetilebilir hale getirirken etkilerini de görünür tutmalı,
ölçülebilir ve bir sonuç uygulanmadan önce geri döndürülebilir.

## Referans fikstürleri

Bileşik örnek geometrisinin her iki paketlenmiş versiyonunu da kullanın:

- `samples/sample-scan.stl`, rutin geliştirme için otomatikleştirilmiş daha küçük normal Git donanımıdır
  kontrolleri ve kontrolleri öğrenme.
- `samples/original-scan.stl`, büyük dosya davranışı, yedekli katmanlar için tam Git LFS fikstürüdür.
  eşit olmayan yoğunluk, örtüşme ve performans çalışması.

Yedekli ve yoğun bölgeler kasıtlı test özellikleridir. Bir test onları hedefleyebilir, ancak
üst üste gelen her yüzeyin tek kullanımlık olduğu varsayılmamalıdır. Kompakt sentetik ağlar ekleyin
değişimin bilinen bir sınıra, eğriliğe, topolojiye, yoğunluğa veya örtüşme değişmezine ihtiyacı vardır.

## Karşılaştırma kontrol listesi

Bir algoritma veya parametre değişikliği için şunu kaydedin:

- MeshMill sürümü veya taahhüdü;
- giriş fikstürü ve sağlama toplamı;
- algoritma, kalite ön ayarı, hedef ve gelişmiş ayarlar;
- orijinal ve elde edilen üçgen ve köşe sayımları;
- küçültme yüzdesi, boyutlar ve boyut kayması;
- performans söz konusu olduğunda geçen süre ve en yüksek bellek;
- aynı kayıtlı görünümlerden ve görüntüleme modlarından ekran görüntüleri;
- görünür sınır, delik, kendi kendine kesişme, örtüşme veya bozulma değişiklikleri;
- sonucun tam ağdan mı yoksa yalnızca seçim işleminden mi geldiği.

Yalnızca başka bir ön ayar ile değil, aynı hedefteki mevcut davranışla da karşılaştırın.
farklı çıktı sayısı. Uygulanabildiği yerlerde gölgeli, yoğunluk, tel çerçeve ve köşe ekranlarını inceleyin.

## Kabul rehberliği

Bir optimizasyon değişikliği beklenmeyen boyut değişikliklerinden, bariz yüzey ters dönmesinden,
işlenen bölgeler arasında çatlaklar, anlamlı sınırların kaybı ve aynı anda büyük kalite gerilemeleri
benzer çıktı sayısı. Yoğunluğa yönelik değişiklikler, kaldırılan konsantrasyonun
kullanışlı eğrilik veya topoloji taşımaz.

Performans sonuçları işlemciyi, bellek kapasitesini, grafik donanımını, işletim sistemini tanımlamalıdır.
sistem, giriş boyutu ve verilerin önceden önbelleğe alınıp alınmadığı. Yapısal doğrulama ve ekran görüntüleri
incelemeyi destekler ancak kaynak geometrisine aşina olan katkıda bulunanların incelemesinin yerini almaz.

## Regresyon testleri

Açık toleranslara sahip deterministik testleri tercih edin. Yeni donanımları normal Git için yeterince küçük tutun,
kökenlerini ve lisanslarını belgeleyin ve gerçek kaynak verilerinin gerekli olmadığı durumlarda sentetik geometriyi kullanın.
Testler, bir işlemin geometriyi değiştirebildiği durumlarda iptali ve durumu geri yüklemeyi kapsamalıdır.

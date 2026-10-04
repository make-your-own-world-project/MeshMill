# Katkıda Bulunmak

Sorunlar ve çekme istekleri yoluyla katkılar memnuniyetle karşılanır.

## Proje kapsamı

MeshMill, büyük boyutlu, yoğun veya zor ağ dosyalarının aşağı yönde düzenleme ve düzenleme için yönetilebilir olmasını sağlar.
üretim iş akışları. Katkılar geometri incelemesini, ağ ve nokta yoğunluğunu geliştirmelidir
yönetim, optimizasyon, seçim, kırpma, temizleme, doğrulama, STL değişimi, performans,
veya bu operasyonların koordinasyonu.

Proje genel amaçlı modelleme, heykel, boyama, animasyon, render,
sahne kompozisyonu, malzemeler, donanım veya diğer içerik oluşturma sistemleri. Tanıtıcı teklifler
bu özellikler proje kapsamı dışındadır.

Yeni özellikler uygulamanın odaklanmasını sağlamalı, kaynağa dönüşen doğrudan iş akışlarını korumalıdır
geometriyi yönetilebilir ağlara dönüştürün ve destekleyici kontrolleri genel bir düzenlemeye dönüştürmekten kaçının
çevre.

## Yerelleştirme

İngilizce kullanıcı arayüzü kaynak metni `locales/en-US.json`'de saklanır. Yerel ayar meta verileri şurada saklanır:
`locales/manifest.json`. Çevrilmiş kullanıcı arayüzü katalogları aynı kararlı anahtarları ve dosya adını kullanır
`<locale>.json`. Çevrilmiş belgeler aşağıdaki eşleşen kök dosya adını kullanır:
`docs/locales/<locale>/`.

Etiketleri, araç ipuçlarını, iletişim kutularını veya kullanıcıların görebileceği diğer metinleri değiştirdikten sonra şunu çalıştırın:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Kaynak değişikliklerini ve yeniden oluşturulan anahtarları birlikte inceleyin.

## Geometri ve algoritma değişiklikleri

Optimizasyonu, yoğunluk analizini, seçimi, kırpmayı değiştirirken paket halindeki örnek geometriyi kullanın.
büyük dosya işleme veya görünüm karşılaştırma davranışı. Kasıtlı olarak gereksiz katmanlar içeriyor
ve eşit olmayan yoğunluk, dolayısıyla yararlı bir sonuç, distorsiyonu gizlemeden yönetilebilirliği geliştirmelidir,
anlamlı sınırları atmak veya başka bir algoritmanın koruduğu geometriyi sessizce kaldırmak.

Girişi, algoritmayı, ayarları, üçgen sayısını, boyutları, boyut kaymasını, geçen süreyi kaydedin,
ve karşılaştırmalar için ilgili ekran görüntüleri. Hem daha küçük normal Git fikstürünü hem de
değişiklik, orijinal Git LFS fikstürü olan büyük veya katmanlı geometriyle ilgilidir. Bir algoritmayı ayarlamayın
yalnızca bu fikstüre. Belirli bir değişmez veya regresyon için küçük sentetik durumlar ekleyin
test edildi.

Karşılaştırma kontrol listesi için [Algoritma testi ve katkısı](docs/ALGORITHM_TESTING.md) konusuna bakın.

## Geliştirme kurulumu

1. Windows'ye 64 bit Python 3.12'yi yükleyin.
2. Sanal bir ortam oluşturun ve etkinleştirin.
3. `requirements-dev.txt`'yi yükleyin.
4. GUI için `python meshmill.py`'yi veya CLI kullanımı için `python meshmill.py --help`'yi çalıştırın.
5. Bir değişikliği göndermeden önce `python -m py_compile meshmill.py`'yi çalıştırın.

Özel ağları, oluşturulan yürütülebilir dosyaları, özel bilgiler içeren ekran görüntülerini ve yerel verileri saklayın
taahhütlerden dizinler oluşturun. Yeniden dağıtılabilir test geometrisi `samples/` kapsamına girer.
kaynak, lisans, boyutlar ve üretim yöntemi belgelenmiştir. Yeni kaynak dosyalar şunu kullanmalıdır:
SPDX tanımlayıcı `GPL-3.0-or-later`.

Her belge ekran görüntüsünü MeshMill uygulama içeriğine göre kırpın. şunları dahil etmeyin:
görev çubuğu, ilgisiz pencere kromu, bildirimler, hesap ayrıntıları, özel yollar veya arka plan
masaüstü içeriği.

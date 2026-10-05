# MeshMill yol haritası

## Platform desteği

Windows ilk paketlenmiş platformdur. Uygulama mimarisi ve ağ formatları
platformlar arasıdır ve gelecek sürümlerde yerel Linux ve macOS paketleri eklenmelidir. Platform çalışması
paketleme, uygulama entegrasyonu, donanım ölçümleri, dosya sistemi davranışı ve otomatikleştirmeyi içerir
Desteklenen her sistemde aynı projeyi ve STL iş akışlarını korurken sürüm testi yapın.

- Linux x86-64 önizleme paketini dağıtımlar, masaüstü ortamları ve ekran genelinde doğrulayın
  kararlı hale getirmeden önce sunucular ve GPU sürücüleri.
- macOS Apple silikon ve x86-64 önizleme paketlerini gerçek donanımda doğrulayın, ardından Geliştiriciyi ekleyin
  Bunları istikrarlı hale getirmeden önce kimlik imzalama ve noter onayı.
- Paylaşılan bir arayüzün arkasına platformda yerel CPU, bellek ve GPU ölçüm sağlayıcıları ekleyin.
- Kaydedilen ayarları, klavye eşlemelerini, komut satırı davranışını ve proje verilerini taşınabilir tutun.

Bu yol haritası planlanan çalışmaları kaydeder. Geçerli sürümdeki özellikleri açıklamaz.

## Kapsam

MeshMill geometriyi, ağ yoğunluğunu, nokta yoğunluğunu, optimizasyonu, temizlemeyi, doğrulamayı ve STL'yi yönetir
o kadar büyük veya ağır ağ dosyaları değiştiriliyor ki, aşağı yöndeki düzenleme iş akışlarında kullanışlı olmaya devam ediyor.

Genel amaçlı modelleme, heykel, boyama, animasyon, render, sahne kompozisyonu, malzemeler,
hile ve diğer içerik oluşturma sistemleri bu yol haritasının dışındadır. Dağıtılmış sentez geçerlidir
MeshMill'nin ağ yönetimi işlemlerine uygundur ve ürünü genel bir düzenleyiciye genişletmez.

## Referans geometrisi

Paketlenmiş kompozit ağ, mevcut algoritmalar ve yol haritası için ortak geliştirme unsurudur
çalışmak. Kasıtlı olarak fazladan katmanları ve eşit olmayan yoğunluğu, tekrarlanabilir karşılaştırmaları destekler.
indirgeme kalitesi, yoğunluk analizi, örtüşme yönetimi, bölgesel işlemler, çekirdek dışı işleme,
ve gelecekteki sentez. Yol haritası uygulamaları bu fikstüre ve küçük
davranışı tek bir model için optimize etmek yerine, amaca yönelik oluşturulmuş regresyon ağları.

## Multi-STL çalışma alanları ve istatistiksel sentez

Bir çalışma alanı, birden fazla STL girişini ayrı, bağımsız olarak görülebilen kaynak nesneler olarak kabul etmelidir.
MeshMill bu kaynakları hizalamalı, geometrik uyumlarını ölçmeli ve kullanılabilir bir tanesini sentezlemelidir.
yinelenen iç yüzeyleri veya tekrarlanan örtüşme geometrisini korumadan ağ oluşturun.

Planlanan davranış:

- tek bir çalışma alanına birden fazla STL kaynağı ekleyin, kaldırın, gizleyin, yalıtın, yeniden sıralayın ve inceleyin;
- kaynak kimliğini, birimleri, dönüşümleri, sınırları, çözünürlüğü ve işlem geçmişini koruyun;
- manuel hizalama kontrolleri ve ölçülebilir uyum kalitesi ile otomatik kayıt sağlama;
- büyük girdilerin sınırlı kalması için kaynakları karşılaştırmadan önce uzamsal bölgelere bölmek;
- doluluk, en yakın yüzey mesafesi, normal uyum, yerel yoğunluk, varyans ve
  örtüşen bölgelerdeki gözlem sayısı;
- eşleşen yüzeyleri, çakışan yüzeyleri, tarama gürültüsünü, boşlukları ve benzersiz geometriyi sınıflandırabilir;
- İstatistiksel olarak uyumlu yüzeyleri, kaydedilen verilerle temsili bir yüzey halinde birleştirin.
  yinelenen üçgenleri üst üste koymak yerine güven;
- hiçbir dış şekil detayına katkıda bulunmayan kapalı, çakışan ve paylaşılan geometriyi kaldırın;
- örtüşmeyen kaynak geometrisini koruyun ve belirsiz bölgeleri görsel inceleme için ortaya çıkarın;
- bir tarama daha net veya daha ayrıntılı olduğunda kaynak başına ve bölge başına ağırlıklandırmaya izin verin;
- sentez sonrasında su geçirmezliği, sınırları, normalleri, boyutları ve topolojiyi doğrulamak;
- birleştirilmiş ağın tekrarlanabilir olması için kaynak kaynağını ve sentez parametrelerini kaydedin;
- beklenen üçgen sayısını, sınırları, kaldırılan örtüşmeyi ve güven dağılımını önceden önizleyin
  Sentezlenen sonucun işlenmesi.

Bu iş akışı, büyük ölçekli projeler için planlanan aynı çekirdek dışı uzamsal dizini ve iş birimi modelini kullanmalıdır.
ağlar. İstatistiksel karşılaştırma ve örtüşme konsolidasyonu da yerel düzeyde dağıtılabilir olmalıdır.
veya uzak MeshMill düğümleri.

## Dağıtılmış sentez

Bir MeshMill kümesi, birden fazla ağ üzerinde paralel olarak çalışan birden fazla düğümü koordine etmelidir.
iş istasyonları. Bir düğüm, atanmış bir bölgeyi inceleyebilir, seçebilir, azaltabilir, doğrulayabilir, onarabilir veya birleştirebilir veya
çalışma ünitesi. Katkılar incelenip bir araya getirilene kadar bağımsız olarak sürümlendirilmiş olarak kalır
paylaşılan bir nesne sürümüne.

Sistem şunları desteklemelidir:

- birden fazla operatörden ve otomatik düğümden eşzamanlı katkılar;
- deterministik iş birimi girdileri, parametreleri, bağımlılıkları ve çıktıları;
- CPU, GPU, bellek, algoritmalar ve mevcut yüke dayalı yetenek bilinçli planlama;
- Ağların, bölgelerin, doğrulama geçişlerinin ve sentez aşamalarının bağımlılığa duyarlı bölümlenmesi;
- duraklatma, devam ettirme, iptal etme, yeniden deneme, yeniden atama ve arıza giderme özellikleriyle dayanıklı kuyruklar;
- içeriğe yönelik yapılar ve düğümler arasındaki bütünlük kontrolleri;
- kayıtlı bir dizi kabul edilmiş katkı versiyonundan tekrarlanabilir sentez;
- daha sonra senkronize edilebilecek çevrimdışı veya aralıklı olarak bağlanan iş istasyonları;
- Katılımcı düğümler ve paylaşılan proje verileri üzerinde açık kontrol ile yerel öncelikli işlem.

## Sürümlü işbirliği

Her katkı, ana nesne versiyonunu, seçilen bölgeyi veya iş birimini, işlemi, işlemi kaydetmelidir.
parametreler, düğüm kimliği, zaman damgaları, bağımlılıklar, doğrulama sonuçları ve çıktı sağlama toplamı.

Planlanan işbirliği davranışı:

- projeler nesneleri, dalları, kontrol noktalarını, katkıları ve sentezlenmiş versiyonları içerir;
- katkıda bulunanlar birbirlerinin üzerine yazmadan aynı ana sürümden çalışabilirler;
- örtüşmeyen katkılar doğrulama sonrasında otomatik olarak birleştirilebilir;
- örtüşen geometri veya uyumsuz bağımlılıklar açık bir çatışma yaratır;
- çakışmalar görsel karşılaştırma, bölge düzeyinde seçim, yeniden temel oluşturma, yeniden çalıştırma ve manuel çözümleme sağlar;
- inceleme durumları beklemede, kabul edilmiş, reddedilmiş, değiştirilmiş, çelişkili ve dahil edilmiş durumları içerir;
- son sentez manifestosu her birleştirilmiş katkıyı ve bağımlılığı tanımlar.

## Koordinasyon Kullanıcı Arayüzü

Masaüstü uygulaması, ayrı bir komut satırı gerektirmeden dağıtılmış işi yönetmelidir
veya sunucu yönetimi iş akışı. Planlanan görünümler şunları içerir:

- **Projeler:** nesneler, dallar, sürümler, katkıda bulunanlar ve sentez durumu.
- **Küme:** bağlı iş istasyonları ve düğümler, özellikler, sistem durumu, yük ve geçerli atama.
- **Kuyruk:** bekleyen, etkin, duraklatılmış, engellenmiş, başarısız ve tamamlanmış iş birimleri.
- **Katkılar:** yazar, düğüm, üst sürüm, etkilenen bölge, parametreler, kontroller ve inceleme durumu.
- **Karşılaştırın:** senkronize 3D görünümler, geometri farklılıkları, ölçümler ve sınır incelemesi.
- **Çakışmalar:** çakışan bölgeler, bağımlılık çakışmaları, çözüm seçenekleri ve doğrulama sonuçları.
- **Sentez:** bağımlılık grafiği, toplu ilerleme, seçilen katkı versiyonları ve nihai çıktı.
- **Geçmiş:** dal grafiği, kontrol noktaları, birleştirmeler, sentezlenmiş versiyonlar ve tekrarlanabilirlik bildirimleri.

Görünüm alanı sahipliği, atanan bölgeleri, tamamlanan çalışmaları, bekleyen değişiklikleri, çakışmaları,
ve temel ağı değiştirmeden sürüm farklılıkları.

## Koordinasyon ve taşıma

İlk tasarım aşaması, bir aktarım seçmeden önce protokol sınırlarını tanımlamalıdır. Protokol
Koordinasyon meta verilerini büyük ağ yapıtlarından ayırmalı, devam ettirilebilir aktarımı desteklemeli ve
harici bir hesap veya barındırılan hizmet olmadan yerel bir ağda kullanılabilir durumda kalır.

Gerekli koordinasyon kavramları:

- koordinatör seçimi veya açıkça seçilmiş bir koordinatör;
- düğüm keşfi ve manuel düğüm kaydı;
- kimliği doğrulanmış oturumlar ve proje kapsamlı yetkilendirme;
- iş sahipliğine ilişkin kiralamalar ve kalp atışları;
- eş zamanlı iş sunumu ve sonuç kabulü;
- farklı MeshMill sürümleri arasında sürüm anlaşması;
- ilerleme, günlükler, doğrulama, hatalar ve yeniden denemeler için yapılandırılmış olaylar;
- koordinatör, iş istasyonu, ağ veya düğüm kesintisinden sonra kurtarma.

## Teslimat aşamaları

### Aşama 0: çekirdek dışı büyük ağ işleme

Dizin, akış, önbellek, iş birimi ve güvenlik sözleşmesi şurada belgelenmiştir:
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Tüm ağı ayırmadan önce üçgen sayısını ve çalışma belleğini tahmin edin.
- Büyük boyutlu ikili STL dosyalarını sınırlı, eşit şekilde örneklenmiş gezinme genel bakışları olarak açın.
- Tam çözünürlüklü geometriyi, deterministik örtüşme sınırlarıyla uzamsal küplere bölün.
- CPU ve bellek sınırları dahilinde bağımsız küpleri aynı anda okuyun, analiz edin ve optimize edin.
- Hata değerlendirmesi, adaylık gibi azaltma aşamaları için GPU hesaplama uygulamalarını karşılaştırın
  puanlama, uzamsal sorgular ve bağımsız iş birimi işleme. Bir sahneyi yalnızca şu durumlarda boşaltın:
  determinizmi, ağı azaltmadan ölçülebilir bir uçtan uca hız veya bellek avantajı sağlar
  kalite, topoloji garantileri veya uygun bir GPU'ya sahip olmayan sistemlerle uyumluluk.
- Bellekteki tüm mesh'i gerektirmek yerine, kabadan inceye görüntü alanı düzeylerini aktarın.
- Küp durumunu doğrudan görünüm alanında çizin: sıraya alınmış, okunuyor, işleniyor, tamamlandı ve başarısız oldu.
- Her küpü doldurarak küp başına ilerlemeyi gösterin ve yüksek düzeyde tam nesne görünümünü koruyun.
- İşlenmiş küpleri sınır doğrulama, kopya kaldırma ve tekrarlanabilir ayarlarla birleştirin.
- Daha sonraki aşamalarda yerel küp planlayıcıyı dağıtılmış sentez çalışma birimlerine genişletin.

### Aşama 1: versiyonlanmış yerel temel

- Nesne, işlem, katkı, dal ve bildirim formatlarını tanımlayın.
- Kaynak başına görünürlük, dönüşümler, meta veriler ve kökene sahip çoklu STL çalışma alanları ekleyin.
- Kayıt kalitesi ölçümlerini ve mekansal örtüşme sınıflandırmasını ekleyin.
- Yinelenen ve kapalı geometriyi kaldırırken istatistiksel olarak uyumlu yüzeyleri sentezleyin.
- Tek kaynağa özgü çatışmalar, boşluklar, güven ve geometri için görsel inceleme ekleyin.
- Uygulama oturumları boyunca yerel geçmişi sürdürün.
- Görsel ağ ve bölge karşılaştırmaları ekleyin.
- Operasyonları belirleyici ve bağımsız olarak tekrarlanabilir hale getirin.

### Aşama 2: koordineli yerel düğümler

- Çalışan düğümlerini bir iş istasyonunda çalıştırın.
- Kuyruğa alma, yetenek raporlaması, iş ataması ve iptali ekleyin.
- MeshMill kullanıcı arayüzünde düğüm ve iş birimi durumunu görüntüleyin.
- Bölümlemeyi ve sonuç derlemesini yerel olarak doğrulayın.

### Aşama 3: çoklu iş istasyonu sentezi

- Kimliği doğrulanmış LAN keşfi ve kaydını ekleyin.
- İçerik odaklı iş girdilerini ve sonuçlarını özgeçmiş desteğiyle aktarın.
- Birden fazla iş istasyonunda eşzamanlı çalışmayı koordine edin.
- Düğüm veya ağ arızasından sonra atamaları kurtarın.

### Aşama 4: işbirlikçi versiyon oluşturma

- Katkıda bulunanları, şubeleri, inceleme durumlarını ve izinleri ekleyin.
- Çakışmayan katkıları birleştirin.
- Çakışan veya bağımlılık çatışmalarını tespit edin ve çözün.
- Seçilen katkıları tekrarlanabilir bir nesne sürümünde sentezleyin.

### Aşama 5: Üretimin Sertleştirilmesi

- Protokol uyumluluk testleri ve karma sürüm işleme ekleyin.
- Denetim, bütünlük, yolsuzluk, kesinti ve kurtarma testleri ekleyin.
- Karşılaştırmalı planlama, bölümleme, aktarma, birleştirme ve sentez performansı.
- Belge dağıtımı, yedekleme, geçiş ve olay kurtarma.

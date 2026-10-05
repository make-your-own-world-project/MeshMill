<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

MeshMill; çok büyük boyutlu, yoğun veya karmaşık ağ (mesh) geometrilerini
yönetilebilir hale getirmeye odaklanmış bir masaüstü uygulamasıdır. Hızlı inceleme, yoğunluk analizi, bölgesel seçim, kırpma, silme
ve hesap oluşturma ya da geometri yükleme gerektirmeyen kontrollü ağ sadeleştirme imkanı sunar.

GPU ile hızlandırılmış OpenGL oluşturma, görüntü alanı gezinmesini, donanım toplamayı, yoğunluk görselleştirmeyi,
ve etkileşimli denetim duyarlı. Mesh azaltma şu anda ayrı yerel CPU çalışanlarında çalışmaktadır.
uzun geometri hesaplamalarını arayüzden uzak tutmak.

MeshMill; 3D tarayıcılar, CAD ve modelleme dışa aktarımları, yeniden yapılandırma süreçleri,
oluşturulan geometriler ve diğer STL kaynaklarından gelen ağlarla çalışır. Geometriyi sonraki aşamadaki düzenleyiciler,
üretim araçları ve diğer ağ iş akışları için hazırlar. Genel amaçlı modelleme, şekillendirme (sculpting), animasyon,
malzeme ve sahne oluşturma işlemleri kapsamı dışındadır.

## İndir

[GitHub Sürümleri](../../releases) sayfasından şu dosyalardan birini indirin:

- `MeshMill-<version>-windows-x64-setup.exe`: Başlat menüsü ve isteğe bağlı
  masaüstü kısayolları içeren, kullanıcıya özel yükleyici.
- `MeshMill-<version>-windows-x64-portable.zip`: Taşınabilir uygulama. Arşivin tamamını çıkartın,
  ardından `MeshMill.exe`'yi çalıştırın.

Her iki paket de uygulama çalışma zamanını (runtime) içerir. Son kullanıcılar Python, Node.js veya
bağımlılıklar. Kararlı sürüm, x64 donanımında Windows 10 ve Windows 11'i destekler.

İmzasız Linux x86-64 ve macOS Intel/Apple silikon önizleme paketleri de Sürümlerde görünebilir.
Yerel GitHub tarafından barındırılan çalıştırıcılar üzerine kuruludurlar ve paketlenmiş CLI ve örnek ağ duman testlerini geçerler.
ancak yine de gerçek donanım üzerinde test yapılması gerekiyor. Bkz. [Linux ve macOS önizleme testi](../../PLATFORM_TESTING.md)
Sonuçları yüklemeden veya raporlamadan önce.

İmzasız topluluk yapıları Windows SmartScreen veya macOS Gatekeeper uyarısı görüntüleyebilir. Sürüm
sağlama toplamları her sürümün yanında listelenir.

## Hızlı başlangıç

1. Bir STL açın.
2. Gölgeli (Shaded), Yoğunluk (Density), Tel Kafes (Wireframe) veya Köşeler (Vertices) görüntüleme modunda inceleyin.
3. Bir kalite seviyesi, algoritma ve hedef üçgen sayısı seçin.
4. Sonucu hesaplamak için **Optimize Et**'i seçin.
5. Orijinal ve optimize edilmiş ağları (mesh) karşılaştırın, ardından işlemi onaylamak için **Uygula**'yı seçin.
6. **Mevcut durumu kaydet**'i seçin veya `Ctrl+S` tuşuna basın.

MeshMill, yalnızca bir dosya veya ayar değiştiği için optimizasyonu asla başlatmaz.

## Yetenekler

- İkili (binary) ve ASCII STL girişi, ikili STL çıkışı
- Yoğunluk dengeli, şekil ve topoloji koruyucu Fast QEM indirgeme işlemi
- GPU ile hızlandırılmış OpenGL görünüm, donanım toplama ve yoğunluk görselleştirme
- Örgü azaltımı için yerel arka plan geometri çalışanları
- Gölgeli, yoğunluk, tel kafes (wireframe) ve köşe noktası (vertex) görüntüleme modları
- Sabit bir üçgen üst sınırı yerine geometriden türetilen otomatik hedefler
- Eklemeli çoklu bölge seçimi ile poligon seçimi
- Yalnızca seçili bölgeyi kırpma, silme veya optimize etme
- Önbelleğe alınmış orijinal, önceki ve mevcut ağ (mesh) karşılaştırması
- Uygulanan geometri değişiklikleri için geri alma ve yineleme
- Boyut sapması, indirgeme yüzdesi ve tahmini çıktı boyutu
- Milimetre, santimetre, metre, inç ve fit görüntüleme birimleri
- CPU, bellek, GPU ve geometri etkinliği metrikleri
- İkili STL dosyasının yapılandırılmış bellek bütçesini aşması durumunda sınırlı genel görünüm yükleme
- GUI ve komut satırı uygulamaları
- Hesap, telemetri, yükleme veya bulut bağımlılığı olmaksızın yerel işleme

## Azaltmadan önce geometriyi inceleyin

Gölgeli ekran, yüzeyin ve silüetin net bir görünümünü sağlar. Karşılaştırma yapmakta fayda var
Bir optimizasyon geçişi uygulamadan önce şeklin korunması.

![Paketlenmiş örnek ağı gösteren MeshMill gölgeli görünüm portu](../../images/meshmill-shaded.png)

Köşeler ekranı gerçek nokta dağılımını gösterir. Yoğun tarama bölgeleri, seyrek alanlar ve
örneklemedeki ani değişiklikler geometriyi değiştirmeden görülebilir. Genişletilmiş metrikler paneli
Mesh ile çalışırken CPU, bellek, GPU ve geometri işleme etkinliğini izler.

![MeshMill Vertices ekranı genişletilmiş performans ölçümleriyle birlikte](../../images/meshmill-vertices.png)

Tel Çerçeve ekranı doğrudan üçgen yapısını gösterir. Gereksiz yoğunluğun belirlenmesine yardımcı olur,
düzensiz üçgenleme ve basitleştirmenin önemli geometriyi ortadan kaldırabileceği bölgeler.

![Üçgen yoğunluğundaki değişimi gösteren MeshMill Tel Çerçeve ekranı](../../images/meshmill-wireframe.png)

## Örgü yoğunluğunu analiz edin

Yoğunluk ekranı, model genelinde göreceli yerel yoğunluğu eşler. Seyrek bölgeler serin kalırken
Giderek daha yoğun olan bölgeler daha parlak renklerle hareket ederek düzensiz örneklemeyi bir bakışta görünür hale getirir.

![Göreceli ağ yoğunluğunu gösteren MeshMill yoğunluk ekranı](../../images/meshmill-density.png)

Geçici bir optimizasyon değerlendirilirken yoğunluk mevcut kalır. Araç kutusu şunları bildirir:
algoritma, hedef, sonuçta ortaya çıkan üçgen ve köşe sayıları, azaltma yüzdesi, boyutlar ve
geçiş uygulanmadan önceki tahmini çıktı boyutu.

![Geçici optimizasyonu gösteren MeshMill Yoğunluk ekranı](../../images/meshmill-density-overview.png)

Dairesel büyüteci kullanarak bir bölgeyi incelemek için farenin sağ düğmesini basılı tutun. Büyütülmüş görünüm
imlecin merkezinde kalır ve ana kamera konumunu değiştirmeden yerel yoğunluğu ortaya çıkarır.

![Görünüm alanı büyüteci ile MeshMill Yoğunluk ekranı](../../images/meshmill-density-zoom.png)

## Görünüm kontrolleri

| Giriş | Eylem |
| --- | --- |
| Orta tuşla sürükleme | Yörünge hareketi (Orbit) |
| Shift + orta tuşla sürükleme | Kaydırma (Pan) |
| Fare tekerleği | İmlece doğru yakınlaştırma |
| Ctrl + fare tekerleği | Saat yönünde veya saat yönünün tersine döndürme |
| Ok tuşları | Görünüm merkezi etrafında yörünge hareketi |
| Ctrl + ok tuşları | Kaydırma (Pan) |
| Ctrl + Shift + Yukarı/Aşağı | Yakınlaştırma/Uzaklaştırma (Zoom) |
| Ctrl + Üst Karakter + Sol/Sağ | Rulo |
| `F1` / `F2` / `F3` / `F4` | Gölgeli / Yoğunluk / Tel Kafes / Tepe Noktaları |
| Sağ fare basılı tutma | Büyüteç |
| Shift + sol tıklama | Cetvel noktaları ekleme veya kaldırma |
| Ctrl + sola sürükle | Seçim çokgeni çizin |
| `Ctrl+C` | Çokgeni kaydedilen seçime ekleyin |
| `Ctrl+X` | Seçimi kırp |
| `Ctrl+Space` | Seçimi optimize edin |
| `Delete` | Seçimi sil |
| `Escape` | Etkin seçimi veya cetveli temizleyin |
| `Ctrl+Z` / `Ctrl+Y` | Geri al / yinele |
| `Ctrl+S` | Mevcut ağ durumunu kaydet |

Standart görünüm tuşları altı tuşlu gezinme bloğunu takip eder:

| Anahtar | Görüntüle | Ctrl + tuşu |
| --- | --- | --- |
| `Insert` | Sol | Geçerli yönlendirmeyi Sol |
| `Home` | Ön | Geçerli yönlendirmeyi Ön |
| `Page Up` | Sağ | Geçerli yönlendirmeyi Sağ |
| `Delete` | Seçim olmadığında en üstte | Geçerli yönlendirmeyi Üst |
| `End` | Geri | Geçerli yönlendirmeyi Geri |
| `Page Down` | Alt | Geçerli yönlendirmeyi Alt |

Bir görünümün kaydedilmesi aynı zamanda karşıt görünümü de günceller. Sol ve Sağ, Ön ve Arka ve Üst ve Alt
eşleştirilmiş olarak kalır. Onay iletişim kutusunda **Kaydet** varsayılan eylemdir; dolayısıyla Enter,
yönlendirme. Ön, hem Üst hem de Alt görünümlerin üstünde görünür.

Kısayollar Ayarlar'da değiştirilebilir veya sıfırlanabilir.

## Seçim iş akışı

Çokgen çizmek için Ctrl tuşunu basılı tutun ve sola sürükleyin. Yeniden şekillendirmek için köşeleri sürükleyin, eklemek için bir kenara sol tıklayın.
işaretleyin veya bir kenarı kaldırmak için sağ tıklayın. `Ctrl+C` ile daha fazla bölge ekleyin. Kamera gizlemelerini hareket ettirme
seçilen geometriyi korurken ekran alanı çokgenini kullanın.

Etkin seçimle yapılan optimizasyon yalnızca o seçimi etkiler. Sonuç geçicidir
**Uygula** seçilene kadar. **İptal** geçici sonucu iptal eder ve seçimi korur;
başka bir konfigürasyon denenebilir. Kırpma ve silme işlemleri, normal, geri alınamayan ağ düzenlemeleri haline gelir.

Seçim paneli, seçilen kümülatif köşeleri, üçgenleri, ağ payını, tahmini
boyut ve boyutlar. Eylemleri, tutulanları kırpar, ekler, optimize eder, siler, geri adım atar veya temizler
çevredeki geometriyi gizlemeden seçim.

![MeshMill, korunan bölgesel seçimi ve geometri istatistiklerini gösteriyor](../../images/meshmill-crop-selection.png)

## Büyük ağlar

İkili bir STL tahsis etmeden önce MeshMill, tahmini çalışma belleğini yapılandırılmış bellekle karşılaştırır.
Bellek bütçesi. Bütçenin üzerindeki bir dosya sınırlı, salt okunur bir genel bakış olarak açılır. Genel bakış raporları
kaynak üçgenin tamamı sayılır ancak tam değil örnek olduğu için düzenlemeyi ve dışa aktarmayı devre dışı bırakır
nesne. Dizine alınmış, yakınlaştırmaya bağımlı çekirdek dışı işleme planlanmıştır
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Komut satırı

`MeshMillCLI.exe` her iki sürüm paketine de dahildir:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Tüm seçenekler için `.\MeshMillCLI.exe --help`'yi çalıştırın. MeshMill, giriş dosyasının üzerine yazmayı reddediyor.

## Örnek geometri

Geliştirme örneğinin iki versiyonu mevcuttur. Örnek, kompozit bir ağdır.
kasıtlı olarak gereksiz geometri katmanları ve çeşitli yoğunluklar. Tarayıcısı olmayan insanlara
Algoritmaların karşılaştırılması, yoğunluğun incelenmesi, bölgesel operasyonların uygulanması için gerçekçi bir donanım,
ve yol haritası özelliklerinin geliştirilmesi. MeshMill taranmış giriş gerektirmez.

| Dosya | Üçgenler | Boyut | Teslimat | Şunun için en iyisi |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 11,9 MiB | Normal Git | Hızlı değerlendirme, CI ve kontrollerin öğrenilmesi |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196,8 MiB | Git LFS | Yoğun kaynak geometrisini ve geniş ağ performansını test etme |

Daha küçük örnek her normal klonla birlikte indirilir. El değmemiş orijinal isteğe bağlıdır ve
Git LFS aracılığıyla yönetiliyor, böylece sıradan depo geçmişini şişirmiyor. GitHub Masaüstü şunları içerir
Git LFS. Komut satırı kullanıcıları Git LFS'yi yükleyebilir ve çalıştırabilir:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Etiketli sürümler ayrıca Git kullanmayan kişiler için orijinal STL'yi doğrudan indirilebilecek şekilde yayınlar.
Kaynak, boyutlar ve sağlama toplamları için bkz. [`samples/README.md`](../../../samples/README.md).

Algoritmaya katkıda bulunanlar ayrıca şunları da okumalıdır:
İndirgemeyi karşılaştırmadan veya değiştirmeden önce [algoritma test kılavuzu](docs/ALGORITHM_TESTING.md)
davranış.

## STL birimleri

STL bir birimi kodlamaz. Model birimlerinin değiştirilmesi, etiketleri ve ölçümleri ölçeklendirmeden değiştirir
kaydedilen koordinatlar. Kaynak geometrisini tanımlayan birimi seçin.

## Gizlilik

MeshMill yerel dosyaları okur ve yazar. Hiçbir hesap, telemetri, yükleme, reklam veya
bulut işleme özelliği. Mevcut GPU metrik uygulaması yerel Windows performansını kullanıyor
sayaçlar. Linux ve macOS için eşdeğer yerel ölçüm sağlayıcıları planlanmaktadır.

Tanılama sorunlarını gidermek için geliştiriciler GUI'yi şununla başlatabilir:
`--diagnostic-log <local-file.jsonl>`. Günlük, giriş yönlendirmesini ve kamera durumunu yerel olarak kaydeder ve
normal kullanım sırasında devre dışı bırakılır.

## Geliştirme ve sürüm

Yerelleştirilmiş kullanıcı arayüzü metni ve belgeleri başlangıçta harici makine çevirisiyle üretilir
hizmetler ve yapısal hasar açısından otomatik olarak kontrol edilir. Makine çevirisi hala yapılabilir
doğal olmayan veya yanlış. Ana dilini konuşanların çevirileri gözden geçirmeleri ve düzeltmeleri teşvik edilir.
katkı süreci.

- [Katkıda Bulunuyor](CONTRIBUTING.md)
- [Yayınlama süreci](RELEASING.md)
- [Yol Haritası](ROADMAP.md)
- [Sorun Giderme](docs/TROUBLESHOOTING.md)
- [Üçüncü taraf bildirimleri](THIRD_PARTY_NOTICES.md)

## MeshMill'yi destekleyin

MeshMill bağımsız olarak geliştirilmiş ve bakımı yapılmıştır. Oku
[bu çalışmayı desteklemek neden önemlidir](SUPPORT.md) veya sürekli geliştirmeyi şu şekilde destekleyin:
[Bana bir Kahve Al](https://buymeacoffee.com/tednv).

MeshMill, GNU Genel Kamu Lisansı sürüm 3 veya üzeri kapsamında lisanslanmıştır. Bkz.
[`LICENSE`](../../../LICENSE).

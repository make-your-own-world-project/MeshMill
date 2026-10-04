# Çekirdek dışı ağ mimarisi

MeshMill'nin mevcut büyük dosya koruması, tam bir dosya ayırmadan önce çalışan belleği tahmin eder.
ağ. Yapılandırılmış bütçeyi aşan dosyalar sınırlı gezinme genel bakışları olarak açılabilir. bir
genel bakış örneklenmiş geometridir, bu şekilde gözle görülür şekilde tanımlanır ve bu şekilde düzenlenemez veya dışa aktarılamaz.
tam kaynak olmasına rağmen.

Yakınlaştırmaya bağlı gerçek ayrıntı, kalıcı bir uzamsal indeks gerektirir. Aşağıdaki tasarım bunu tanımlar
sonraki uygulama aşaması.

## Dizin formatı

Her kaynak ağı, aşağıdakileri içeren sürümlendirilmiş bir `.meshmill-index` dizini alır:

- `manifest.json`, kaynak boyutu, değişiklik süresi, örneklenmiş içerik karmaları, sınırlar ile birlikte,
  üçgen sayısı, indeks versiyonu, koordinat hassasiyeti ve seviye açıklamaları;
- sekizli düzey ve Morton koduyla adreslenen uzamsal döşemeler;
- işgal edilen her ana döşeme için kaba bir ekran ağı;
- yaprak döşemelerde tam çözünürlüklü üçgen kayıtları; Ve
- bölgesel operasyonlar ve montaj sırasında kullanılan sınır sahipliği ve örtüşen meta veriler.

Dizin oluşturma, kaynağı sınırlı bloklar halinde sırayla okur. Geçici döşeme çalıştırmalarını yazar ve
gerekli her dosya doğrulamayı geçtikten sonra manifest'i atomik olarak yayınlar. Kesintiye uğrayan veya
eski dizin manifest dosyasından algılanır ve tam dizin açılmadan devam ettirilebilir veya yeniden oluşturulabilir
bellekte örgü.

## Görünüm akışı akışı

Görünüm alanı, kamera kesikliğini ve ekran alanı hatasını kullanarak döşemeleri seçer. Kaba ana fayanslar
ilk olarak gösterildi. Görünür alt döşemeler, kamera yaklaştıkça ve ekran dışındayken bunların yerini alır.
düşük etkili fayanslar kaba kalır. RAM ve VRAM'nin bağımsız bütçeleri vardır ve en az son zamanlarda kullanılırlar
önbellekler. Ayrıntıyı serbest bırakmak hiçbir zaman kaba bütün nesne temsilini serbest bırakmaz.

Zamanlayıcı şu kutucuk durumlarını kaydeder: sıraya alınmış, okunuyor, işleniyor, yükleniyor, yerleşik, başarısız,
ve iptal edildi. Görünüm alanı küpleri duruma göre renklendirebilir ve her küpü kendi durumuyla orantılı olarak doldurabilir.
ilerleme. İptal, kısmi sonuçları kaldırır ve son tam gösterimi etkin bırakır.

## İşleme ve kapasite

Yerel iş birimi, bir döşeme artı işleminin gerektirdiği deterministik örtüşmeden oluşur. Eşzamanlılık
şu anda mevcut olan RAM, yapılandırılmış bellek yüzdesi, mantıksal işlemci sayısı ve
ölçülen iş birimi boyutu. GPU yükleme ve görüntülemenin ayrı bir VRAM bütçesi vardır. Paralel olarak rapor edildi
kapasite, temsili döşemeler ölçülene kadar bir tahmindir.

Operasyonlar, her sınır öğesi için bir sahibi korur. Montaj paylaşılan sınırları doğrular,
kopyaları kaldırır, sayıları ve sınırları kontrol eder ve kullanılan parametrelerin tamamını kaydeder. Aynı iş
birim ve sonuç formatı daha sonra dağıtılmış sentez düğümleri arasında programlanabilir.

## Güvenlik kuralları

- Genel bir örnek, tam çözünürlüklü görünüm ayrıntısı olarak değil, genel bakış olarak etiketlenir.
- Bir genel bakış, kaynak ağının tamamı olarak üzerine yazılamaz veya dışa aktarılamaz.
- Mevcut bütçeyi aşan tam yük talepleri açık bir seçim gerektirir.
- Dizin oluşturma, döşeme işleme ve birleştirme iptal edilebilir durumda kalır ve öncekiler korunur
  tam hali.
- Kapasite değerleri tahmindir ve mevcut motoru mu yoksa planlanan motoru mu tanımladıklarını belirtir.
  paralel döşeme uygulaması.

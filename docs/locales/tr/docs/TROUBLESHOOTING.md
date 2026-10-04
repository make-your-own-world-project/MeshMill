# Sorun giderme

## Windows indirmeyi engelliyor

İmzasız topluluk yapıları Microsoft Defender SmartScreen'i tetikleyebilir. İndirilenleri karşılaştırın
dosyasının aynı GitHub Sürümünden `SHA256SUMS.txt` ile SHA-256 karma değeri. İmzalı sürümler tanımlanır
yayıncıları Windows dosya özelliklerinde.

## Taşınabilir yapı başlamıyor

`MeshMill.exe`'yi çalıştırmadan önce ZIP'in tamamını çıkarın. Sonraki `_internal` dizini kalmalıdır
her iki yürütülebilir dosyaya da. Yürütülebilir dosyayı ZIP görüntüleyicinin içinden çalıştırmayın.

## Genel bakış olarak büyük bir STL açılır

Tahmini çalışma kümesi, Ayarlar'daki bellek bütçesini aşıyor. Genel bakış modu kasıtlı olarak
salt okunur. Bütçeyi yalnızca makinede yeterli kullanılabilir bellek olduğunda artırın veya
Düzenleme için açmadan önce meshleyin.

## Standart görünüm kaydedilmedi

Ctrl ile değiştirilmiş görünüm kısayoluna basın, ardından **Kaydet**'i seçin veya onay ekranında Enter'a basın
diyalog. Bir görünümün kaydedilmesi aynı zamanda tersini de günceller. Durum satırı kaydedilen görünümü bildirir.

## Gezinme kısayolları yanıt vermiyor

Önce herhangi bir kalıcı iletişim kutusunu kapatın. Özelleştirilmişyse Ayarlar'daki kısayolları inceleyin veya sıfırlayın.
varsayılan görünüm kısayolları Ekle, Giriş, Sayfa Yukarı, Sil, Sonlandır ve Sayfa Aşağı'yı kullanır.

## Yerel yönlendirme tanılama günlüğü oluşturma

Tanılama günlüğü varsayılan olarak devre dışıdır. Klavye yönlendirmesini ve kamera durumunu yerel olarak kaydetmek için:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Günlük, açılan dosya yolunu içerebilir. Paylaşmadan önce inceleyin ve düzenleyin. Mesh geometrisi değil
günlüğe yazılır.

## Sorun bildir

MeshMill sürümünü, Windows sürümünü, GPU modelini, ağ üçgen sayısını, tam eylemi içerir
sıra ve yükleyici paketinin mi yoksa taşınabilir paketin mi kullanıldığı. Yeniden dağıtılabilir örneği kullanın
mümkün olduğunda ağlayın. Özel taramaları veya tanılama günlüklerini önce incelemeden eklemeyin.

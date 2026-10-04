# MeshMill serbest bırakılıyor

Sürüm işlem hattı, GitHub tarafından barındırılan Windows çalıştırıcılarında Windows yapıtlarını oluşturur. Son kullanıcılar alır
bağımsız bir yükleyici veya taşınabilir ZIP kullanın ve Python, Node.js veya bağımlılıkları yüklemeyin.

Yerelleştirme kaynak kataloglarını oluşturmadan önce yenileyin ve doğrulayın:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## İlk halka açıklanmadan önce

1. Planlanan uygulama ve dokümantasyon çevirilerini tamamlayın ve doğrulayın.
2. GPL'yi ve üçüncü taraf bildirimlerini inceleyin.
3. Kurulumu, başlatmayı, STL yüklemeyi, optimizasyonu, dışa aktarmayı ve kaldırmayı temiz bir ortamda test edin
   Windows hesabı veya sanal makine.
4. CI'yi `samples/sample-scan.stl`'ye karşı çalıştırın. Her belge ekran görüntüsünü inceleyin ve kırpın
   görev çubuğu, MeshMill'nin parçası olmayan pencere kromu, bildirimler, özel yollar, hesap
   ayrıntıları ve ilgisiz masaüstü içeriğini yayınlamadan önce kontrol edin.
5. Depo-yerel Git yazarını, hesabın GitHub yanıtsız adresiyle yapılandırın.
   ilk taahhüt. `git config --local --get user.email` ile onaylayın.
6. İsteğe bağlı Authenticode imzalama sırlarını yapılandırın:
   - `WINDOWS_CERTIFICATE_BASE64`: Base64 kodlu PFX sertifikası.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX şifresi.

İmza sertifikası olmadan oluşturulan dosyalar çalışmaya devam eder ancak Windows SmartScreen görüntülenebilir
Tanınmayan yayıncı uyarısı. İmzasız yapıları imzalı veya güvenilir olarak tanımlamayın.

## Orijinal tarama ve Git LFS

`samples/original-scan.stl`, GitHub'nin normal 100 MiB'ını aştığı için Git LFS aracılığıyla izleniyor
dosya sınırı. İlk taahhütten önce şunları doğrulayın:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Filtre `lfs` olmalı ve işaretçi nesne kimliği `samples/SHA256SUMS.txt` ile eşleşmelidir. Sürüm
iş akışı, LFS içeriğini kontrol eder ve orijinal STL'yi ayrı bir yayın varlığı olarak yayınlar. CI kullanımları
daha küçük normal Git örneğidir ve LFS nesnesini indirmez.

## Bir sürüm yapısını yayınlamadan test etme

**Eylemler**'i açın, **Yayın**'ı seçin, **İş akışını çalıştır**'ı seçin ve gibi sayısal bir sürüm girin.
`0.1.0`. Manuel çalıştırma, test amacıyla iş akışı yapıtlarını yükler ancak genel bir GitHub oluşturmaz
Serbest bırakın.

## Sürüm yayınlama

Temiz, incelenmiş bir `main` şubesinden:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Etiket, yayınlama iş akışını başlatır. Bu:

1. sabitlenmiş yapı bağımlılıklarını yükler;
2. eşleşen Windows sürüm meta verilerini oluşturur;
3. bağımsız GUI ve CLI yürütülebilir dosyalarını oluşturur;
4. İmzalama sırları yapılandırıldığında yürütülebilir dosyaları imzalar;
5. kullanıcı başına Inno Kurulum yükleyicisini oluşturur;
6. yapılandırıldığında yükleyiciyi imzalar;
7. taşınabilir ZIP ve SHA-256 sağlama toplamı dosyasını oluşturur;
8. iş akışı yapıtlarını yükler;
9. Aktarılan etiket için GitHub Sürümünü oluşturur.

Sürümü duyurmadan önce yükleyiciyi ve taşınabilir arşivi temiz bir Windows sisteminde doğrulayın.
Kaynağı aynı sürüm etiketi altında mevcut olan her dağıtılmış ikili dosyaya karşılık gelen şekilde tutun.
İlkini etiketlemeden önce GitHub düğmesinin nihai genel depo URL'sine işaret ettiğini doğrulayın
serbest bırakın.

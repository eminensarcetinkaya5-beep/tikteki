# TikTeki — İlk çalışan temel sürüm

Bu paket mevcut GitHub/Vercel siten için hazırlanmıştır. Hesabında yayın veya Firebase ayarı değiştirilmedi. Gerçek bağlantı bilgilerin assets/app.js içinde bulunuyor. Bu web yapılandırması bir yönetici özel anahtarı değildir.

## 1. Dosyaları GitHub'a yükle

Önce mevcut index.html dosyanın yedeğini al. ZIP'i aç. index.html dosyasını ve assets klasörünü GitHub'daki tikteki deponun ana dizinine yükle. assets klasörünün içinde app.js ve style.css bulunmalı. Dosyaları fazladan bir tikteki klasörünün içine koyma. api/index.py ve requirements.txt dosyalarını değiştirmen gerekmiyor. Commit changes ile kaydet ve Vercel dağıtımının tamamlanmasını bekle.

## 2. Authentication

Google ve Email/Password sağlayıcıları açık olmalı. Authentication → Settings → Authorized domains listesinde tikteki.vercel.app bulunmalı. Mevcut Firebase projesindeki tüm uygulamalar aynı kullanıcı havuzunu paylaşır; TikTeki için ayrı kullanıcı havuzu istersen ayrı Firebase projesi gerekir.

## 3. Realtime Database

Bu sürüm Firestore değil, mevcut Realtime Database kullanır. Veriler yalnızca tiktekiV1 dalına yazılır.

Firebase → Realtime Database → Rules bölümünde mevcut kuralları YEDEKLE. setup/database.rules.json güvenli, bağımsız bir başlangıç kural dosyasıdır. Mevcut projede başka uygulamalar olduğundan tüm kuralları körlemesine bununla değiştirme. Mevcut rules nesnesine dosyadaki tiktekiV1 nesnesini ekle; diğer uygulama kurallarını koru. Üst seviyede .read:true / .write:true veya bütün oturum açmış kullanıcılara genel erişim varsa bunlar alt kuralları geçersiz kılar. Bu durumda önce mevcut kuralları uygulama dallarına ayırmak gerekir. Mevcut kurallarını paylaşırsan doğru birleşim hazırlanabilir.

Bağımsız, başka veri kullanmayan bir projede dosyanın tamamını kullanabilirsin. Publish ile yayınla. Kurallar e-posta adreslerini veya şifreleri veritabanına kaydetmez. Profil görünen adları ve biyografiler giriş yapan kullanıcılara açıktır. Favoriler ve takip edilenler yalnızca hesap sahibine okunabilir. Videolar, beğeniler ve yorumlar giriş yapanlara açıktır. Video, yorum, beğeni ve takip yazımları doğrulanmış e-posta gerektirir. Profili ve favorileri kullanıcı yalnızca kendi hesabında değiştirebilir.

## 4. Video deposu

Firebase → Storage → Get started ile Cloud Storage deposunu kur. Bu ürün Blaze (kullanıma göre ödemeli) plan gerektirir; Spark planındaki projede yükleme açılmaz. Paket herhangi bir ücretli plana geçiş yapmaz. Bu maliyeti kabul etmiyorsan Storage'ı etkinleştirme; giriş ve metin profilini kullanabilirsin. İstersen daha sonra farklı bir video sağlayıcısı bağlanabilir.

https://firebase.google.com/docs/storage/web/start

Beklenen depo: sohbet-uygulamasi-35fd4.firebasestorage.app. Farklı depo oluşturursan assets/app.js içindeki storageBucket ve mediaURL kontrolü ile database.rules.json içindeki URL doğrulamasını birlikte güncelle.

Storage → Rules bölümünde setup/storage.rules dosyasındaki tiktekiV1 eşleşmesini mevcut kurallara ekle. Diğer uygulamaların yollarını koru; herkese bütün yolları yazma izni veren genel eşleşme kullanma. Bağımsız projede dosyanın tamamı kullanılabilir.

Bu sürüm yalnızca açık video paylaşımı içindir. getDownloadURL bağlantıları erişim belirteci içerir; bağlantıya sahip kişiler videoyu indirebilir. Özel video özelliği yoktur. MP4/WebM/MOV kabul edilir, en fazla 50 MB. Tarayıcıda oynatma codec desteğine bağlıdır; sunucuda format dönüştürme yapılmaz. Dosya türü/boyutu kontrolleri içerik moderasyonu veya zararlı dosya taraması değildir.

## 5. İlk deneme

Chrome'da https://tikteki.vercel.app aç. Google ile giriş yap veya e-postayla hesap oluştur. E-postayla kaydolduysan gelen bağlantıyı açıp uygulamada Doğruladım'a bas. Profilini kaydet. + ile kısa bir video seç, önizle ve paylaş. İkinci bir hesapla beğenme, yorum ve takip işlemlerini dene. İlk hesapla videoyu sil; başka hesabın videoyu silememesi gerekir.

## Bu pakette uygulananlar

- Google ve e-posta/şifre üyeliği, giriş, oturum takibi, çıkış
- E-posta doğrulaması, yeniden gönderme, şifre sıfırlama
- Görünen ad ve biyografi düzenleme (benzersiz @kullanıcı adı değildir)
- Video seçme, önizleme, yükleme yüzdesi, yükleme iptali
- Video açıklaması, dosya boyutu ve tür kontrolü
- Son 100 video için tarih sıralı akış ve açıklama/etiket araması
- Yerel video kontrolleri, döngü, ekrandan çıkınca durdurma
- Takip/takipten çıkma ve son 100 video içinden takip akışı
- Beğeni/geri alma ve gerçek zamanlı beğeni sayısı
- Favoriye kaydetme/çıkarma ve kaydedilenler akışı
- Son 100 yorum, yorum ekleme ve yetkili silme
- Telefon paylaşım menüsü veya bağlantı kopyalama
- Profilde kendi videoları, video/takip sayısı
- Video sahibinin video, yorum ve beğeni kayıtlarını silmesi
- Boş durumlar, hata mesajları ve mobil uyum

Akış Yenile ile güncellenir; yapay zekâ önerisi veya sınırsız sayfalama yoktur. Diğer kullanıcıların silinen videolara ait favori işaretleri kalabilir; akışta gösterilmez. Upload sırasında sekme kapanırsa sahipsiz dosyalar için ileride sunucu temizleme işi gerekir.

## Sonraki aşama

Mesajlaşma, bildirimler, avatar yükleme, benzersiz kullanıcı adları, engelleme/şikâyet/moderasyon, özel hesap, hesap silme, video düzenleme, müzik lisansları, altyazı, düet, canlı yayın, öneri sistemi ve diğer 100 maddelik listedeki işlevler BU sürümde bulunmaz. Sahte buton olarak eklenmediler. Bu ilk sürüm kontrollü test içindir; halka açık geniş kullanımdan önce moderasyon, sunucuda hız sınırı, App Check, maliyet izleme, sayfalama ve güvenlik kurallarının emülatör testleri eklenmeli.

## Doğrulama sınırı

JavaScript sözdizimi, HTML bağlantıları ve SDK yerine test nesneleri kullanan işlev testleri yerelde kontrol edildi. Buradan gerçek Firebase hesabında giriş/video yükleme veya kuralların emülatör çalıştırması yapılamadı. Sonuçlar ancak yukarıdaki kurulumdan sonra canlı ortamda doğrulanabilir.

Kaynaklar: https://firebase.google.com/docs/auth/web/google-signin ve https://firebase.google.com/docs/database/security

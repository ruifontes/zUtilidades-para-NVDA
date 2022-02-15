# zAraçlar Kılavuzu

* Yazar: Héctor J. Benitez Corredera  
* NVDA uyumluluğu: 2019.3 2021.1
* [Eklentiyi İndir:](https://nvda.es/files/get.php?file=zUtilidades)  
* [Github Projesi:](https://github.com/hxebolax/zUtilidades-para-NVDA)  

---

İçindekiler<a id="Índice"></a>
-------------
- [Başlarken](#mark0)
- [Uygulama Başlatıcı Modülü](#mark1)
- [Ana ekran](#mark2)
- [Kategori listesi](#mark3)
- [Eylem listesi](#mark4)
- [Eylem Ekle](#mark5)
- [eylemi düzenle](#mark6)
- [Eylemi Silme](#mark7)
- [Menü butonu](#mark8)
- [Hızlı tuşlar](#mark9)
- [Yazarın açıklamaları](#mark10)
- [Çabuk Notlar modülü](#mark11)
- [Her yerden hızlı bir not ekleyin](#mark12)
- [Uygulama Başlatıcı ve Çabuk Notlar için Sanal Menüler](#mark13)
- [Çevirmenler ve ortak çalışanlar](#mark14)
- [Sürüm Geçmişi](#mark15)
- [Sürüm 0.2.3](#mark0.2.3)
- [Sürüm 0.2.2](#mark0.2.2)
- [Sürüm 0.2.1](#mark0.2.1)
- [Sürüm 0.2](#mark0.2)
- [Sürüm 0.1.6](#mark0.1.6)
- [Sürüm 0.1.5](#mark0.1.5)
- [Sürüm 0.1](#mark0.1)

---

# Başlarken<a id="mark0"></a>

zAraçlar, NVDA için bir dizi küçük uygulama olarak tasarlanmıştır.  

İlgi duyulabilecek uygulamaların eklenmesi için çalışmalar devam edecek. Böylece kolay arayüz ile erişilebilir olacaklardır.  

zAraçlar eklentisinin NVDA Araçlar menüsünde bir menüsü olacaktır, bu menüde farklı modüller eklenecektir.  

Bütün modüller, NVDA menüsü / Tercihler / Girdi hareketleri'ne giderek zAraçlar seçeneği içerisinde bulunur ve kısa yol eklenebilir.  

Varsayılan olarak modüller herhangi bir Kısayol atanmadan gelir.  

Bu nedenle, Araçlar / zAraçlar menüsüne giderek veya her modül için bir tuş kombinasyonu atayarak modülleri çalıştırabiliriz.  

Eklenti, şu anda aşağıdaki modüllerden oluşmaktadır:  

* Uygulama başlatıcı.  
* Çabuk Notlar.  

# Uygulama Başlatıcı Modülü<a id="mark1"></a>

Bu modül, ister taşınabilir ister kurulu olsun, bilgisayarımızın herhangi bir yerinden bir uygulamayı hızlı bir şekilde başlatmamızı sağlayacaktır.  

## Ana ekran<a id="mark2"></a>

Ana ekran bir kategori listesi, bir Eylem listesi ve bir Menü düğmesinden oluşur.  

Sekme tuşu ile aralarında dolaşabiliriz.  

### Kategori listesi<a id="mark3"></a>

Bu alanda kategori ekleyebilir, düzenleyebilir veya silebilir, uygulamalarımızı istediğimiz gibi kategoriler halinde sıralayabiliriz.  

Ekle, Düzenle veya Sil seçeneklerine iki şekilde ulaşabiliriz.  

Kategoriler alanında Uygulama veya Shift+F10 tuşlarına bastığımızda üç seçenekten birini seçebileceğimiz bir menü görüntülenecektir.  

Hem ekleme hem de düzenleme diyalogları çok basittir, yeni kategorinin adını koyabileceğimiz veya seçtiğimiz kategoriyi düzenleyebileceğimiz tek bir metin alanına, Kabul Et ve İptal Et düğmelerine sahiptir.  

Listeden bir kategori seçip silindiğinde, içerisinde bulunan bütün eylemlerin ve veritabanında bulunan programların geri alınamaz şekilde silineceğini unutmamalıyız. Hepsini yeniden tanımlamamız gerekir.  

Bu seçeneklere Menü butonuna basarak veya Alt+M tuş kombinasyonunu kullanarak da ulaşabiliriz. Önceki 3 seçenekten birini seçebileceğimiz Kategoriler adlı bir alt menü ile diğer seçenekleri içeren bir menü görüntülenecektir.  

Düzenle ve Sil seçeneğinin her zaman odaklanılan kategoride olacağını ve kategori olmaması durumunda ilgili seçenekleri kullanamayacağımızı unutmamalıyız.  

Kategoriyi sıralamak üzere taşımak için Alt + Yukarı Ok ve Aşağı Ok tuş kombinasyonlarını da kullanabiliriz.  

### Eylem listesi<a id="mark4"></a>

Bu alan, seçtiğimiz kategoriye eklediğimiz Eylemlerin görüldüğü yerdir.  

Eylem Ekle, Eylemi Düzenle veya Eylemi Sil olmak üzere üç seçenek bulunur.  

Bu seçenekleri kategori listesinde olduğu gibi, Uygulama tuşu, Shift + F10 ile hızlıca açabilir veya Menü düğmesine (Alt + M) ile gidip Eylemler alt menüsüne erişebiliriz.  

Bu Eylem listesinde, boşluk tuşuna basarak seçili olan uygulamayı başlatabiliriz.  

listeyi sıralamak üzere taşımak için Alt + Yukarı Ok ve Aşağı Ok tuş kombinasyonlarını da kullanabiliriz.  

Bu alanda dilediğimiz bir harfe basarak farklı girdiler arasında hızlıca gezinebiliriz, böylece veritabanında çok sayıda Eylem varsa çalıştırmak istediğimiz uygulamayı hızlıca bulabiliriz.  

#### Eylem ekle menüsü<a id="mark5"></a>

Bu menüde aşağıdaki seçenekler arasından seçim yapabiliriz:  

* Uygulama ekle:  

Bir uygulama eklersek, gerekli olan iki alan vardır ve bunlar uygulamanın adı ve uygulamamızın bulunduğu dizindir.  

Şu anda eklenti, exe, bat ve com uzantılarına sahip uygulamaları desteklemektedir.  

Zorunlu alanlar doldurulduktan sonra, uygulamanın ek parametreler gerektirmesi veya uygulamayı yönetici modunda çalıştırmak isteyip istemediğimizi seçebiliriz.  

Bir uygulamayı yönetici modunda çalıştırmak istiyorsak, uygulamayı başlattığımızda ilgili izin istenecektir.  

* CMD komutu ekle.  

Bu iletişim kutusunda konsol komutları ekleyebiliriz.  

Komutu tanımlamak için ad  ve komutlar alanını doldurmak gereklidir.  

Birkaç takdir, Windows PowerShell'de ustalaşırsak cmd komutlarını başlatmanın yanı sıra, PowerShell'i komut satırına koyarsak ve ardından istediğimizi izlersek, PowerShell komutlarını da çalıştıracağız.  

Aynı şekilde, bunlar CMD komutlarıysa, Shift + 6 ile, bunu İspanyolca QWERTY klavye ile yaparak elde edilen (Bölü) sembolüyle ayrılması gereken birkaç satırı çalıştırabileceğimizi ekliyorum. İngilizce QWERTY klavye kullanıyorsanız, bu Shift+7 ile yapılacaktır.  

Windows Gezgini'ni yeniden başlatmak için komut satırına bir örnek koydum, bir komut satırını diğerinden ayırmak için (Bölü) sembolünü kullandığımı göreceksiniz.  

`taskkill /f /im explorer.exe & start explorer`  

Ayrıca bu iletişim kutusunda, konsolun kapanmaması ve sonuçları görebilmemiz için bir duraklama koyabiliriz.  

Yönetici olarak da çalıştırabiliriz.  

* Klasör erişimi ekle.  

Bu iletişim kutusunda, klasöre erişimi tanımlamak için bir ad belirtmemiz ve bir klasör seçmemiz gerekecek.  

Bu, sistem klasörlerimizi her yerden hızlı bir şekilde açmamızı sağlayacaktır.  

* Windows çalıştır kısayolları ekle.  

Bu iletişim kutusunda başlatmak için bir kısayol seçebiliriz. Ayrıca yönetici olarak başlatmak isteyip istemediğimizi de seçebiliriz.  

Kısayol adını ve yolunu tanımlayan alanlar gereklidir.  

* Yüklü uygulama ekle.  

Bu iletişim kutusunda, bilgisayarımıza yüklenen tüm uygulamalar, kullanıcı tarafından eklenen veya Windows ile birlikte gelenler görüntülenecektir.  

Ayrıca bu ekranda Windows mağazasından yüklenen uygulamaları seçebiliriz.  

Uyarı bu, Windows 7 için geçerli değildir.  

Bu iletişim kutusundan bir uygulama eklendiğinde, düzenlenemeyeceğini, düzenleme gerekiyorsa silip yeniden eklememiz gerektiğini unutmamalıyız.  

Bu iletişim kutusundaki yönetici seçeneği tüm uygulamalar için çalışmayacaktır. Yalnızca yönetici ayrıcalıklarının yükseltilmesine izin verenler için çalışır.  

Ayrıca, bu iletişim kutusunda, uygulamalar tarafından yüklenen erişimlerin de görüneceği konusunda uyarmalıyız. Bunları seçebiliriz ama bazıları hata vererek açılmasına izin vermeyebilir.  

Ayrıca dikkatli olmanız gerektiğini de unutmayın. çünkü bu listede yönetmek için olabilecek uygulamalar olacak, ne için olduklarını bilmiyorsak onlara dokunmamak daha iyidir.  

#### eylemi düzenle<a id="mark6"></a>

Düzenle iletişim kutusu, Eylem Ekle iletişim kutusuyla tamamen aynıdır, ancak seçtiğimiz girişi değiştirmemize izin verecektir.  

Yüklü uygulama ekle seçeneği tarafından eklenenler dışındaki tüm öğeleri değiştirmemize izin verecek, diyaloglar eklenecek seçeneklerdekiyle aynı olacaktır.  

#### Eylemi Sil<a id="mark7"></a>

Bir girdiyi silersek, bu eylemin geri alınamayacağını hesaba katmalıyız.  

### Menü butonu<a id="mark8"></a>

Bu düğmeye, Alt+M kombinasyonuna basılarak arabirimin herhangi bir yerinden erişilebilir.  

Bu menüde Kategoriler, Eylemler, Yedekle veya geri yükle ve Seçenekler olmak üzere dört alt menü bulacağız, Ayrıca Çıkış seçeneği de bulunur.  

Kategoriler ve Eylemler yukarıda açıklandığından, Yedekle ve Geri yükle ile Seçenekler'i açıklayacağız:  

Pekala, Yedekle seçeneğini seçersek, veritabanı yedeğimizi nereye kaydedeceğimizi seçmemiz gereken bir Windows kaydetme penceresi açılacaktır.  

Ddosya adı varsayılan olarak şöyle bir şeydir:

`Backup-03052021230645.zut-zl`  

Uzantı varsayılan olarak ayarlanmıştır, adı modüle karşılık gelir ve oluşturulduğu tarihi içerir, böylece istediğimiz adı koyabiliriz.  

Kaydedildikten sonra, veritabanımızın bozulması, yanlışlıkla silmemiz veya kaydettiğimiz bir sürüme geri dönmek istememiz durumunda onu geri yükleyebiliriz.  

Peki, Geri Yükle seçeneğini seçiyoruz ve dosyaları açmak için klasik bir Windows penceresi açılacak.  

Kaydettiğimiz *.zut-zl uzantılı kopyayı seçmeliyiz, dosyayı bulamazsanız uzantıyı değiştirmemeye dikkat edin.  

Seçildiğinde, yedekleme geri yüklenecek, Tamam'a tıkladığımızda eklenti kapanacak ve bir sonraki açışımızda kopyamız geri yüklenecektir.  

*.zut-zl dosyalarının gerçekten sıkıştırılmış dosyalar olduğunu unutmayın. ancak bunları değiştirirken dikkatli olun çünkü bunlar değiştirilirse imza eşleşmez ve bu onları geri yüklemenize izin vermez.  

Demek istediğim, bu dosyaların, geri yükleme sırasında eşleşmezse başarısız olacağı ve her imzanın her dosya için farklı olduğu bir imzası var.  

Seçenekler alt menüsünde artık yalnızca uygulama başlatıcısının varsayılan değerlerine dön seçeneği var.  

Bu seçeneği seçersek, tüm veritabanı silinecek ve eklenti yeni kurulmuş gibi sıfırlanacaktır.  

## Hızlı tuşlar<a id="mark9"></a>

Hem kategori, hem de Uygulamalar alanlarında kısayol tuşlarını şöyle sıralayabiliriz:  

* Alt + Yukarı Ok veya Aşağı Ok: Kategori veya Eylem listesinde ögeler arasında gezinmeyi sağlar. Liste başına vbeya sonuna ulaşıldığı zaman bir sesle daha fazla gidilemeyeceği belirtilir.  
* Alt + K: Hızlıca Kategori listesine gider.  
* Alt + L: Uygulamaların bulunduğu Eylem listesine gider.  
* Alt + M: Menüyü açar.  
* Uygulama tuşu veya Shift + F10: Kategori veya eylem listesinde, seçeneklerin bulunduğu içerik menüsü görüntülenir.  
* Boşluk çubuğu: Eylem listesinde seçili olan uygulama etkinleştirilir.  
* Escape: Ana Uygulama Başlatıcı ekranı da dahil olmak üzere uygulamanın açabileceği tüm iletişim kutularını kapatır.  

## Yazarın açıklamaları<a id="mark10"></a>

Bir uygulamayı başlattığımızda Uygulama başlatıcı penceresi kapanır. Başka bir uygulama başlatabilmek için aynı pencereyi tekrar açmamız gerekir.  

Ayrıca, kategorinin konumunu ve en son ziyaret edilen uygulamayı kaydedecek bir işlev de uygulandı, bu nedenle Uygulama Başlatıcı'yı açtığımızda, söz konusu kategorinin hem son kategorisi hem de son uygulaması her zaman seçili olarak gelecektir.  

Odak kaydetme özelliği eklendiğinden, eklenti penceresini her açtığımızda son seçili odakta açılacaktır.  

Örneğin: Menü düğmesi seçili durumdayken Uygulama başlatıcı penceresini kapatıp, tekrar açtığımızda aynı buton üzerine odaklanmış olduğunu görürüz.  

Bu özellikler NVDA yeniden başlatılana kadar geçerlidir. Ekran okuyucuyu yeniden başlatıp Uygulama başlatıcıyı açtığımızda Kategoriler listesine odaklandığını görürüz.  

Bu eklenti, Windows 10 ile kullanılmak üzere yapılmıştır, bu nedenle önceki sürümleri kullanıyorsanız ve herhangi bir sorun yaşarsanız lütfen bana bildirin, ancak bazı özellikler yalnızca Windows 10'da bulunduğundan kesinlikle hiçbir şey yapamam.  

# Çabuk Notlar modülü<a id="mark11"></a>

Bu modül, elimizin altında danışabileceğimiz, düzenleyebileceğimiz, silebileceğimiz küçük notlara sahip olmamıza yardımcı olacaktır.  

Modül, Uygulama Başlatıcı ile aynı işleme sahiptir ancak aşağıda açıklanan bazı tuşlarda değişiklik gösterir.  

Yedekleme yapabileceğimiz, geri yükleyebileceğimiz, eklentiyi varsayılan değerlere döndürebileceğimiz, kategorileri ve notları yönetebileceğimiz menüyü açıklamayacağım.  

Ayrıca arayüzü de tamamen aynı olduğu için tekrar açıklamayacağım.  

Çabuk bir şekilde Not ekleyebilir, Notun adını girebnilir ve sekme tuşuna basarak içeriğini de belirtebiliriz.  

Notu düzenle iletişim kutusu da tamamen aynıdır, verilen ad değiştirilebilir ve içeriği de düzenlenebilir.  

Bu modül, bazı ek tuş kombinasyonları kullanması bakımından uygulama başlatıcı modülünden şu farklılıkları gösterir:  

* F1: Bir notun üstündeyken F1'e basarsak notun içeriğini bize okuyacaktır.  
* F2: Seçili notu panoya kopyalar. Bu şekilde dilediğimiz yazma alanına içeriğini yapıştırabiliriz.  
* F3: Bu kombinasyon Çabuk notlar penceresini kapatır ve odaklandığımız notun içeriğini aktif olan bir yazma alanına yapıştırır, yani Not Defteri, bir e-posta alanı, Word vb.  

Örnek: Not defteri uygulaması açıkken Çabuk notlar uygulamasını çalıştırıp, bir not seçip ve F3 tuşuna basarsak ilgili not kopyalanır. Çabuk notlar penceresi kapanır ve ilgili not içeriği not defteri içerisine yapıştırılır.  

Ancak Masaüstü aktifken aynı işlemler gerçekleştirilirse hiçbir şey olmadığı görülür.  

Ayrıca hem kategoriler alanında hem de not listesi alanında çalışmaya devam ediyor, bu alanları Alt+Oklarla yukarı aşağı sıralayarak seçtiklerimizi hareket ettirebiliyoruz.  

Boşluk tuşuna basarsak, sadece seçili not içeriğini görebileceğimiz bir pencere açılacaktır.  

Bu modül için de tanımlı bir kısayol bulunmadığından, Girdi hareketleri iletişim kutusundan dilediğimiz tuş bileşenlerini atayabiliriz.  

Menü butonu ile açılan içeriğe Seçenekler adlı bir iletişim kutusu eklendi.  

Şu anda yalnızca bir seçeneğiniz var:  

* Çabuk notlarda pencere başlığını yakalayın (her yerden)  

Eğer bu seçenek seçili durumda olursa; Bir metin dosyası açık olduğunda Çabuk not ekle penceresini çağırıp yeni not eklersek, Ad alanına ilgili metnin başlığı otomatik olarak eklenecektir.  

# Her yerden hızlı bir not ekleyin<a id="mark12"></a>

Ayrıca Çabuk Notlar modülü, eklenti iletişim kutusunu açmadan herhangi bir yerden Çabuk not ekleme özelliğine sahiptir.  

Girdi Hareketleri iletişim kutusunda, aşağıda bulacağımız tuş kombinasyonunu yapılandırabiliriz:  

NVDA / Tercihler / Girdi Hareketleri / zAraçlar / Tek basışta seçili metinden yeni bir çabuk not ekler. Çift basışta, yeni bir çabuk not ekler.  

Dilediğimiz tuş atamasını tamamladıktan sonra, herhangi bir yerde metin seçip ve tuş kombinasyonuna basmamız yeterli olacaktır.  

İlk olarak notumuzu hangi kategoriye kaydetmek istediğimizi seçmemiz gereken bir pencere açılacak, sadece eklediğimiz kategoriler görünecektir.  

Sekme tuşuna bastığımızda notun ad yazma alanına erişebilir ve tekrar sekme tuşuna bastığımızda ise kopyaladığımız metnin içerik alanında olduğunu görürüz.  

Tamam tuşuna basarak notumuzu kaydedip, ilgili kategori içerisinde görebiliriz.  

Belirlediğimiz kısayol tuşuna iki defa peş peşe basarsak: Eklenti bizden kategori seçmemizi, not adını girmemizi ve ardından da içeriğini belirlememizi ister. Bu şekilde yeni bir not oluşturmuş oluruz.  

# Uygulama Başlatıcı ve Çabuk Notlar için Sanal Menüler<a id="mark13"></a>

Bu menüler, zAraçlar'ı geliştirmek için geldi ve şimdi onu çok daha üretken ve daha hızlı hale getiriyor.  

Uygulama başlatıcısına ve Çabuk notlara atadığımız kısayollarda artık çift basma ile çalışan özellikler var.  

Bu kombinasyona bir kez basarsak grafik arayüz, iki kez basarsak sanal menü görünecektir.  

Bu menüde kategoriler arasında sağ ve sol oklarla, varsa söz konusu kategorideki öğeler arasında yukarı ve aşağı oklarla hareket edebiliyoruz.  

Uygulama başlatıcı menüsü ile Çabuk notlar menüsü arasında bazı farklılıklar var.  

Uygulama başlatıcısının sanal menüsünde oklarla hareket ettiriyoruz ve enter ile seçtiğimiz öğeyi ilgili eylemi gerçekleştirerek yürütüyoruz.  

Eğer bu bir cmd komutu ise, o zaman onu çalıştıracaktır, eğer hızlı bir erişim ise aynı ve grafiksel arayüz gibi.  

Escape ile menüden hiçbir şey yapmadan çıkabiliriz.  

Bu menüde, N harfi hariç dilediğimiz bir harfe basarak hızlıca ilgili kategoriye gidebiliriz.  

Bastığımız harf ile başlayan bir kategori yoksa bir yardım mesajı seslendirilir.  

Menü etkinken, biz menüden çıkana kadar diğer tüm NVDA tuş kombinasyonlarının çalışmayacağını belirtmeliyiz.  

Çabuk Notlar menüsünde boşluk tuşu işe yaramaz ve uygulama başlatıcı ile farklılıkları ise:  

Bir öğenin üstüne geldiğimizde F1'e basarsak notun içeriğini sözlü hale getirir, F2 ile notu panoya kopyalar ve F3 ile notun içeriğini odaklandığımız yazma alanına yapıştırır.  

Bu menüde de klavye tuşları Escape ile çıktıktan sonra aktif olacaktır.  

## Çevirmenler ve ortak çalışanlar:<a id="mark14"></a>

* Fransızca: Remy Ruiz  
* Portekizce: Ângelo Miguel Abrantes  
* İtalyanca: Alessio Lenzi
* Javi Domínguez: Bana menüyü nasıl programlayacağımı öğrettiğin için çok teşekkür ederim. Bunu benim gibi aptallara açıklamak yerine.
* Türkçe: Umut KORKMAZ

# Sürüm Geçmişi:<a id="mark15"></a>
## Sürüm 0.2.3.<a id="mark0.2.3"></a>

Yeni bir Çabuk not ekle veya seçilen metinden Çabuk not ekle'de pencerelerin başlığını yakalama imkanı eklendi.  

Bu seçenek, Çabuk Notlar modülünün menüsündeki seçenekler / Seçenekler bölümünde etkinleştirilebilir.  

Bu andan itibaren kutu işaretlenirse, Yeni bir Çabuk not ekle veya seçilen Metinden Çabuk not ekle Kısayoluna basıldığında aktif pencerenin başlığı ad olarak alınır.  

## Sürüm 0.2.2.<a id="mark0.2.2"></a>

* Hem uygulama başlatıcıda hem de Çabuk Notlar içerisinde kategoriler arasında taşıma özelliği eklendi.  
* Seçili metinden Çabuk not ekle tuşu için çift tıklama eklendi. Şimdi çift tıklama ile sıfırdan yeni bir Çabuk not oluşturmamıza imkan verecek.  
* Fransızca dokümantasyon güncellendi.  
* İtalyanca dil eklendi.  

## Sürüm 0.2.1.<a id="mark0.2.1"></a>

* Bir metin yapıştırmaya çalışırken boş pano ile ilgili sorun düzeltildi.  

## Sürüm 0.2.<a id="mark0.2"></a>

* Birçok dahili hata düzeltildi.  
* Uygulama Başlatıcı modülü stabilize edildi.  
* Yeni bir Çabuk Notlar modülü eklendi.  
* Her iki modül için sanal menüler eklendi.  

## Sürüm 0.1.6.<a id="mark0.1.6"></a>

* Fransızca ve Portekizce dili eklendi (Portekiz / Brezilya).  

## Sürüm 0.1.5.<a id="mark0.1.5"></a>

* Menüler yeniden yapılandırıldı.  

Ekleme yeteneği eklendi:  

* CMD komutu ekle.  
* Klasör erişimi ekle  .
* Windows çalıştır kısayolları ekle.  
* Yüklü uygulama ekle.  
* Seçeneklerdeki Varsayılana sıfırlaUygulama başlatıcısı Menü düğmesine eklendi.  
* Veritabanındaki çeşitli hatalar düzeltildi.  
* Sabit dahili hatalar.  
* Eklenti tercüme edilmek üzere hazırlandı.  

## Sürüm 0.1.<a id="mark0.1"></a>

* Uygulama Başlatıcı modülü eklendi.  
* İlk sürüm.


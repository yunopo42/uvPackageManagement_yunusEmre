# Library App Çalışma Planı

## Mevcut durum

- [x] `AuditModel` oluşturuldu.
- [x] `Publisher` modeli oluşturuldu.
- [x] `Author` modeli oluşturuldu.
- [x] `Category` modeli ve üst kategori ilişkisi oluşturuldu.
- [x] `BookImage` modeli oluşturuldu.
- [x] `Book` modeli ve nesne ilişkileri oluşturuldu.
- [x] Circular import problemi çözüldü.
- [x] Generic `IRepository[T]` interface'i oluşturuldu.
- [x] `get_all`, `get_by_id`, `add`, `update`, `delete` sözleşmeleri tanımlandı.
- [x] SQLite bağlantısı oluşturuldu.
- [x] Foreign key kontrolü etkinleştirildi.
- [x] Veritabanı başlatma fonksiyonu oluşturuldu.
- [x] `publishers` tablosu oluşturuldu.
- [x] `PublisherRepository` concrete sınıfı oluşturuldu.
- [x] `PublisherRepository.add()` tamamlandı ve test edildi.
- [x] SQLite satırını `Publisher` nesnesine çeviren mapper tamamlandı.
- [x] `PublisherRepository.get_by_id()` tamamlandı ve test edildi.
- [x] Bulunamayan ID için `None` sonucu test edildi.
- [x] Eklenen kayıt ham SQL sorgusuyla doğrulandı.

## Sıradaki işler — PublisherRepository

- [x] `get_all()` metodunu yaz ve test et.
- [x] `update()` metodunu yaz.
- [x] Güncellemede `updated_at`, `updated_by` ve `row_version` alanlarını yönet.
- [x] `update()` metodunu test et.
- [x] `delete()` metodunu soft delete olarak yaz.
- [x] Silmede `is_deleted`, `deleted_at`, `updated_at` ve `row_version` alanlarını yönet.
- [x] `delete()` metodunu test et.
- [x] Silinen kaydın `get_by_id()` ve `get_all()` sonuçlarında görünmediğini doğrula.

## Minimum mentor teslimi

- [x] Modeller ve miras yapısı
- [x] Modeller arasında nesne ilişkileri
- [x] Repository interface
- [x] Beş metodu da çalışan en az bir concrete repository
- [x] CRUD akışının uçtan uca testi
- [x] Terminal tabanlı Publisher yönetim menüsü
- [ ] Kod temizliği ve son kontrol

> PublisherRepository'nin kalan üç metodu tamamlandığında minimum repository-pattern
> görevinin büyük bölümü bitmiş olacak.

## Tam kütüphane uygulaması için veritabanı tabloları

- [ ] `authors` tablosu
- [ ] `categories` tablosu ve `parent_id` self foreign key
- [ ] `books` tablosu
- [ ] `book_images` tablosu ve `book_id` foreign key
- [ ] `book_categories` ara tablosu
- [ ] `books.author_id` foreign key
- [ ] `books.publisher_id` foreign key
- [ ] İndeksler ve unique kuralları

## Tam kütüphane uygulaması için repository'ler

- [ ] `AuthorRepository`
- [ ] `CategoryRepository`
- [ ] `BookImageRepository`
- [ ] `BookRepository`
- [ ] Book–Category çoktan çoğa kayıt işlemleri
- [ ] Book–Image bire çok kayıt işlemleri
- [ ] İlişkili modelleri JOIN sorgularıyla okuma
- [ ] Birden fazla SQL işlemi için transaction yönetimi

## Test ve proje temizliği

- [ ] `main.py` içindeki deneme kodlarını küçük test fonksiyonlarına ayır.
- [ ] Test çalıştırmalarında sürekli kayıt birikmesini önle.
- [ ] Duplicate `slug` hatasını kontrollü şekilde yönet.
- [ ] Geçersiz güncelleme ve silme senaryolarını test et.
- [ ] `.gitignore` içine `__pycache__/`, `*.pyc` ve `*.db` ekle.
- [ ] Dosya adını `bookImage.py` yerine `book_image.py` yap.
- [ ] Türkçe terminal karakter kodlamasını düzenle.
- [ ] Son Git kontrolü, commit ve push

## Bir sonraki adım

Minimum mentor teslimi için kod temizliği, `.gitignore`, son kontrol ve commit/push
işlemlerini tamamlamak. Tam uygulamaya devam edilecekse sırada diğer tablolar ve
repository'ler var.

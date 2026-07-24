from models.publisher import Publisher
from models.author import Author
from models.category import Category
from models.bookImage import BookImage
from models.book import Book
from datetime import date

publisher = Publisher(
    name="Can Yayınları",
    slug="can-yayinlari" ,
    created_by="Yunus Emre Atmaz",
    founded_year=2005,
    city="Konya",
    email="canyayinlari@gmail.com",
    phone="+90 212 000 00 00",
    website="https://www.canyayinlari.com",
    logo_url="https://example.com/can-yayinlari.png"
)

print("********Publisher Test********")
print(publisher.name)
print(publisher.slug)
print(publisher.is_active)
print(publisher.id)



author = Author(
    full_name="George Orwell",
    slug="george-orwell",
    created_by="Yunus Emre Atmaz",
    nationality="İngiliz",
    birth_date=date(1903, 6, 25),
    death_date=date(1950, 1, 21),
    biography="İngiliz romancı, gazeteci ve eleştirmen.",
    website=None,
    is_active=True
)

print("\n*********Author Test*********")
print(author.full_name)
print(author.id)
print(author.created_by)
print(author.created_at)
print(author.slug)
print(author.is_active)


books = Category(
    name = "Kitaplar",
    slug= "kitaplar",
    created_by="Yunus Emre Atmaz",
    description= "Tüm kitap kategorileri",
    display_order=1
)
print("\n*********Category Test*********")
print(books.parent)

#bir alt level
novel = Category(
    name = "Roman",
    slug = "roman",
    created_by="Yunus Emre Atmaz",
    parent=books, #ilk create ettiğim kategori
    description="Roman türündeki kitaplar",
    display_order=2
)
print(novel.name)
print(novel.parent.name)

#novelin alt leveli
science_fiction = Category(
    name="Bilim Kurgu",
    slug="bilim-kurgu",
    created_by="Yunus Emre Atmaz",
    parent=novel
)

print(science_fiction.name)
print(science_fiction.parent.name)


image = BookImage(
    url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxpxPxvUTotQgmb-szX871R6z6bBp2JF8NcVKgaY1OcA&s=10",
    created_by="Yunus Emre Atmaz",
    alt_text="1984 Kitap Kapağı",
    is_cover=True,
    sort_order=1
)
print("\n*********Category Test*********")
print(image.url)
print(image.created_by)
print(image.created_at)
print(image.alt_text)
print(image.is_cover)
print(image.sort_order)



book = Book(
    title="1984",
    slug="1984",
    subtitle="Bin Dokuz Yüz Seksen Dört",
    isbn="9789750718533",
    author=author,
    publisher=publisher,
    created_by="Admin",
    categories=[novel, science_fiction],
    publication_year=1949,
    edition=1,
    page_count=352,
    language="Türkçe",
    format="Ciltsiz",
    price=180.0,
    currency="TRY",
    stock=25,
    status="active",
    rating=4.8,
    summary="Totaliter bir geleceği konu alan distopik roman.",
    images=[image]
)



print(book.title)
print(book.author.full_name)
print(book.publisher.name)

for category in book.categories:
    print(category.name)

for image in book.images:
    print(image.url)
    print(image.book.title)


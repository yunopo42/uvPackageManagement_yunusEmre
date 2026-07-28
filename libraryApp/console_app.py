from database.initializer import initialize_database
from models.publisher import Publisher
from repositories.publisher_repository import PublisherRepository


def read_optional_text(label: str) -> str | None:
    value = input(label).strip()
    return value if value else None


def print_publisher(publisher: Publisher) -> None:
    print("-" * 50)
    print("ID:", publisher.id)
    print("Ad:", publisher.name)
    print("Slug:", publisher.slug)
    print("Kurulus yili:", publisher.founded_year)
    print("Sehir:", publisher.city)
    print("Ulke:", publisher.country)
    print("E-posta:", publisher.email)
    print("Aktif mi:", publisher.is_active)
    print("Row version:", publisher.row_version)


def list_publishers(repository: PublisherRepository) -> None:
    publishers = repository.get_all()

    if not publishers:
        print("\nKayitli aktif Publisher bulunamadi.")
        return

    print(f"\nToplam aktif Publisher: {len(publishers)}")

    for publisher in publishers:
        print_publisher(publisher)


def get_publisher(repository: PublisherRepository) -> None:
    entity_id = input("Publisher ID: ").strip()
    publisher = repository.get_by_id(entity_id)

    if publisher is None:
        print("Publisher bulunamadi.")
        return

    print_publisher(publisher)


def add_publisher(repository: PublisherRepository) -> None:
    print("\nBos birakilamayan alanlar: ad, slug, olusturan")

    name = input("Ad: ").strip()
    slug = input("Slug: ").strip()
    created_by = input("Olusturan: ").strip()

    if not name or not slug or not created_by:
        print("Ad, slug ve olusturan alanlari zorunludur.")
        return

    founded_year_text = input("Kurulus yili: ").strip()

    try:
        founded_year = (
            int(founded_year_text)
            if founded_year_text
            else None
        )
    except ValueError:
        print("Kurulus yili sayi olmalidir.")
        return

    publisher = Publisher(
        name=name,
        slug=slug,
        created_by=created_by,
        founded_year=founded_year,
        city=read_optional_text("Sehir: "),
        country=read_optional_text("Ulke: "),
        address=read_optional_text("Adres: "),
        email=read_optional_text("E-posta: "),
        phone=read_optional_text("Telefon: "),
        website=read_optional_text("Web sitesi: "),
        logo_url=read_optional_text("Logo URL: ")
    )

    try:
        added_publisher = repository.add(publisher)
    except Exception as error:
        print("Publisher eklenemedi:", error)
        return

    print("\nPublisher eklendi.")
    print_publisher(added_publisher)


def update_publisher(repository: PublisherRepository) -> None:
    entity_id = input("Guncellenecek Publisher ID: ").strip()
    publisher = repository.get_by_id(entity_id)

    if publisher is None:
        print("Publisher bulunamadi.")
        return

    print("Degistirmek istemedigin alanlari bos birak.")

    name = input(f"Ad [{publisher.name}]: ").strip()
    slug = input(f"Slug [{publisher.slug}]: ").strip()
    city = input(f"Sehir [{publisher.city or ''}]: ").strip()
    country = input(f"Ulke [{publisher.country or ''}]: ").strip()
    updated_by = input("Guncelleyen: ").strip()

    if not updated_by:
        print("Guncelleyen alani zorunludur.")
        return

    if name:
        publisher.name = name

    if slug:
        publisher.slug = slug

    if city:
        publisher.city = city

    if country:
        publisher.country = country

    publisher.updated_by = updated_by

    try:
        updated_publisher = repository.update(publisher)
    except Exception as error:
        print("Publisher guncellenemedi:", error)
        return

    print("\nPublisher guncellendi.")
    print_publisher(updated_publisher)


def delete_publisher(repository: PublisherRepository) -> None:
    entity_id = input("Silinecek Publisher ID: ").strip()
    publisher = repository.get_by_id(entity_id)

    if publisher is None:
        print("Publisher bulunamadi.")
        return

    print_publisher(publisher)
    confirmation = input(
        "Bu kaydi soft delete yapmak istiyor musun? (e/h): "
    ).strip().lower()

    if confirmation != "e":
        print("Silme islemi iptal edildi.")
        return

    deleted = repository.delete(entity_id)

    if deleted:
        print("Publisher soft delete ile silindi.")
    else:
        print("Publisher silinemedi.")


def print_menu() -> None:
    print(
        """

Publisher Yonetim Menusu
1 - Publisher listele
2 - ID ile Publisher getir
3 - Publisher ekle
4 - Publisher guncelle
5 - Publisher sil (soft delete)
0 - Cikis
"""
    )


def main() -> None:
    initialize_database()
    repository = PublisherRepository()

    actions = {
        "1": list_publishers,
        "2": get_publisher,
        "3": add_publisher,
        "4": update_publisher,
        "5": delete_publisher
    }

    while True:
        print_menu()
        selection = input("Secimin: ").strip()

        if selection == "0":
            print("Program kapatildi.")
            break

        action = actions.get(selection)

        if action is None:
            print("Gecersiz secim.")
            continue

        action(repository)


if __name__ == "__main__":
    main()

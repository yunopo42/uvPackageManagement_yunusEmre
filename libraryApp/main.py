from uuid import uuid4

from database.connections import get_connection
from database.initializer import initialize_database
from models.publisher import Publisher
from repositories.publisher_repository import PublisherRepository


def create_test_publisher() -> Publisher:
    test_suffix = uuid4().hex[:8]

    return Publisher(
        name="Iletisim Yayinlari",
        slug=f"iletisim-yayinlari-{test_suffix}",
        created_by="Yunus Emre Atmaz",
        founded_year=1982,
        city="Istanbul",
        country="Turkiye",
        is_active=True
    )


def verify_with_raw_sql(publisher_id: str) -> None:
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                name,
                slug,
                city,
                updated_by,
                updated_at,
                row_version,
                is_deleted,
                deleted_at,
                is_active
            FROM publishers
            WHERE id = ?
            """,
            (publisher_id,)
        ).fetchone()
    finally:
        connection.close()

    print("\n--- Ham SQL dogrulamasi ---")

    if row is None:
        print("Kayit bulunamadi.")
        return

    print("ID:", row["id"])
    print("Ad:", row["name"])
    print("Slug:", row["slug"])
    print("Sehir:", row["city"])
    print("Guncelleyen:", row["updated_by"])
    print("Guncellenme zamani:", row["updated_at"])
    print("Row version:", row["row_version"])
    print("Silinmis mi:", bool(row["is_deleted"]))
    print("Silinme zamani:", row["deleted_at"])
    print("Aktif mi:", bool(row["is_active"]))


def main() -> None:
    initialize_database()
    print("Veritabani hazir.")

    repository = PublisherRepository()

    # CREATE
    publisher = create_test_publisher()
    added_publisher = repository.add(publisher)

    print("\n--- add() testi ---")
    print("ID:", added_publisher.id)
    print("Ad:", added_publisher.name)

    # READ ONE
    found_publisher = repository.get_by_id(added_publisher.id)

    print("\n--- get_by_id() testi ---")

    if found_publisher is None:
        raise RuntimeError("Eklenen Publisher geri okunamadi.")

    print("ID:", found_publisher.id)
    print("Ad:", found_publisher.name)
    print("Slug:", found_publisher.slug)

    missing_publisher = repository.get_by_id("olmayan-id")
    print("Olmayan kayit sonucu:", missing_publisher)

    # READ ALL
    all_publishers = repository.get_all()

    print("\n--- get_all() testi ---")
    print("Aktif Publisher sayisi:", len(all_publishers))

    for current_publisher in all_publishers:
        print(
            current_publisher.id,
            current_publisher.name,
            current_publisher.row_version
        )

    # UPDATE
    old_version = found_publisher.row_version
    found_publisher.name = "Iletisim Yayinlari Guncel"
    found_publisher.city = "Ankara"
    found_publisher.updated_by = "Yunus Emre Atmaz"

    updated_publisher = repository.update(found_publisher)

    print("\n--- update() testi ---")
    print("Ad:", updated_publisher.name)
    print("Sehir:", updated_publisher.city)
    print("Guncelleyen:", updated_publisher.updated_by)
    print("Eski version:", old_version)
    print("Yeni version:", updated_publisher.row_version)
    print("Guncellenme zamani:", updated_publisher.updated_at)

    # UPDATE SONRASI TEKRAR OKUMA
    publisher_after_update = repository.get_by_id(
        updated_publisher.id
    )

    print("\n--- update sonrasi get_by_id() testi ---")

    if publisher_after_update is None:
        raise RuntimeError("Guncellenen Publisher geri okunamadi.")

    print("DB adi:", publisher_after_update.name)
    print("DB sehri:", publisher_after_update.city)
    print("DB version:", publisher_after_update.row_version)

    verify_with_raw_sql(updated_publisher.id)

    # SOFT DELETE
    count_before_delete = len(repository.get_all())
    delete_result = repository.delete(updated_publisher.id)
    count_after_delete = len(repository.get_all())
    publisher_after_delete = repository.get_by_id(
        updated_publisher.id
    )
    second_delete_result = repository.delete(
        updated_publisher.id
    )

    print("\n--- delete() testi ---")
    print("Silme sonucu:", delete_result)
    print("Silmeden once aktif kayit:", count_before_delete)
    print("Silmeden sonra aktif kayit:", count_after_delete)
    print("get_by_id sonucu:", publisher_after_delete)
    print("Ikinci silme sonucu:", second_delete_result)

    verify_with_raw_sql(updated_publisher.id)


if __name__ == "__main__":
    main()

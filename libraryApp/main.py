import sqlite3
from uuid import uuid4

from database.connections import get_connection
from database.initializer import initialize_database
from database.unit_of_work import UnitOfWork
from models.publisher import Publisher


def create_test_publisher(slug_suffix: str | None = None) -> Publisher:
    test_suffix = slug_suffix or uuid4().hex[:8]

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
    # Kasten UnitOfWork disinda, ayri bir connection aciyoruz.
    # Boylece commit'in gercekten diske indigini disaridan dogrulamis oluyoruz.
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


def count_publishers_by_slug(slug: str) -> int:
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM publishers WHERE slug = ?",
            (slug,)
        ).fetchone()
    finally:
        connection.close()

    return row["total"]


def test_rollback() -> None:
    # UnitOfWork'un asil isini kanitlayan test:
    # ayni transaction icinde once basarili bir insert, sonra
    # UNIQUE slug kisiti yuzunden patlayan bir insert yapiyoruz.
    # Beklenti: ILK kayit da DB'ye yazilmamis olmali.
    print("\n--- rollback testi ---")

    first_slug = f"rollback-testi-{uuid4().hex[:8]}"
    second_slug = f"rollback-testi-{uuid4().hex[:8]}"

    try:
        with UnitOfWork() as uow:
            uow.publishers.add(create_test_publisher(first_slug))
            uow.publishers.add(create_test_publisher(second_slug))

            # Ayni slug ile ucuncu kayit -> UNIQUE kisiti patlar.
            uow.publishers.add(create_test_publisher(first_slug))

            uow.commit()  # Buraya hic gelinmiyor.
    except sqlite3.IntegrityError as error:
        print("Beklenen hata alindi:", error)

    print(
        "Birinci kayit DB'de mi:",
        count_publishers_by_slug(first_slug) > 0
    )
    print(
        "Ikinci kayit DB'de mi:",
        count_publishers_by_slug(second_slug) > 0
    )


def test_commit_unutulursa() -> None:
    # commit() cagrilmazsa hicbir sey kaydedilmemeli.
    print("\n--- commit unutulursa testi ---")

    slug = f"commitsiz-{uuid4().hex[:8]}"

    with UnitOfWork() as uow:
        uow.publishers.add(create_test_publisher(slug))
        # commit yok

    print(
        "Kayit DB'de mi:",
        count_publishers_by_slug(slug) > 0
    )


def main() -> None:
    initialize_database()
    print("Veritabani hazir.")

    # CREATE
    with UnitOfWork() as uow:
        publisher = create_test_publisher()
        added_publisher = uow.publishers.add(publisher)
        uow.commit()

    print("\n--- add() testi ---")
    print("ID:", added_publisher.id)
    print("Ad:", added_publisher.name)

    # READ ONE + READ ALL (salt okuma, commit gerekmez)
    with UnitOfWork() as uow:
        found_publisher = uow.publishers.get_by_id(added_publisher.id)
        missing_publisher = uow.publishers.get_by_id("olmayan-id")
        all_publishers = uow.publishers.get_all()

    print("\n--- get_by_id() testi ---")

    if found_publisher is None:
        raise RuntimeError("Eklenen Publisher geri okunamadi.")

    print("ID:", found_publisher.id)
    print("Ad:", found_publisher.name)
    print("Slug:", found_publisher.slug)
    print("Olmayan kayit sonucu:", missing_publisher)

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

    with UnitOfWork() as uow:
        updated_publisher = uow.publishers.update(found_publisher)
        uow.commit()

    print("\n--- update() testi ---")
    print("Ad:", updated_publisher.name)
    print("Sehir:", updated_publisher.city)
    print("Guncelleyen:", updated_publisher.updated_by)
    print("Eski version:", old_version)
    print("Yeni version:", updated_publisher.row_version)
    print("Guncellenme zamani:", updated_publisher.updated_at)

    # UPDATE SONRASI TEKRAR OKUMA
    with UnitOfWork() as uow:
        publisher_after_update = uow.publishers.get_by_id(
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
    with UnitOfWork() as uow:
        count_before_delete = len(uow.publishers.get_all())
        delete_result = uow.publishers.delete(updated_publisher.id)
        uow.commit()

        count_after_delete = len(uow.publishers.get_all())
        publisher_after_delete = uow.publishers.get_by_id(
            updated_publisher.id
        )
        second_delete_result = uow.publishers.delete(
            updated_publisher.id
        )
        uow.commit()

    print("\n--- delete() testi ---")
    print("Silme sonucu:", delete_result)
    print("Silmeden once aktif kayit:", count_before_delete)
    print("Silmeden sonra aktif kayit:", count_after_delete)
    print("get_by_id sonucu:", publisher_after_delete)
    print("Ikinci silme sonucu:", second_delete_result)

    verify_with_raw_sql(updated_publisher.id)

    # UNIT OF WORK TESTLERI
    test_rollback()
    test_commit_unutulursa()


if __name__ == "__main__":
    main()

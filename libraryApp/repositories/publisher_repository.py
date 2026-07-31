from models.publisher import Publisher
from repositories.repository import IRepository
import sqlite3
from datetime import datetime , timezone

class PublisherRepository(IRepository[Publisher]):
    # Bağlantı IRepository.__init__ üzerinden Unit of Work tarafından verilir.

    def get_all(self) -> list[Publisher]:
        sql = """
        SELECT *
        FROM publishers
        WHERE is_deleted = 0
        ORDER BY created_at DESC
        """

        rows = self._connection.execute(sql).fetchall()

        publishers = []

        for row in rows:
            publisher = self._row_to_publisher(row)
            publishers.append(publisher)

        return publishers

    def get_by_id(self, entity_id: str) -> Publisher | None:
        sql = """
            SELECT *
            FROM publishers
            WHERE id = ?
            AND is_deleted = 0
        """

        row = self._connection.execute(
            sql,
            (entity_id,)
        ).fetchone()

        if row is None:
            return None

        return self._row_to_publisher(row)

    def add(self, entity: Publisher) -> Publisher:
        sql = """
            INSERT INTO publishers (
                id,
                created_at,
                created_by,
                updated_at,
                updated_by,
                is_deleted,
                deleted_at,
                row_version,
                name,
                slug,
                founded_year,
                city,
                country,
                address,
                email,
                phone,
                website,
                logo_url,
                is_active
            )
            VALUES (
                :id,
                :created_at,
                :created_by,
                :updated_at,
                :updated_by,
                :is_deleted,
                :deleted_at,
                :row_version,
                :name,
                :slug,
                :founded_year,
                :city,
                :country,
                :address,
                :email,
                :phone,
                :website,
                :logo_url,
                :is_active
            )
        """
        parameters = {
            "id": entity.id,
            "created_at": entity.created_at.isoformat(),
            "created_by": entity.created_by,
            "updated_at": (
                entity.updated_at.isoformat()
                if entity.updated_at is not None
                else None
            ),
            "updated_by": entity.updated_by,
            "is_deleted": int(entity.is_deleted),
            "deleted_at": (
                entity.deleted_at.isoformat()
                if entity.deleted_at is not None
                else None
            ),
            "row_version": entity.row_version,
            "name": entity.name,
            "slug": entity.slug,
            "founded_year": entity.founded_year,
            "city": entity.city,
            "country": entity.country,
            "address": entity.address,
            "email": entity.email,
            "phone": entity.phone,
            "website": entity.website,
            "logo_url": entity.logo_url,
            "is_active": int(entity.is_active)
        }

        self._connection.execute(sql, parameters)

        return entity

    def update(self, entity : Publisher) -> Publisher:
        if entity.updated_by is None:
            raise ValueError(
                "Güncelleme yapan kullanıcı belirtilmelidir."
            )

        updated_at = datetime.now(timezone.utc)

        sql = """
            UPDATE publishers
            SET
                name = :name,
                slug = :slug,
                founded_year = :founded_year,
                city = :city,
                country = :country,
                address = :address,
                email = :email,
                phone = :phone,
                website = :website,
                logo_url = :logo_url,
                is_active = :is_active,
                updated_at = :updated_at,
                updated_by = :updated_by,
                row_version = row_version + 1
            WHERE id = :id
            AND row_version = :row_version
            AND is_deleted = 0
        """

        parameters = {
            "id": entity.id,
            "name": entity.name,
            "slug": entity.slug,
            "founded_year": entity.founded_year,
            "city": entity.city,
            "country": entity.country,
            "address": entity.address,
            "email": entity.email,
            "phone": entity.phone,
            "website": entity.website,
            "logo_url": entity.logo_url,
            "is_active": int(entity.is_active),
            "updated_at": updated_at.isoformat(),
            "updated_by": entity.updated_by,
            "row_version": entity.row_version
        }

        cursor = self._connection.execute(sql, parameters)

        if cursor.rowcount == 0:
            # Rollback'i burada yapmıyoruz; hatayı fırlatmak repository'nin,
            # transaction'ı geri sarmak Unit of Work'un işi.
            raise ValueError(
                "Publisher bulunamadı, silinmiş veya "
                "başka bir işlem tarafından güncellenmiş."
            )

        # DİKKAT: Bu iki satır artık commit'ten ÖNCE çalışıyor.
        # Aynı transaction içindeki ikinci bir update için doğru davranış,
        # ama rollback olursa bellekteki nesne DB ile uyumsuz kalır.
        entity.updated_at = updated_at
        entity.row_version += 1

        return entity

    def delete(self, entity_id: str) -> bool:
        deleted_at = datetime.now(timezone.utc)

        sql = """
            UPDATE publishers
            SET
                is_deleted = 1,
                deleted_at = :deleted_at,
                updated_at = :updated_at,
                row_version = row_version + 1
            WHERE id = :id
              AND is_deleted = 0
        """

        parameters = {
            "id": entity_id,
            "deleted_at": deleted_at.isoformat(),
            "updated_at": deleted_at.isoformat()
        }

        cursor = self._connection.execute(sql, parameters)

        return cursor.rowcount == 1

    @staticmethod
    def _row_to_publisher(row: sqlite3.Row) -> Publisher:
        return Publisher(
            id=row["id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            created_by=row["created_by"],
            updated_at=(
                datetime.fromisoformat(row["updated_at"])
                if row["updated_at"] is not None
                else None
            ),
            updated_by=row["updated_by"],
            is_deleted=bool(row["is_deleted"]),
            deleted_at=(
                datetime.fromisoformat(row["deleted_at"])
                if row["deleted_at"] is not None
                else None
            ),
            row_version=row["row_version"],
            name=row["name"],
            slug=row["slug"],
            founded_year=row["founded_year"],
            city=row["city"],
            country=row["country"],
            address=row["address"],
            email=row["email"],
            phone=row["phone"],
            website=row["website"],
            logo_url=row["logo_url"],
            is_active=bool(row["is_active"])
        )

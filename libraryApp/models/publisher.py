from models.audit import AuditModel
from datetime import datetime

class Publisher(AuditModel):
    def __init__(
            self,
            name : str,
            slug : str,
            created_by : str,
            founded_year : int | None = None,
            city :str | None = None,
            country : str | None = None,
            address : str | None = None,
            email : str | None = None,
            phone : str | None = None,
            website : str | None = None,
            logo_url : str | None = None,
            is_active : bool = True,
            id: str | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            updated_by: str | None = None,
            is_deleted: bool = False,
            deleted_at: datetime | None = None,
            row_version: int = 1):

        super().__init__(
            created_by=created_by,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            updated_by=updated_by,
            is_deleted=is_deleted,
            deleted_at=deleted_at,
            row_version=row_version) #inheritance ettik
        self.name = name
        self.slug = slug
        self.founded_year = founded_year
        self.city = city
        self.country = country
        self.address = address
        self.email = email
        self.phone = phone
        self.website = website
        self.logo_url = logo_url
        self.is_active = is_active
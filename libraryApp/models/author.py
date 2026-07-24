from models.audit import AuditModel
from datetime import date

class Author(AuditModel):
    def __init__(
            self,
            full_name : str,
            slug : str,
            created_by : str,   #inheritance edilen parametre
            nationality : str | None = None,
            birth_date : date | None = None,  #str yerine date kullandım hazır date modülü var
            death_date : date | None = None,  
            biography : str | None = None,
            photo_url : str | None = None,
            website : str | None = None,
            is_active : bool =True
            ):
        super().__init__(created_by=created_by)
        self.full_name = full_name
        self.slug = slug
        self.nationality = nationality
        self.birth_date = birth_date
        self.death_date = death_date
        self.biography = biography
        self.photo_url = photo_url
        self.website = website
        self.is_active = is_active

from models.audit import AuditModel

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
            is_active : bool = True):

        super().__init__(created_by=created_by) #inheritance ettik
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
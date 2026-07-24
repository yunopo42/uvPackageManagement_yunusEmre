from __future__ import annotations
from models.audit import AuditModel

class Category(AuditModel):
    def __init__(
            self,
            name : str,
            slug : str,
            created_by :str,
            parent : Category | None = None,
            description : str | None = None,
            display_order : int = 0,
            is_active : bool = True
    ):
        super().__init__(created_by=created_by)
        self.name = name
        self.slug = slug
        self.parent = parent
        self.description = description
        self.display_order = display_order
        self.is_active = is_active
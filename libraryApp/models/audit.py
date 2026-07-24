from datetime import datetime, timezone
from uuid import uuid4 #id atama işlemleri için      

class AuditModel:
    def __init__(
            self,
            created_by : str,
            id : str | None = None,
            created_at : datetime | None = None,
            updated_at : str | None = None,
            updated_by : str | None = None,
            is_deleted : bool =False,
            deleted_at : str | None = None,
            row_version : int = 1):
        self.id = id  if id is not None else str(uuid4())
        self.created_at = created_at if created_at is not None else datetime.now(timezone.utc)
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.is_deleted = is_deleted
        self.deleted_at = deleted_at
        self.row_version = row_version


# first_model = AuditModel(created_by='Yunus Emre Atmaz')

# print(first_model.id)
# print(first_model.created_at)
# print(first_model.created_by)
# print(first_model.is_deleted)
# print(first_model.row_version)

# second_model = AuditModel(created_by='ahmet Atmaz')

# print(second_model.id == first_model.id)

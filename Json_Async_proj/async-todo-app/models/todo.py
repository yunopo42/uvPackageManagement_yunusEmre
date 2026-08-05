from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class Todo:
    user_id : int
    title : str
    completed : bool
    id : int | None = None

    @classmethod
    def from_dict(cls , data: dict[str, Any]) -> "Todo": #API'den gelen dict'i Todo'ya transform edecek
        return cls(
            id = data.get("id"),
            user_id = data.get("userId"),
            title = data.get("title"),
            completed = data.get("completed")
        )
    def to_dict(self) -> dict[str, Any]: #Todo'yu API'ye göndermek üzeredict'e transform eder
        return{
            "userId" : self.user_id,
            "title" : self.title,
            "completed" : self.completed
        }

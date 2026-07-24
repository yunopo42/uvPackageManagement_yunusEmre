from __future__ import annotations

from typing import TYPE_CHECKING

from models.audit import AuditModel

if TYPE_CHECKING:
    from models.book import Book

    
class BookImage(AuditModel):
    def __init__(
        self,
        url : str,
        created_by : str, 
        book : Book | None = None,
        alt_text : str | None = None,
        is_cover : bool = False,
        sort_order : int = 0
        ):

        super().__init__(created_by=created_by)
        self.book = book
        self.url = url
        self.alt_text = alt_text
        self.is_cover = is_cover
        self.sort_order = sort_order
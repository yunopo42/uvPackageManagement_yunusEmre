from __future__ import annotations

import sqlite3
from types import TracebackType

from database.connections import get_connection
from repositories.publisher_repository import PublisherRepository


class UnitOfWork:
    def __init__(self) -> None:
        self._connection: sqlite3.Connection | None = None
        self.publishers: PublisherRepository | None = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError(
            )

        return self._connection

    def __enter__(self) -> UnitOfWork:
        self._connection = get_connection()

        # Yeni repository'ler eklendikce buraya ayni connection ile eklenecek.
        self.publishers = PublisherRepository(self._connection)

        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool:
        try:
            # Kosulsuz rollback: commit edilmisse etkisi yok,
            # edilmemisse yarim kalan is geri sarilir.
            # Boylece unutulan bir commit sessizce veri kaybettirmez.
            self.connection.rollback()
        finally:
            self.connection.close()
            self._connection = None
            self.publishers = None

        # False donuyoruz ki olusan istisna yutulmayip yukari yayilsin.
        return False

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

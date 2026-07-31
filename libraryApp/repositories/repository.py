import sqlite3
from abc import ABC , abstractmethod  #---> ABC: Sınıfın soyut sınıf olmasını sağlar.  abstractmethod: Alt sınıfın ilgili metodu yazmasını zorunlu kılar.
from typing import Generic , TypeVar  #---> TypeVar: Repository’nin çalışacağı model tipini temsil eder. Generic: Aynı repository interface’ini farklı model tiplerinde kullanmamızı sağlar.

T = TypeVar("T")

class IRepository(ABC , Generic[T]):
    # Bağlantı dışarıdan (Unit of Work tarafından) verilir.
    # Repository bağlantıyı ne açar ne kapatır, commit/rollback kararı da vermez.
    def __init__(self , connection : sqlite3.Connection) -> None:
        self._connection = connection

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self , entity_id : str) -> T | None:
        pass

    @abstractmethod
    def add(self , entity : T) -> T:
        pass

    @abstractmethod
    def update(self , entity : T) -> T:
        pass

    @abstractmethod
    def delete(self , entity_id : str) -> bool:
        pass

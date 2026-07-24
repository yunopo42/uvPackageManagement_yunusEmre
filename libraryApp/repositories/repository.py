from abc import ABC , abstractmethod  #---> ABC: Sınıfın soyut sınıf olmasını sağlar.  abstractmethod: Alt sınıfın ilgili metodu yazmasını zorunlu kılar.
from typing import Generic , TypeVar  #---> TypeVar: Repository’nin çalışacağı model tipini temsil eder. Generic: Aynı repository interface’ini farklı model tiplerinde kullanmamızı sağlar.

T = TypeVar("T")

class IRepository(ABC , Generic[T]):
    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self , entity_id : str) -> T | None:
        pass

    @abstractmethod
    def add(self , entity : T):
        pass

    @abstractmethod
    def update(self , entity : T) -> T:
        pass
    
    @abstractmethod
    def delete(self , entity_id : str) -> bool:
        pass


    


from abc import ABC , abstractmethod
from models import Todo

class TodoRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Todo]:  #tüm todoları getirecek
        pass 

    @abstractmethod
    async def get_todo(self , todo_id :int): #belirtilen ID'ye sahip todo
        pass

    @abstractmethod
    async def create_todo(self , todo : Todo) -> Todo: #yeni todo oluşturacak
        pass
    @abstractmethod
    async def update(self , todo_id : int , todo : Todo) -> Todo: #todo kaydını güncelleyecek
        pass

    @abstractmethod
    async def delete(self , todo_id : int) -> bool: #todo kayıt silme
        pass
#task 5 import
import httpx

from models import Todo
from repositories.todo_repository import TodoRepository

class JsonPlaceholderTodoRepository(TodoRepository):  #TodoRepository'den abstract ediyor
    def __init__(self , client : httpx.AsyncClient):
        self.client = client

    async def get_all(self) -> list[Todo]:
        response = await self.client.get("/todos")
        response.raise_for_status()

        todo_list = response.json()
        return [Todo.from_dict(todo_data) for todo_data in todo_list]

    async def get_todo(self, todo_id):
        response = await self.client.get(f"/todos/{todo_id}")
        response.raise_for_status()

        todo_data = response.json()
        return Todo.from_dict(todo_data)
#task-6
    async def create_todo(self, todo: Todo):
        response = await self.client.post("/todos", json=todo.to_dict())
        response.raise_for_status()
        created_todo_data = response.json()
        return Todo.from_dict(created_todo_data)
    
    async def update(self , todo_id : int , todo : Todo):
        update_data = todo.to_dict()
        update_data["id"] = todo_id
        response = await self.client.put(f"/todos/{todo_id}", json = update_data)
        response.raise_for_status()
        updated_todo_data = response.json()
        return Todo.from_dict(updated_todo_data)
    
    async def delete(self , todo_id : int):
        response = await self.client.delete(f"/todos/{todo_id}")
        response.raise_for_status()
        return True
    


        
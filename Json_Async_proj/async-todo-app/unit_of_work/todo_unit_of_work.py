import httpx
from repositories import JsonPlaceholderTodoRepository 
#task 7
class TodoUnitOfWork:
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com") -> None:
        self.base_url = base_url


    async def __aenter__(self) -> "TodoUnitOfWork":
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0
        )
        self.todos = JsonPlaceholderTodoRepository(client = self.client)
        return self

    async def __aexit__(self, exc_type, exc_val, traceback) -> None:
        await self.client.aclose()


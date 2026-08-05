import httpx
#task 3 import
from models import Todo
#task 4-5 import
from repositories import JsonPlaceholderTodoRepository
#task 5 import
import asyncio
#task 6 import
from models import Todo
#task 7 import
from unit_of_work import TodoUnitOfWork

#task-8 terminal CLI
def menu_yazdir():
    print("\n"+ "="*45)
    print("    Async Todo Uygulaması")
    print("="*45)
    print("1. Tüm Todo'ları Listele")
    print("2. Todo Detayını Görüntüle")
    print("3. Yeni Todo Oluştur")
    print("4. Todo Güncelle")
    print("5. Todo Sil")
    print("0. Çıkış")
    print("="*45)

def sayi_al(mesaj: str):
    while True:
        veri = input(mesaj).strip()
        try:
            sayi = int(veri)
            if sayi <=0:
                print("Lütfen pozitif bir sayı girin.")
                continue
            return sayi
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
def tamamlanma_durumu_al():
    while True:
        cevap = input("Todo tamamlandı mı? (y/n):").strip().lower()
        if cevap in ["y" , "evet" , "yes"]:
            return True
        elif cevap in ["n" , "hayır" , "no"]:
            return False
        print("Lütfen 'y' veya 'n' ile cevap verin.")
def todo_yazdir(todo: Todo):
    durum = "Tamamlandı ✅" if todo.completed else "Tamamlanmadı ❌"
    print("-"*45)
    print(f"ID              :{todo.id}")
    print(f"Kullanıcı ID    :{todo.user_id}")
    print(f"Başlık          :{todo.title}")
    print(f"Durum           :{durum}")
    print("-"*45)

async def todolari_listele(repository):
    print("\nTodo kayıtları getiriliyor...\n")
    todos = await repository.get_all()
    print(f"Toplam {len(todos)} Todo kaydı bulundu.\n")
    print("İlk 5 Todo kaydı :\n")
    for todo in todos[:5]:
        todo_yazdir(todo)

async def todo_getir(repository):
    todo_id = sayi_al("Getirilecek Todo ID : ")
    todo = await repository.get_todo(todo_id)
    print("\nTodo kaydı getiriliyor...\n")
    todo_yazdir(todo)

async def todo_ekle(repository):
    print("\nYeni Todo bilgilerini girin: \n")
    user_id = sayi_al("Kullanıcı ID : ")
    title = input("Todo başlığı : ").strip()

    while not title:
        print("Todo başlığı boş bırakılamaz.")
        title = input("Todo başlığı: ").strip()
    completed = tamamlanma_durumu_al()
    new_todo = Todo(user_id=user_id , title=title , completed=completed)
    created_todo = await repository.create_todo(new_todo)
    print("\nYeni Todo kaydı başarıyla oluşturuldu.")
    todo_yazdir(created_todo)

async def todo_guncelle(repository):
    todo_id = sayi_al("Güncellenecek Todo ID : ")
    existing_todo = await repository.get_todo(todo_id)
    if not existing_todo:
        print("Todo kaydı bulunamadı.")
        return
    print("\nMevcut Todo bilgileri :\n")
    todo_yazdir(existing_todo)
    print("\nYeni bilgileri girin (boş bırakılırsa mevcut değer korunur):\n")
    user_id = sayi_al("Yeni kullanıcı ID : ")
    title = input("Yeni Todo başlığı : ").strip()
    while not title:
        print("Todo başlığı boş bırakılamaz.")
        title = input("Yeni Todo başlığı: ").strip()
    completed = tamamlanma_durumu_al()

    todo_to_update = Todo(
        id= todo_id,
        user_id=user_id,
        title=title,
        completed=completed
    )
    updated_todo = await repository.update(todo_id=todo_id, todo= todo_to_update)

    print("\nTodo kaydı başarıyla güncellendi.")
    todo_yazdir(updated_todo)

async def todo_sil(repository):
    todo_id = sayi_al("Silinecek Todo ID : ")
    existing_todo = await repository.get_todo(todo_id)
    print("\nSilinecek Todo kaydı :\n")
    todo_yazdir(existing_todo)

    onay = input("Bu Todo silinsin mi? (y/n):").strip().lower()

    if onay not in ["y" , "evet" , "yes"]:
        print("Silme işlemi iptal edildi.")
        return
    deleted = await repository.delete(todo_id)
    if deleted:
        print("\nTodo kaydı başarıyla silindi.")
    else:
        print("\nTodo kaydı silinemedi.")

async def main():
    # r = httpx.get("https://www.youtube.com/watch?v=ID_JjpbZrmU")
    # print(r.status_code)
    # url = "https://jsonplaceholder.typicode.com/todos"
    # request = httpx.get(url)
    # print(request.status_code)

    # ilk_3_post = request.json()[:3]
    # #ayrı ayrı
    # for post in ilk_3_post:
    #     print(post)
    #     print("\n***************\n")
    # print(ilk_3_post)

    #Task-3 Todo class'ını kullanarak API'den gelen dict'i Todo'ya dönüştürmek
    # api_data = {"userId" : 1 , "id" : 6 , "title" : "Python Async await çalışıyor" , "completed" : False} 

    # todo = Todo.from_dict(api_data)
    # print("Todo nesnesi : \n****************\n" , todo)
    # print("\nAPI'ye gönderilecek dict : \n****************\n" , todo.to_dict())
    # #task-4 
    # print("todo repository başarıyla import edildi.")
    # print(TodoRepository)

    # url = "https://jsonplaceholder.typicode.com"
    # try:
    #     async with TodoUnitOfWork() as uow:
    #         # repository = JsonPlaceholderTodoRepository(client)
    #         #get_alls()
    #         print("1-İlk 3 todo kaydı : \n")
    #         todos = await uow.todos.get_all()
    #         for todo in todos[:3]:
    #             print(todo)
    #         print("\n***************\n")   

    #         #get
    #         print("\n2- ID değeri 10 olan Todo: \n")
    #         found_todo = await uow.todos.get_todo(10)
    #         if found_todo:
    #             print(found_todo)

    #         #create
    #         print("\n3-Yeni Todo oluşturma : \n")
    #         new_todo = Todo(user_id=1, title="Python Async CRUD işlemleri tamamlandı", completed=False)
    #         created_todo = await uow.todos.create_todo(new_todo)
    #         print("Eklenen Todo : ")
    #         print(created_todo)

    #         #UPDATE
    #         print("\n4-Todo Güncelleme : \n")
    #         todo_to_update = Todo(id=1 , user_id=1, title="Python Async CRUD tamamlandı" , completed=True)
    #         updated_todo = await uow.todos.update(todo_id=1 , todo=todo_to_update)
    #         print("Güncellenen Todo : ")
    #         print(updated_todo)

    #         #DELETE
    #         print("\n5-Todo Silme : \n")
    #         is_deleted = await uow.todos.delete(todo_id=1)
    #         if is_deleted:
    #             print("Todo silindi.")
            

    #         print("\nID değeri 10 olan Todo:\n")
    #         todo = await uow.todos.get_todo(10)
    #         if todo:
    #             print(todo)

    # except httpx.HTTPStatusError as e:
    #     print("API durum kodu hatasi" , e.response.status_code)
    # except httpx.RequestError as e:
    #     print("API isteği hatasi" , str(e))
    #task-8
    try:
        async with TodoUnitOfWork() as uow:
            repository = uow.todos
            if repository is None:
                raise RuntimeError(
                    "Todo repository oluşturulamadı"
                )
            while True:
                menu_yazdir()
                secim = input("Seçiminiz : ").strip()
                try:
                    if secim == "1":
                        await todolari_listele(repository)
                    elif secim == "2":
                        await todo_getir(repository)
                    elif secim == "3":
                        await todo_ekle(repository)
                    elif secim == "4":
                        await todo_guncelle(repository)
                    elif secim == "5":
                        await todo_sil(repository)
                    elif secim == "0":
                        print("Çıkış yapılıyor....")
                        break
                    else :print("Geçersiz seçim. Tekrar deneyin.(0-5 arası değer girin)")
                except httpx.HTTPStatusError as e :
                    print("\nAPI durum kodu hatası : " , e.response.status_code)
                    print(f"İstek Adresi : {e.request.url}")
                except httpx.RequestError as e:
                    print("\nAPI isteği hatası : " , str(e))
                
    except RuntimeError as e:
                        print("\nAPI bağlantı hatası : " , str(e))

if __name__ == "__main__":
    asyncio.run(main())

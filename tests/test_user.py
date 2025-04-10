from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@example.com'})
    assert response.status_code == 404  # Предполагаем, что API возвращает 404 для несуществующего пользователя
    assert response.json() == {"detail": "User not found"}  # Сообщение о том, что пользователь не найден


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {"email": "newuser@example.com", "name": "New User"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201  # Ожидаем, что создание пользователя возвращает статус 201
    assert isinstance(response.json(), int)  # Проверяем, что возвращается ID (целое число)


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    new_user = {"email": users[0]['email'], "name": "Another User"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409  # Ожидаем ошибку при создании с дублирующимся email
    assert response.json() == {"detail": "User with this email already exists"}  # Сообщение от API


def test_delete_user():
    '''Удаление пользователя'''
    # Для этого теста сначала нужно создать тестового пользователя, либо использовать фикстуру
    user_to_delete = {"email": "user_to_delete@example.com", "name": "User To Delete"}
    response = client.post("/api/v1/user", json=user_to_delete)
    assert response.status_code == 201  # Убедитесь, что пользователь создан

    # Теперь удалим этого пользователя
    response = client.delete("/api/v1/user", params={'email': user_to_delete['email']})
    assert response.status_code == 204  # Ожидаем, что успешное удаление возвращает статус 204 (No Content)

    # Проверим, что пользователь действительно удалён
    response = client.get("/api/v1/user", params={'email': user_to_delete['email']})
    assert response.status_code == 404  # Теперь этот пользователь не должен существовать
    assert response.json() == {"detail": "User not found"}  # Сообщение о том, что пользователь не найден
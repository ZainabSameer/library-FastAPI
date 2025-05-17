from fastapi.testclient import TestClient
from data.book_data import books_list, reviews_list
from data.user_data import user_list

def seed_db(db):
    db.commit()
    db.add_all(user_list)
    db.commit()
    db.add_all(books_list)
    db.commit()
    db.add_all(reviews_list)
    db.commit()

def login(test_app: TestClient, username: str, password: str):
    response = test_app.post("/api/login", json={"username": username, "password": password})

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json().get('detail', 'Unknown error')}")

    token = response.json().get('token')
    if not token:
        raise Exception("No token returned from login endpoint.")

    headers = {"Authorization": f"Bearer {token}"}
    return headers


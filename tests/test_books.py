import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.user import UserModel
from models.book import BookModel
from tests.lib import login
from main import app

def test_get_books(test_app: TestClient, override_get_db):
    response = test_app.get("/api/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) >= 2
    for book in books:
        assert 'id' in book
        assert 'title' in book
        assert 'author' in book
        assert 'in_stock' in book
        assert 'rating' in book
        assert 'publication_year' in book
        assert 'user' in book
        assert 'email' in book['user']
        assert 'username' in book['user']



def test_get_single_book(test_app: TestClient, test_db: Session, override_get_db):
    book = test_db.query(BookModel).first()
    assert book is not None
    response = test_app.get(f"/api/books/{book.id}")
    assert response.status_code == 200
    book = response.json()
    assert isinstance(book, dict)
    assert 'id' in book
    assert 'title' in book
    assert 'author' in book
    assert 'in_stock' in book
    assert 'rating' in book
    assert 'publication_year' in book
    assert 'user' in book
    assert 'email' in book['user']
    assert 'username' in book['user']
    assert 'reviews' in book
    for review in book['reviews']:
        assert 'content' in review
        assert 'id' in review

def test_get_book_not_found(test_app: TestClient, test_db: Session, override_get_db):
    max_book_id = test_db.query(BookModel.id).order_by(BookModel.id.desc()).first()
    if max_book_id is None:
        invalid_book_id = 1
    else:
        invalid_book_id = max_book_id[0] + 1

    response = test_app.get(f"/api/books/{invalid_book_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['detail'] == 'Book not found'

def test_create_book(test_app: TestClient, test_db: Session):

    user = UserModel(username='testUser', email='zozo@kpmg.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)


    headers = login(test_app, 'testUser', 'mys3cretp2ssw0rd')

    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "in_stock": True,
        "rating": 5,
        "publication_year": 2023,
    }

    response = test_app.post("/api/books", headers=headers, json=book_data)

    assert response.status_code == 200
    book_response = response.json()
    assert book_response["title"] == book_data["title"]
    assert book_response["author"] == book_data["author"]
    assert book_response["in_stock"] == book_data["in_stock"]
    assert book_response["rating"] == book_data["rating"]
    assert book_response["publication_year"] == book_data["publication_year"]
    assert "id" in book_response
    assert "user" in book_response
    assert book_response['user']["username"] == 'testUser'


    book_id = book_response["id"]
    book = test_db.query(BookModel).filter(BookModel.id == book_id).first()
    assert book is not None
    assert book.title == book_data["title"]
    assert book.author == book_data["author"]
    assert book.in_stock == book_data["in_stock"]
    assert book.rating == book_data["rating"]
    assert book.publication_year == book_data["publication_year"]

def test_update_book(test_app: TestClient, test_db: Session, override_get_db):
    user = UserModel(username='anotherTestUser321', email='goodbye@example.com')
    user.set_password('passw0rd')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    headers = login(test_app, 'anotherTestUser321', 'passw0rd')

    book = BookModel(
        title="Another Test Book",
        author="Original Author",
        in_stock=True,
        rating=65,
        publication_year=2020,
        user_id=user.id
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)

    updated_data = {
        "title": "Another Updated Book Name",
        "author": "Updated Author",
        "in_stock": not book.in_stock,
        "rating": 55,
        "publication_year": 2024
    }

    response = test_app.put(f"/api/books/{book.id}", headers=headers, json=updated_data)
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book['id'] == book.id
    assert updated_book['title'] == updated_data['title']
    assert updated_book['author'] == updated_data['author']
    assert updated_book['in_stock'] == updated_data['in_stock']
    assert updated_book['rating'] == updated_data['rating']
    assert updated_book['publication_year'] == updated_data['publication_year']

def test_update_book_not_found(test_app: TestClient, test_db: Session, override_get_db):
    user = UserModel(username='someguy', email='someperson@example.com')
    user.set_password('bestpassword')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    headers = login(test_app, 'someguy', 'bestpassword')
    max_book_id = test_db.query(BookModel.id).order_by(BookModel.id.desc()).first()
    if max_book_id is None:
        invalid_book_id = 1
    else:
        invalid_book_id = max_book_id[0] + 1

    updated_data = {
        "title": "Another Updated Book Name",
        "author": "Updated Author",
        "in_stock": True,
        "rating": 56,
        "publication_year": 2025
    }

    response = test_app.put(f"/api/books/{invalid_book_id}", headers=headers, json=updated_data)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Book not found"

def test_unauthorized_update_book(test_app: TestClient, test_db: Session, override_get_db):
    user1 = UserModel(username='user1', email='user1@example.com')
    user1.set_password('password1')
    test_db.add(user1)
    test_db.commit()
    test_db.refresh(user1)

    user2 = UserModel(username='user2', email='user2@example.com')
    user2.set_password('password2')
    test_db.add(user2)
    test_db.commit()
    test_db.refresh(user2)

    book = BookModel(
        title="Private Book",
        author="Owner Author",
        in_stock=True,
        rating=90,
        publication_year=2020,
        user_id=user1.id
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)

    headers = login(test_app, 'user2', 'password2')

    updated_data = {
        "title": "Unauthorized Edit",
        "author": "Intruder",
        "in_stock": False,
        "rating": 10,
        "publication_year": 2024
    }
    response = test_app.put(f"/api/books/{book.id}", headers=headers, json=updated_data)
    assert response.status_code == 403
    response_data = response.json()
    assert response_data["detail"] == "Operation forbidden"

def test_delete_book(test_app: TestClient, test_db: Session, override_get_db):
    user = UserModel(username='deleter', email='remover@example.com')
    user.set_password('del')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    headers = login(test_app, 'deleter', 'del')

    book = BookModel(
        title="Not Long For This World Book",
        author="Ghost Writer",
        in_stock=True,
        rating=6,
        user_id=user.id
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)

    response = test_app.delete(f"/api/books/{book.id}", headers=headers)
    assert response.status_code == 200

    response = test_app.get(f"/api/books/{book.id}", headers=headers)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"].lower() == "book not found"


def test_book_not_found_for_deletion(test_app: TestClient, test_db: Session, override_get_db):
    user = UserModel(username='remover', email='deleter@example.com')
    user.set_password('swingandamiss')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    headers = login(test_app, 'remover', 'swingandamiss')

    max_book_id = test_db.query(BookModel.id).order_by(BookModel.id.desc()).first()
    if max_book_id is None:
        invalid_book_id = 1
    else:
        invalid_book_id = max_book_id[0] + 1

    response = test_app.delete(f"/api/books/{invalid_book_id}", headers=headers)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "not found"


def test_unauthorized_deletion(test_app: TestClient, test_db: Session, override_get_db):
    user_a = UserModel(username='usera', email='usera@example.com')
    user_a.set_password('passworda')
    test_db.add(user_a)
    test_db.commit()
    test_db.refresh(user_a)

    user_b = UserModel(username='userb', email='userb@example.com')
    user_b.set_password('passwordb')
    test_db.add(user_b)
    test_db.commit()
    test_db.refresh(user_b)

    book = BookModel(
        title="What is a Book?",
        author="Author A",
        in_stock=True,
        rating=100,
        user_id=user_a.id
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)


    headers = login(test_app, 'userb', 'passwordb')

    response = test_app.delete(f"/api/books/{book.id}", headers=headers)
    assert response.status_code == 403
    response_data = response.json()


def test_unauthorized_deletion(test_app: TestClient, test_db: Session, override_get_db):
    user_a = UserModel(username='usera', email='usera@example.com')
    user_a.set_password('passworda')
    test_db.add(user_a)
    test_db.commit()
    test_db.refresh(user_a)

    user_b = UserModel(username='userb', email='userb@example.com')
    user_b.set_password('passwordb')
    test_db.add(user_b)
    test_db.commit()
    test_db.refresh(user_b)

    book = BookModel(
        title="What is a Book?",
        author="Author A",
        in_stock=True,
        rating=100,
        user_id=user_a.id
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)

    headers = login(test_app, 'userb', 'passwordb')

    response = test_app.delete(f"/api/books/{book.id}", headers=headers)
    assert response.status_code == 403
    response_data = response.json()
    assert response_data["detail"] == "Operation forbidden"

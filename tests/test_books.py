import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.user import UserModel
from models.book import BookModel
from tests.lib import login
from main import app
from models.user import UserModel



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
def test_create_book(test_app: TestClient, test_db: Session):
    user = UserModel(username='testUser', email='zozo@kpmg.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()
    headers = login(test_app, 'testUser123', 'mys3cretp2ssw0rd')
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "in_stock": True,
        "rating": 5,
        "publication_year": 2023,
    }
    response = test_app.post("/api/books", headers=headers, json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["author"] == book_data["author"]
    assert response.json()["in_stock"] == book_data["in_stock"]
    assert response.json()["rating"] == book_data["rating"]
    assert response.json()["publication_year"] == book_data["publication_year"]
    assert "id" in response.json()  
    assert "user" in response.json()  
    assert response.json()['user']["username"] == 'testUser123'

    book_id = response.json()["id"]
    book = test_db.query(BookModel).filter(BookModel.id == book_id).first()
    assert book is not None
    assert book.title == book_data["title"]
    assert book.author == book_data["author"]
    assert book.in_stock == book_data["in_stock"]
    assert book.rating == book_data["rating"]
    assert book.publication_year == book_data["publication_year"]

def test_update_book(test_app: TestClient, test_db: Session):
    user = UserModel(username='testUser', email='zozo@kpmg.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()
    
    headers = login(test_app, 'testUser', 'mys3cretp2ssw0rd')
    book_data = {
        "title": "Initial Book",
        "author": "Initial Author",
        "in_stock": True,
        "rating": 4,
        "publication_year": 2022,
    }
    response = test_app.post("/api/books", headers=headers, json=book_data)
    book_id = response.json()["id"]

    update_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "in_stock": False,
        "rating": 5,
        "publication_year": 2023,
    }
    response = test_app.put(f"/api/books/{book_id}", headers=headers, json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    assert response.json()["author"] == update_data["author"]
    assert response.json()["in_stock"] == update_data["in_stock"]
    assert response.json()["rating"] == update_data["rating"]
    assert response.json()["publication_year"] == update_data["publication_year"]

def test_delete_book(test_app: TestClient, test_db: Session):
    user = UserModel(username='testUser', email='zozo@kpmg.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()
    
    headers = login(test_app, 'testUser', 'mys3cretp2ssw0rd')
    book_data = {
        "title": "Book to Delete",
        "author": "Author",
        "in_stock": True,
        "rating": 4,
        "publication_year": 2022,
    }
    response = test_app.post("/api/books", headers=headers, json=book_data)
    book_id = response.json()["id"]

    response = test_app.delete(f"/api/books/{book_id}", headers=headers)
    assert response.status_code == 204  

    response = test_app.get(f"/api/books/{book_id}", headers=headers)
    assert response.status_code == 404  
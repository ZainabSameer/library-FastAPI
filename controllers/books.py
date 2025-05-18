from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.book import BookModel
from models.user import UserModel
from serializers.book import BookSchema, BookCreate as BookCreateSchema
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/books", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books

@router.get("/books/{book_id}", response_model=BookSchema)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=BookSchema)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_book = BookModel(**book.model_dump(), user_id=current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="book not found")

    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="not found")

    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(db_book)
    db.commit()
    return {"message": f"Book with ID {book_id} has been deleted"}
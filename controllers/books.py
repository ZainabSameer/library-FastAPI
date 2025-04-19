from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.book import BookModel
#from schemas import BookSchema
from serializers.book import BookSchema
from typing import List

router = APIRouter()

@router.get("/books", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books

@router.get("/books/{book_id}", response_model=BookSchema)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
            # If book with the given ID is not found
        raise HTTPException(status_code=404, detail="Book not found")
    return book



@router.post("/books", response_model=BookSchema)
def create_book(book: BookSchema, db: Session = Depends(get_db)):
    new_book = BookModel(**book.dict()) # Convert Pydantic model to SQLAlchemy model
    db.add(new_book)
    db.commit() # Save to database
    db.refresh(new_book) # Refresh to get the updated data (including auto-generated fields)
    return new_book


# books.py

@router.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check for unique title
    existing_book = db.query(BookModel).filter(BookModel.title == book.title).first()
    if existing_book and existing_book.id != book_id:
        raise HTTPException(status_code=400, detail="Title already exists")

    # Update book fields
    db_book.title = book.title
    db_book.author = book.author
    db_book.rating = book.rating
    db_book.publication_year = book.publication_year

    db.commit()
    return db_book
@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)  # Remove from database
    db.commit()  # Save changes
    return {"message": f"Book with ID {book_id} has been deleted"}

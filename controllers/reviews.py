from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.reviews import ReviewModel
from models.book import BookModel
from serializers.reviews import ReviewsSchema
from typing import List
from database import get_db

router = APIRouter()

@router.get("/books/{book_id}/reviews", response_model=List[ReviewsSchema])
def get_comments_for_tea(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.reviews

@router.get("/reviews/{review_id}", response_model=ReviewsSchema)
def get_comment(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="not found")
    return review

@router.post("/books/{book_id}/reviews", response_model=ReviewsSchema)
def create_comment(book_id: int, review: ReviewsSchema, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="not found")

    new_review = ReviewModel(**review.dict(), book_id=book_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.put("/reviews/{review_id}", response_model=ReviewsSchema)
def update_review(review_id: int, review: ReviewsSchema, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="review not found")

    comment_data = review.dict(exclude_unset=True)
    for key, value in comment_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="review not found")

    db.delete(db_review)
    db.commit()
    return {"message": f"review with ID {review_id} has been deleted"}

from sqlalchemy.orm import Session, sessionmaker
from data.book_data import books_list
from config.environment import db_URI
from sqlalchemy import create_engine
from models.base import Base 

engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)

try:
    print("Recreating database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding the database...")
    db = SessionLocal()


    db.add_all(books_list)
    db.commit()


    print("Database seeding complete! 👋")
except Exception as e:
    print("An error occurred:", e)

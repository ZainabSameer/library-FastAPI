# main.py

from fastapi import FastAPI
from controllers.books import router as BooksRouter  
app = FastAPI()

# Include the teas router with a prefix '/api'
app.include_router(BooksRouter, prefix="/api")


@app.get('/')
def home():
    # Hello world function
    return {'message': 'Hello World!'}

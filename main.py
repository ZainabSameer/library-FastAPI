from fastapi import FastAPI
from controllers.books import router as BooksRouter  
app = FastAPI()

app.include_router(BooksRouter, prefix="/api")


@app.get('/')
def home():
    return {'message': 'Hello World!'}

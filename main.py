from fastapi import FastAPI
from controllers.books import router as BooksRouter  
from controllers.users import router as UsersRouter 
app = FastAPI()

app.include_router(BooksRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")

@app.get('/')
def home():
    return {'message': 'Welcome to Zainab library'}

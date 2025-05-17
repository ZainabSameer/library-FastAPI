from models.book import BookModel 
from models.reviews import ReviewModel

books_list = [
    BookModel(title="Brave New World", author="Aldous Huxley", rating=4, in_stock=True, user_id=1),
    BookModel(title="The Alchemist", author="Paulo Coelho", rating=4, in_stock=True, user_id=2),
    BookModel(title="The Catch-22", author="Joseph Heller", rating=4, in_stock=False, user_id=1),
    BookModel(title="Crime and Punishment", author="Fyodor Dostoevsky", rating=4, in_stock=True, user_id=3),
    BookModel(title="The Picture of Dorian Gray", author="Oscar Wilde", rating=4, in_stock=True, user_id=1),
    BookModel(title="The Odyssey", author="Homer", rating=4, in_stock=True, user_id=2),
    BookModel(title="Wuthering Heights", author="Emily Brontë", rating=4, in_stock=False, user_id=2),
    BookModel(title="The Road", author="Cormac McCarthy", rating=4, in_stock=True, user_id=4),
    BookModel(title="The Grapes of Wrath", author="John Steinbeck", rating=4, in_stock=True, user_id=3)
]


reviews_list = [
    ReviewModel(content="nice book", book_id=1),
    ReviewModel(content="nice book", book_id=2),
    ReviewModel(content="nice book", book_id=3),
    ReviewModel(content="nice book", book_id=4),
    ReviewModel(content="nice book", book_id=5),
    ReviewModel(content="nice book", book_id=6),
    ReviewModel(content="nice book", book_id=7),
    ReviewModel(content="Gripping and heart-wrenching", book_id=8),
    ReviewModel(content="A powerful portrayal of struggle.", book_id=9)
]


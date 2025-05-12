# FastAPI Application
# Zainab Library
# Project Idea
 - The Online Library System is designed to provide users with a convenient platform to browse and manage a collection of books. Users can view details about each book, including its title, author, rating, and availability. Additionally, users can leave reviews for books, enhancing the community aspect of the library.
# Model Description and Entity Relationship Diagram (ERD)
   ###### Book
   Attributes:
   * id (Primary Key): Unique identifier for each book.
   * title: The title of the book.
   * author: The author of the book.
   * rating: Average rating of the book.
   * in_stock: Boolean value indicating whether the book is currently available.
   ###### Relationships: One Book can have multiple Reviews.
   
   ###### Review
   Attributes:
   * id (Primary Key): Unique identifier for each review.
   * book_id (Foreign Key): References the id of the Book it belongs to.
   * user: The name or ID of the user who submitted the review.
   * content: The text of the review.
   ###### Relationships:Each Review is linked to one Book.
   
# Routes/Endpoints
| **Method** | **Endpoint**                       | **Description**                                   | **Request Body**                                       | **Response**                      |
|------------|------------------------------------|---------------------------------------------------|-------------------------------------------------------|-----------------------------------|
| GET        | `/api/books`                       | Retrieve a list of all books                      | N/A                                                   | JSON array of book objects        |
| GET        | `/api/books/{id}`                 | Retrieve details of a specific book by ID        | N/A                                                   | JSON object of the book          |
| POST       | `/api/books`                       | Create a new book (Admin and owner only)                   | JSON object containing `title`, `author`, `rating`, `in_stock` | JSON object of the created book   |
| PUT        | `/api/books/{id}`                 | Update an existing book (Admin and owner only)              | JSON object with updated `title`, `author`, `rating`, or `in_stock` | JSON object of the updated book   |
| DELETE     | `/api/books/{id}`                 | Delete a book by ID (Admin and owner only)                 | N/A                                                   | Confirmation message              |

### Reviews

| **Method** | **Endpoint**                       | **Description**                                   | **Request Body**                                       | **Response**                      |
|------------|------------------------------------|---------------------------------------------------|-------------------------------------------------------|-----------------------------------|
| GET        | `/api/books/{id}/reviews`         | Retrieve all reviews for a specific book         | N/A                                                   | JSON array of review objects      |
| POST       | `/api/books/{id}/reviews`         | Add a new review for a specific book              | JSON object containing `user`and `content` | JSON object of the created review  |
| DELETE     | `/api/reviews/{id}`               | Delete a specific review by ID (Admin and owner only)      | N/A                                                   | Confirmation message              |
# External Resources/APIs you expect to use or reference

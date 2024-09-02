from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id : Optional[int] = Field(description = 'ID is Optional', default = None)
    title : str = Field(min_length=3)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt = 0, lt = 6)

    model_config = {
        "json_schema_extra":{
            "example":{
                "id": "Optional field",
                "title": "A new Book",
                "author":"author name",
                "description": "Description",
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(1, 'Title 1', 'Author1', 'History', 5),
    Book(2, 'Title 2', 'Author2', 'Computer Science', 5),
    Book(3, 'Title 3', 'Author3', 'Math', 5),
    Book(4, 'Title 4', 'Author4', 'Literature', 5),
    Book(5, 'Title 5', 'Author5', 'Geography', 5),
    Book(6, 'Title 6', 'Author6', 'Physics', 5),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not Found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book_to_return =[]
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return

@app.post("/books/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book Added"}

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book.id:
            BOOKS[index] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail= "Book not Found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book_id:
            BOOKS.pop(index)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail= "Book not Found")

def find_book_id(book : Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    """ if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1 """
    return book
    
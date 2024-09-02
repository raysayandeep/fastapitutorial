from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get('/books/mybooks')
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
async def read_books_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get('/books/')
async def read_books_by_category(category: str):
    book_list = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_list.append(book)
    return book_list

@app.get('/books/{author}/')
async def read_books_by_author_category(book_author: str, category: str):
    book_list = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            if book.get('category').casefold() == category.casefold():
                book_list.append(book)
    return book_list     
        
@app.post('/books/create_book/')
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return {'message':'new book added'}

@app.put('/books/update_book/')
async def update_book(updated_book = Body()):
    for index in range(len(BOOKS)):
        if BOOKS[index].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[index] = updated_book
    return {'message':'book updated '}

@app.delete('/books/delete_book/{title}')
async def delete_book(title: str):
    for index in range(len(BOOKS)):
        if BOOKS[index].get('title').casefold() == title.casefold():
            BOOKS.pop(index)
            break
    return {'message':'book deleted '}
from models import db, Book, Loan, User

def get_books():
    books = Book.query.all()
    return [{"id": book.id, "title": book.title, "author": book.author, "available": book.available} for book in books]

def add_book(book_data):
    book = Book(**book_data)
    db.session.add(book)
    db.session.commit()
    return {"message": "Book added successfully"}

def update_book(book_id, book_data):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Book not found"}, 404
    book.title = book_data.get('title', book.title)
    book.author = book_data.get('author', book.author)
    db.session.commit()
    return {"message": "Book updated successfully"}

def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Book not found"}, 404
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted successfully"}

def borrow_book(user_id, book_id):
    book = Book.query.get(book_id)
    if not book or not book.available:
        return {"error": "Book not available"}, 400
    loan = Loan(user_id=user_id, book_id=book_id)
    book.available = False
    db.session.add(loan)
    db.session.commit()
    return {"message": "Book borrowed"}

def return_book(user_id, book_id):
    loan = Loan.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
    if not loan:
        return {"error": "No active loan for this book"}, 400
    loan.return_date = datetime.now()
    book = Book.query.get(book_id)
    book.available = True
    db.session.commit()
    return {"message": "Book returned"}

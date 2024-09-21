from flask import Flask, request, jsonify
from models import db, Book, User, Loan

app = Flask(__name__)
app.config.from_object('config.variables.Config')

db.init_app(app)

@app.route('/books', methods=['GET'])
def list_books():
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "available": book.available
    } for book in books])

@app.route('/books', methods=['POST'])
def add_new_book():
    book_data = request.json
    book = Book(**book_data)
    db.session.add(book)
    db.session.commit()
    return {"message": "Book added successfully"}

@app.route('/books/<int:id>', methods=['PUT'])
def update_book_details(id):
    book = Book.query.get(id)
    if not book:
        return {"error": "Book not found"}, 404
    book_data = request.json
    book.title = book_data.get('title', book.title)
    book.author = book_data.get('author', book.author)
    db.session.commit()
    return {"message": "Book updated successfully"}

@app.route('/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    book = Book.query.get(id)
    if not book:
        return {"error": "Book not found"}, 404
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted successfully"}

@app.route('/borrow', methods=['POST'])
def borrow_a_book():
    data = request.json
    book = Book.query.get(data['book_id'])
    if not book or not book.available:
        return {"error": "Book not available"}, 400
    loan = Loan(user_id=data['user_id'], book_id=data['book_id'])
    book.available = False
    db.session.add(loan)
    db.session.commit()
    return {"message": "Book borrowed"}

@app.route('/return', methods=['POST'])
def return_a_book():
    data = request.json
    loan = Loan.query.filter_by(user_id=data['user_id'], book_id=data['book_id'], return_date=None).first()
    if not loan:
        return {"error": "No active loan for this book"}, 400
    loan.return_date = db.func.now()
    book = Book.query.get(data['book_id'])
    book.available = True
    db.session.commit()
    return {"message": "Book returned"}

if __name__ == '__main__':
    app.run(debug=True)

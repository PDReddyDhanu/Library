from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    available = db.Column(db.Boolean, default=True)
    loans = db.relationship('Loan', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    loans = db.relationship('Loan', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=db.func.now())
    return_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Loan {self.id}>'
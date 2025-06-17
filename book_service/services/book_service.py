from models import db
from models.book_model import Book
from flask import jsonify
from services.JWT_auth import generate_token
from filtres.book_filtre import apply_filters, apply_pagination

def get_book_by_id(id):
    book = Book.query.get(id)
    return book.to_dict() if book  else None

def create_book(data):
    book = Book (title=data.title, author=data.author, year=data.year, isbn=data.isbn)
    db.session.add(book)
    db.session.commit()
    return book.to_dict()

def update_book(id, data):
    book = Book.query.get(id)
    if book :
        book.title = data.title
        book.author = data.author
        book.year = data.year
        book.isbn = data.isbn
        db.session.commit()
        return book.to_dict() 
    else:
        return None
    
def delete_book(id):
    book= Book.query.get(id)
    if book :
        db.session.delete(book)
        db.session.commit()
        return True
    else:
        return False      

def get_books():
    books = Book.query
    books = apply_filters(books, Book, ["author", "year"])
    books = apply_pagination(books)
    return [book.to_dict() for book in books.all()]
    
def signin(data):
    user: jsonify = {
        'id': 1,
        'username': 'admin',
        'password': 'password'
    }
    if data:
        if data.username == user['username'] and data.password == user['password']:
            return generate_token(user['id'])
    return None
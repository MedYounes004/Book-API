from flask import request
from models.book_model import Book

def filter_books_by_author(books, author):
    return books.query.filter(Book.author.ilike(f'%{author}%')).order_by(Book.id.asc())

def filter_books_by_year(books, year):
    return books.query.filter(Book.year == year).order_by(Book.id.asc())

def paginate_books(books):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10
    return books.offset((page - 1) * limit).limit(limit).all(), page, limit


from flask import request
from models.book_model import Book

def filter_books_by_author(query, author):
    return query.filter(Book.author.ilike(f'%{author}%')).order_by(Book.id.asc())

def filter_books_by_year(query, year):
    return query.filter(Book.year == year).order_by(Book.id.asc())

def paginate_books(query):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10
    
    page = max(1, page)
    limit = max(1, min(100, limit))
    
    paginated_results = query.offset((page - 1) * limit).limit(limit).all()
    return paginated_results, page, limit

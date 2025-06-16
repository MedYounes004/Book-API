from flask import request
from models.book_model import Book

"""def filter_books_by_author(books, author):
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
    return books.offset((page - 1) * limit).limit(limit).all(), page, limit"""

def filter_books_by_author(query, author):
    """
    Filter books by author name (case-insensitive partial match)
    Args:
        query: SQLAlchemy query object
        author: Author name to search for
    Returns:
        Filtered query object
    """
    return query.filter(Book.author.ilike(f'%{author}%')).order_by(Book.id.asc())

def filter_books_by_year(query, year):
    """
    Filter books by publication year
    Args:
        query: SQLAlchemy query object
        year: Publication year (integer)
    Returns:
        Filtered query object
    """
    return query.filter(Book.year == year).order_by(Book.id.asc())

def paginate_books(query):
    """
    Paginate books query
    Args:
        query: SQLAlchemy query object
    Returns:
        Tuple of (paginated_results, page_number, limit)
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10
    
    # Ensure page is at least 1
    page = max(1, page)
    # Ensure limit is reasonable (between 1 and 100)
    limit = max(1, min(100, limit))
    
    paginated_results = query.offset((page - 1) * limit).limit(limit).all()
    return paginated_results, page, limit

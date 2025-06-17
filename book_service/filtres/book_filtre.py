from flask import request
from models.book_model import Book

def apply_filters(query, model, filter_fields):

    for field in filter_fields:
        value = request.args.get(field)
        if value:
            query = query.filter(getattr(model, field).ilike(f"%{value}%"))
    return query

def apply_pagination(query):

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10

    return query.offset((page - 1) * limit).limit(limit)

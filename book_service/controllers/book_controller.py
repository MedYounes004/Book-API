from flask import Blueprint, jsonify, request
from services.book_service import get_book_by_id, create_book, update_book, delete_book, signin
from models.book_model import Book
from filtres.book_filtre import filter_books_by_author, filter_books_by_year, paginate_books
from services.JWT_auth import token_required
from constants.book_constants import welcome_message, Book_added, Book_invalid_data, Book_no_data, Book_not_found, Book_deleted

book_controller = Blueprint('book', __name__)


@book_controller.route('/')
def index():
    return welcome_message(), 200


@book_controller.route('/books', methods=['POST'])
@token_required
def add_book():
    data = request.get_json()
    if data:
        create_book(data)
        return Book_added(), 200
    else:
        return Book_invalid_data(), 400

@book_controller.route('/books', methods=['GET'])
def get_books():
    # Start with the base query object, not the executed results
    query = Book.query
    
    # Get filter parameters
    author = request.args.get('author')
    year = request.args.get('year')
    
    # Apply filters using your helper functions
    if author:
        query = filter_books_by_author(query, author)
    if year:
        try:
            year_int = int(year)
            query = filter_books_by_year(query, year_int)
        except ValueError:
            return jsonify({'error': 'Invalid year format'}), 400
    
    # Apply pagination and get results
    paginated_data, page, limit = paginate_books(query)
    
    if paginated_data:
        # Convert to dictionary format
        books_list = [book.to_dict() for book in paginated_data]
        
        return jsonify({
            'data': books_list,
            'page': page,
            'limit': limit,
            'total_on_page': len(paginated_data)
        }), 200
    else:
        return jsonify(Book_no_data), 404

"""@book_controller.route('/books',methods=['GET'])
def get_books():
    data = Book.query.all()
    if data :
        data = paginate_books(data)
        author = request.args.get('author')
        year = request.args.get('year')
        if author:
            data = filter_books_by_author(data, author)
        if year:
            data = filter_books_by_year(data, year)
        return jsonify({'data': book.to_dict() for book in data}), 200
    else:
        return Book_no_data(), 404"""
    

@book_controller.route('/books/<int:id>',methods=['GET'])
def get_book_id(id):
    book = get_book_by_id(id)
    return jsonify({'data': book}),200 if book else Book_not_found()


@book_controller.route('/books/<int:id>',methods=['PUT'])
def modify_book(id):
    data = request.get_json()
    modif = update_book(id, data)
    if modif:
        return jsonify({'message': 'Book updated successfully', 'data': modif}), 200
    else:
        return Book_not_found(), 404


@book_controller.route('/books/<int:id>',methods=['DELETE'])
@token_required
def remove_book(id):
    if delete_book(id):
        return Book_deleted(), 200
    else:
        return Book_not_found(), 404


@book_controller.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    token = signin(data)
    if token:
        return jsonify({'token': token}), 200
    else:
        return Book_invalid_data(), 400
from flask import Blueprint, jsonify, request
from services.book_service import create_book, get_book_by_id , update_book, delete_book
from models.book_model import Book

book_controller = Blueprint('book', __name__)

@book_controller.route('/')
def index():
    return jsonify({'message': 'Welcome to the Book API'}), 200

@book_controller.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if data:
        create_book(data)
        return jsonify({'message': 'Book added successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400

@book_controller.route('/books',methods=['GET'])
def get_books():
    data = Book.query.all()
    if data :
        return jsonify({'data': book.to_dict() for book in data}), 200
    else:
        return jsonify({'message': 'No books found'}), 404
    
@book_controller.route('/books/<int:id>',methods=['GET'])
def get_book_id(id):
    book = get_book_by_id(id)
    return jsonify({'data': book}),200 if book else jsonify({'message': 'No books found'}), 404

@book_controller.route('/books/<int:id>',methods=['PUT'])
def modify_book(id):
    data = request.get_json()
    modif = update_book(id, data)
    if modif:
        return jsonify({'message': 'Book updated successfully', 'data': modif}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@book_controller.route('/books/<int:id>',methods=['DELETE'])
def remove_book(id):
    if delete_book(id):
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

from flask import Blueprint, jsonify, request
from services.book_service import get_book_by_id, create_book, update_book, delete_book, signin, get_books
from models.book_model import BookModel, LoginModel
from services.JWT_auth import token_required
from constants.book_constants import messages
from pydantic import ValidationError

book_controller = Blueprint('book', __name__)

@book_controller.route('/')
def index():
    return jsonify(messages["welcome_message"]), messages["200"]


@book_controller.route('/books', methods=['POST'])
@token_required
def add_book():
    try:
        data = BookModel(**request.get_json())
        if data:
            create_book(data)
            return jsonify(messages["Book_added"]), messages["200"]
        else:
            return jsonify(messages["Book_invalid_data"]), messages["400"]
    except ValidationError as e :
        return jsonify({'error': e.errors()}), messages["400"]

@book_controller.route('/books', methods=['GET'])
def get_all_books():
    data = get_books()
    if data:
        return jsonify({'data': data}), messages["200"]
    return jsonify(messages["Book_no_data"]), messages["404"]
    
    
@book_controller.route('/books/<int:id>',methods=['GET'])
def get_book(id):
    book = get_book_by_id(id)
    if book:
        return jsonify({'data': book}), messages["200"]  
    else :
        return jsonify(messages["Book_not_found"]), messages["404"]


@book_controller.route('/books/<int:id>',methods=['PUT'])
@token_required
def modify_book(id):
    try:
        data = BookModel(**request.get_json())
        modif = update_book(id, data)
        if modif!= None:
            return jsonify({'message': 'Book updated successfully', 'data': modif}), messages["200"]
        else:
            return jsonify(messages["Book_not_found"]), messages["404"]
    except ValidationError as e:
        return jsonify({'error': e.errors()}), messages["400"]


@book_controller.route('/books/<int:id>',methods=['DELETE'])
@token_required
def remove_book(id):
    if delete_book(id) is True:
        return jsonify(messages["Book_deleted"]), messages["200"]
    else:
        return jsonify(messages["Book_not_found"]), messages["404"]


@book_controller.route('/login',methods=['POST'])
def login():
    try:
        data = LoginModel(**request.get_json())
        token = signin(data)
        if token:
            return jsonify({'token': token}), messages["200"]
        else:
            return jsonify(messages["User_invalid_data"]), messages["400"]
    except ValidationError as e:
        return jsonify({'error': e.errors()}), messages["400"]
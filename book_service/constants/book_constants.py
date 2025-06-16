from flask import jsonify

# book_constants.py
from flask import jsonify

def welcome_message():
    return jsonify({'message': 'Welcome to the Book API'})

def Book_added():
    return jsonify({'message': 'Book added successfully'})

def Book_invalid_data():
    return jsonify({'error': 'Invalid book data provided'})

def Book_no_data():
    return jsonify({'error': 'No data provided'})

def Book_not_found():
    return jsonify({'error': 'Book not found'})

def Book_deleted():
    return jsonify({'message': 'Book deleted successfully'})




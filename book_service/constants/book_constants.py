from flask import jsonify

welcome_message = jsonify({'message': 'Welcome to the Book API'})
Book_added = jsonify({'message': 'Book added successfully'})
Book_not_found = jsonify({'message': 'Book not found'})
Book_deleted = jsonify({'message': 'Book deleted successfully'})
Book_no_data = jsonify({'message': 'No books found'})
Book_invalid_data = jsonify({'message': 'Invalid data'})




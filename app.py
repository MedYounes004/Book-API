from flask import Flask, request, jsonify
from models import db, Book
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, timedelta
from functools import wraps
from flasgger import Swagger
from flasgger.utils import swag_from as swag_from_decorator
import os
import jwt



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(os.path.dirname(__file__), 'books.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre-clé-secrète-très-sécurisée-ici')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-très-sécurisée')
    db.init_app(app)
    return app
app=create_app()

app.config['SWAGGER'] = {
    'title': 'Book API',
    'uiversion': 3,
    'description': 'API for managing books',
    'specs_route': '/swagger'
}    

swagger = Swagger(app)

class CreateBook(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1800, le=2025)  # Ensure valid year range
    isbn: str = Field(..., min_length=1, max_length=50)
    class Config:
        extra = 'forbid'

def generate_token(user_id):
    """Génère un token JWT pour un utilisateur donné"""
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),  # Issued at
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']  # Expiration
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Vérifie et décode un token JWT"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide

def token_required(f):
    """Décorateur pour protéger les routes avec JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupération du token depuis l'header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False, 
                'error': 'Token is missing! Use: Authorization: Bearer <token>'
            }), 401
        
        # Extraction du token (format: "Bearer <token>")
        try:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header  # Si pas de préfixe Bearer
        except IndexError:
            return jsonify({
                'success': False, 
                'error': 'Invalid token format! Use: Bearer <token>'
            }), 401
        
        # Vérification du token
        user_id = verify_token(token)
        if user_id is None:
            return jsonify({
                'success': False, 
                'error': 'Invalid or expired token!'
            }), 401
        
        # Ajout de l'user_id au contexte de la requête
        request.current_user_id = user_id
        
        return f(*args, **kwargs)
    
    return decorated
"""
def generate_token(id):
    payload = {
        'user_id': id,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']  # Token valid for 1 hour
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing!'}), 401
        
        try:
            user_id = verify_token(token)
            if user_id is None:
                return jsonify({'success': False, 'error': 'Invalid or expired token!'}), 401
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        
        return f(*args, **kwargs)
    return decorated
"""
@app.route('/')

def index():
    return jsonify({
        'success': True,
        'message': 'Welcome to the Book API'
    }), 200

@app.route('/books', methods=['POST'])
@token_required
@swag_from_decorator({
    'tags': ['Books'],
    'description': 'Add a new book',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': CreateBook.model_json_schema()
        }
    ],
    'responses': {
        201: {
            'description': 'Book added successfully',
            'schema': CreateBook.model_json_schema()
        },
        400: {
            'description': 'Validation error'
        },
        500: {
            'description': 'Server error'
        }
    }
})
def add_book():
    try:
        data = CreateBook(**request.get_json())
        book = Book(
            title = data.title,
            author = data.author,
            year = data.year,
            isbn = data.isbn
        )
        db.session.add(book) 
        db.session.commit()

        return jsonify({
            'success': True,
            'data': book.to_dic(),
            'message': 'Book added successfully'
        }), 201
    except ValidationError as v:
        return jsonify({'success': False,'errors': v.errors()}), 400
    except Exception as e:
        return jsonify({'success': False,'error': str(e)}), 500


@app.route('/books',methods=['GET'])
@swag_from_decorator({
    'tags': ['Books'],
    'description': 'Get a list of books',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'description': 'Page number for pagination'
        },
        {
            'name': 'author',
            'in': 'query',
            'type': 'string',
            'description': 'Filter books by author name'
        },
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'description': 'Filter books by publication year'
        }
    ],
    'responses': {
        200: {
            'description': 'List of books retrieved successfully'
            }
        },
        500: {
            'description': 'Server error'
        }
    }
)
def get_books():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 2

        book_athor = request.args.get('author', type=str)
        book_year = request.args.get('year', type=int)
        query = Book.query

        if book_athor:
           query = query.filter(Book.author.ilike(f'%{book_athor}%'))
        if book_year:
           query = query.filter(Book.year == book_year)

        query =query.order_by(Book.id.asc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        books = pagination.items

        return jsonify({
            'success': True,
            'data': [book.to_dic() for book in books],
            'total_pages': pagination.pages,
            'total_items': pagination.total
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/books/<int:id>',methods=['GET'])
@swag_from_decorator({
    'tags': ['Books'],
    'description': 'Get a book by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the book to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Book retrieved successfully'
            }
        },
        404: {
            'description': 'Book not found'
        },
        500: {
            'description': 'Server error'
        }
})
def get_book_id(id):
    try:
        book = Book.query.get_or_404(id)

        return jsonify({
            'success': True,
            'data': book.to_dic()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/books/<int:id>',methods=['PUT'])
@token_required
@swag_from_decorator({
    'tags': ['Books'],
    'description': 'Update a book by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the book to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': CreateBook.model_json_schema()
        }
    ],
    'responses': {
        200: {
            'description': 'Book updated successfully',
            'schema': CreateBook.model_json_schema()
        },
        404: {
            'description': 'Book not found'
        },
        400: {
            'description': 'Validation error'
        },
        500: {
            'description': 'Server error'
        }
    }
})
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404
    try:
        data = CreateBook(**request.get_json())

        book.title = data.title
        book.author = data.author
        book.year = data.year
        book.isbn = data.isbn

        db.session.commit()
    
        return jsonify({
            'success': True,
            'data': book.to_dic(),
            'message': 'Book updated successfully'
        }), 200
    except ValidationError as v:
        return jsonify({'success': False,'errors': v.errors()}), 400
    except Exception as e:
        return jsonify({'success': False,'error': str(e)}), 500
        

@app.route('/books/<int:id>',methods=['DELETE'])
@token_required
@swag_from_decorator({
    'tags': ['Books'],
    'description': 'Delete a book by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the book to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Book deleted successfully',
            'schema': CreateBook.model_json_schema()
        },
        404: {
            'description': 'Book not found'
        },
        400: {
            'description': 'Validation error'
        },
        500: {
            'description': 'Server error'
        }
    } 
})                    
def delete_book(id):
    try:
        book = Book.query.get_or_404(id)
        title = book.title
        db.session.delete(book)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Book {title} deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

class LoginModel(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    password: str = Field(..., min_length=1, max_length=30)
    class Config:
        extra = 'forbid'

@app.route('/login',methods=['POST'])
@swag_from_decorator({
    'tags': ['Authentication'],
    'description': 'User login',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': LoginModel.model_json_schema()
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'token': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Invalid username or password'
        },
        400: {
            'description': 'Validation error'
        },
        500: {
            'description': 'Server error'
        }
    }
})
def login():
    user: jsonify = {
        'id': 1,
        'username': 'admin',
        'password': 'password'
    }
    try:
        data = LoginModel(**request.get_json())
        if data.username == user['username'] and data.password == user['password']:
            token = generate_token(user['id'])
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    except ValidationError as v:
        return jsonify({'success': False, 'errors': v.errors()}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@app.errorhandler(404)
@swag_from_decorator({
    'tags': ['Errors'],
    'description': 'Resource not found',
    'responses': {
        404: {
            'description': 'Resource not found'
        }
    }
})
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Ressource not found'
    }), 404

@app.errorhandler(500)
@swag_from_decorator({
    'tags': ['Errors'],
    'description': 'Internal server error',
    'responses': {
        500: {
            'description': 'Internal server error'
        }
    }
})
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Server Error'
    }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
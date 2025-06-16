from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),  
        'exp': datetime.utcnow() + timedelta(minutes=10)  
    }
    return jwt.encode(payload, 'jwt-secret-key-très-sécurisée', algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, 'jwt-secret-key-très-sécurisée', algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token is missing! Use: Authorization: Bearer <token>'}), 401
        
        try:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header 
        except IndexError:
            return jsonify({'error': 'Invalid token format! Use: Bearer <token>'}), 401
        
        user_id = verify_token(token)
        if user_id is None:
            return jsonify({ 'error': 'Invalid or expired token!'}), 401
        
        request.current_user_id = user_id
        return f(*args, **kwargs)
    
    return decorated
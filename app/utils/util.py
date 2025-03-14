from PRIVATE import MYSECRETKEY
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import jwt




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

            try:
                data = jwt.decode(token, MYSECRETKEY, algorithms=['HS256'])
                user_id = data['sub']
                
            except jwt.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(user_id, *args, **kwargs)
        
        else:
            return jsonify({'message': 'You must be logged in to access this area!'}), 401

    return decorated


def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id)
    }

    token = jwt.encode(payload, MYSECRETKEY, algorithm='HS256')
    return token

import jwt 
from flask import request,jsonify
from functools import wraps 
from app import app 



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            token = token.split(" ")[1]
            print(token)
            payload = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid Token'}), 403
    return decorated



def role_required(role_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:
                try:
                    if token.startswith("Bearer "):
                        token = token.split(" ")[1]
                        payload = jwt.decode(
                            token, app.config['SECRET_KEY'], algorithms=["HS256"])
                        user_role = payload.get('role_id')
                        if user_role == role_id:
                            return func(*args, **kwargs)
                        else:
                            return jsonify({'error': 'Insufficient permission'}), 403  # 403 Forbidden
                    else:
                        return jsonify({'error': 'Invalid token format'}), 401  # 401 Unauthorized
                except jwt.ExpiredSignatureError:
                    return jsonify({'error': 'Token has expired'}), 401  # 401 Unauthorized
                except jwt.InvalidTokenError:
                    return jsonify({'error': 'Token is invalid'}), 401  # 401 Unauthorized
            else:
                return jsonify({'error': 'Token is missing'}), 401  # 401 Unauthorized
        return wrapper
    return decorator




    #             try:
    #                 token = token.split(" ")[1]
    #                 payload = jwt.decode(
    #                     token, app.config['SECRET_KEY'], algorithms=["HS256"])
    #                 user_role = payload.get('role_id')
    #                 if user_role == role_id:
    #                     return func(*args, **kwargs)
    #                 else:
    #                     return jsonify({'error': 'insufficient permission'})
    #             except jwt.ExpiredSignatureError:
    #                 return jsonify({'error': 'Token has expired'}), 401
    #             except jwt.InvalidTokenError:
    #                 return jsonify({'error': 'Token is invalid'}), 401
    #         else:
    #             return jsonify({'error': 'Token is missing'}), 401
    #     return wrapper
    # return decorator

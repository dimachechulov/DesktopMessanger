import jwt
from datetime import datetime, timedelta

# Secret key for encoding and decoding JWT token
SECRET_KEY = 'your_secret_key'

# Function to generate JWT token
def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to decode and verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'


token = generate_token("Dmitry")

print(verify_token(token))
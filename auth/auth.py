import jwt
from datetime import datetime, timedelta

from DBManager import DBManager
from werkzeug.security import generate_password_hash, check_password_hash

# Secret key for encoding and decoding JWT token
SECRET_KEY = 'your_secret_key'

# Function to generate JWT token

class AuthService:
    def __init__(self):
        self.db = DBManager()

    def register_user(self, username, password, email, age):
        users = self.db.get_all_users()
        for user in users:
            if username == user.name:
                raise ValueError("Username must be unique")
        self.db.create_user(name=username, password=generate_password_hash(password), email=email,age=age)
        return self.login_user(username, password)

    def login_user(self, username,password):
        user = self.db.get_user_by_name(username=username)
        if user is None:
            raise ValueError("Wrong username")

        if not check_password_hash(user.password , password):
            raise ValueError("Wrong password")
        return self.generate_token(username, password), user

    def generate_token(self, username, password):
        payload = {
            'username': username,
            'password' : password,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    # Function to decode and verify JWT token
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'


# token = generate_token("Dmitry", "changeme")
#
# print(verify_token(token))

print()
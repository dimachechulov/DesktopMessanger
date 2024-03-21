from datetime import datetime
from peewee import *
import psycopg2
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from models.models import User, Base, Message


# conn = None
#
# try:
#     conn = psycopg2.connect(
#         dbname='OOP_postgres',
#         user='postgres',
#         password='postgres',
#         host='localhost',
#         port = '5432'
#     )
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT version();")
#         print(f"Service version: {cursor.fetchone()}")
#     cursor = conn.cursor()
# except Exception as ex:
#     print(f"INFO {ex}")
class DBManager:
    def __init__(self):
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/OOP_postgres')
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def create_user(self, name,email,age, password):
        user =User(name=name, email=email, age=int(age), password=password)
        self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_name(self, username):
        return self.session.query(User).filter_by(name=username).first()

    def create_message(self, from_username, to_username, content):
        from_user = self.session.query(User).filter_by(name=from_username).first()
        to_user = self.session.query(User).filter_by(name=to_username).first()
        message = Message(from_user=from_user.id, to_user=to_user.id, content=content)
        self.session.add(message)
        self.session.commit()
        return message

    def get_messages_by_two_users(self, from_username, to_username):
        from_user = self.session.query(User).filter_by(name=from_username).first()
        to_user = self.session.query(User).filter_by(name=to_username).first()
        messages =  self.session.query(Message).filter(
    or_(
        and_(Message.from_user == from_user.id, Message.to_user == to_user.id),
        and_(Message.from_user == to_user.id, Message.to_user == from_user.id)
    )).order_by(Message.created_at)
        return list(messages)





#
# manan = DBManager()
#
# manan.create_user("Dmitry1", "dim1.chechulov@gmail.com", 20, "12345678")
#
# users = manan.all_users()
#
# for user in users:
#   print(user.id, user.name, user.email, user.age, user.password)








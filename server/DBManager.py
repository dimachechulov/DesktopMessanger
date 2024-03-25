from datetime import datetime
from peewee import *
import psycopg2
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from models.models import User, Base, Message, Query, Friend


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


    def find_users_by_name(self, username):
        return self.session.query(User).filter(User.name.startswith(username)).all()

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

    def create_query(self, from_username, to_username):
        from_user = self.session.query(User).filter_by(name=from_username).first()
        to_user = self.session.query(User).filter_by(name=to_username).first()
        query = Query(from_user=from_user.id, to_user=to_user.id)
        self.session.add(query)
        self.session.commit()

    def delete_query(self, from_username, to_username):
        from_user = self.session.query(User).filter_by(name=from_username).first()
        to_user = self.session.query(User).filter_by(name=to_username).first()
        query = self.session.query(Query).filter_by(from_user=from_user.id, to_user=to_user.id).first()
        self.session.delete(query)
        self.session.commit()

    def get_query(self, from_username, to_username):
        from_user = self.session.query(User).filter_by(name=from_username).first()
        to_user = self.session.query(User).filter_by(name=to_username).first()
        return self.session.query(Query).filter_by(from_user=from_user.id, to_user=to_user.id).first()

    def create_friend(self, username1, username2):
        user1 = self.session.query(User).filter_by(name=username1).first()
        user2 = self.session.query(User).filter_by(name=username2).first()
        friend = Friend(user1=user1.id, user2=user2.id)
        self.session.add(friend)
        self.session.commit()

    def is_friend(self, username1, username2):
        user1 = self.session.query(User).filter_by(name=username1).first()
        user2 = self.session.query(User).filter_by(name=username2).first()
        friend =  self.session.query(Friend).filter(
            or_(
                and_(Friend.user1 == user1.id, Friend.user2 == user2.id),
                and_(Friend.user1 == user2.id, Friend.user2 == user1.id)
            )).all()
        return friend

    def get_friends(self, username):
        user = self.session.query(User).filter_by(name=username).first()
        friends_user1 = self.session.query(User).join(Friend, Friend.user2 == User.id).filter(
            Friend.user1 == user.id).all()

        friends_user2 = self.session.query(User).join(Friend, Friend.user1 == User.id).filter(
            Friend.user2 == user.id).all()
        friends = list(friends_user1) + list(friends_user2)
        return friends
















#
# manan = DBManager()
#
# manan.create_user("Dmitry1", "dim1.chechulov@gmail.com", 20, "12345678")
#
# users = manan.all_users()
#
# for user in users:
#   print(user.id, user.name, user.email, user.age, user.password)








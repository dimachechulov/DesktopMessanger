from datetime import datetime
from peewee import *
import psycopg2
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from models.models import User, Base, Message, Query, Friend, Group, GroupUser


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
    def __init__(self, db_url):
        engine = create_engine(db_url)
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

    def create_group(self, name, owner_name):
        user = self.session.query(User).filter_by(name=owner_name).first()
        group = Group(name=name, owner=user.id)
        self.session.add(group)
        self.session.commit()

    def add_user_in_group(self, groupname, username, is_admin):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        group_user = GroupUser(group=group.id, user=user.id, is_admin=is_admin)
        self.session.add(group_user)
        self.session.commit()

    def get_messages_in_group(self, name):
        group = self.session.query(Group).filter_by(name=name).first()

        messages = self.session.query(Message).filter(Message.group == group.id).all()
        return messages

    def get_owner(self, groupname):
        group = self.session.query(Group).filter_by(name=groupname).first()
        owner = self.session.query(User).filter_by(id=group.owner).first()
        return owner
    def is_admin_in_group(self, username,groupname):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        return self.session.query(GroupUser).filter_by(user=user.id, group=group.id).first().is_admin


    def is_owner_in_group(self, username,groupname):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        return user.id == group.owner
    def get_groups_by_user(self, username):
        user = self.session.query(User).filter_by(name=username).first()
        groups = self.session.query(Group).join(GroupUser, GroupUser.group == Group.id).filter(
            GroupUser.user == user.id).all()
        return groups

    def create_message_in_group(self,from_username, group,content):
        user = self.session.query(User).filter_by(name=from_username).first()
        group = self.session.query(Group).filter_by(name=group).first()
        message = Message(from_user=user.id, group=group.id, content=content)
        self.session.add(message)
        self.session.commit()
        return message

    def get_users_in_group(self,groupname):
        group = self.session.query(Group).filter_by(name=groupname).first()
        users = self.session.query(User).join(GroupUser, GroupUser.user == User.id).filter(
            GroupUser.group == group.id).all()
        return users

    def get_users_in_group_no_admin(self, groupname):


        group = self.session.query(Group).filter_by(name=groupname).first()
        users = self.session.query(User).join(GroupUser, GroupUser.user == User.id).filter(
            GroupUser.group == group.id, GroupUser.is_admin == False).all()
        return users

    def get_user_in_group_only_admin(self, groupname):
        group = self.session.query(Group).filter_by(name=groupname).first()
        users = self.session.query(User).join(GroupUser, GroupUser.user == User.id).filter(
            GroupUser.group == group.id, GroupUser.is_admin).all()
        return users


    def add_user_in_admin(self, username, groupname):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        group_user=  self.session.query(GroupUser).filter(
            and_(
                GroupUser.user == user.id,
                GroupUser.group == group.id
            )).first()
        group_user.is_admin = True
        self.session.add(group_user)
        self.session.commit()

    def delete_admin_from_group(self, username, groupname):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        group_user = self.session.query(GroupUser).filter(
            and_(
                GroupUser.user == user.id,
                GroupUser.group == group.id
            )).first()
        group_user.is_admin = False
        self.session.add(group_user)
        self.session.commit()



    def delete_from_group(self, username, groupname):
        user = self.session.query(User).filter_by(name=username).first()
        group = self.session.query(Group).filter_by(name=groupname).first()
        group_user = self.session.query(GroupUser).filter(
            and_(
                GroupUser.user == user.id,
                GroupUser.group == group.id
            )).first()
        self.session.delete(group_user)
        self.session.commit()

























#
# manan = DBManager()
#
# manan.create_user("Dmitry1", "dim1.chechulov@gmail.com", 20, "12345678")
#
# users = manan.all_users()
#
# for user in users:
#   print(user.id, user.name, user.email, user.age, user.password)








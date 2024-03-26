from datetime import datetime


from models.models import User, Message, Query, Friend


class FakeDBManager:
    def __init__(self):
        self.users = []
        self.messages = []
        self.querys = []
        self.friends = []


    def create_user(self, name,email,age, password):
        user =User(id=len(self.users), name=name, email=email, age=int(age), password=password)
        self.users.append(user)

    def get_all_users(self):
        return self.users

    def get_user_by_name(self, username):
        for user in self.users:
            if user.name == username:
                return user





    def create_message(self, from_username, to_username, content):
        from_user = self.get_user_by_name(from_username)
        to_user = self.get_user_by_name(to_username)
        message = Message(id=len(self.messages), from_user=from_user.id, to_user=to_user.id, content=content, created_at=datetime.now())
        self.messages.append(message)
        return message

    def get_messages_by_two_users(self, from_username, to_username):
        from_user = self.get_user_by_name(from_username)
        to_user = self.get_user_by_name(to_username)

        result = []
        for message in self.messages:
            if (message.from_user == from_user.id and message.to_user == to_user.id) or (message.to_user == from_user.id and message.from_user == to_user.id):
                result.append(message)
        return result

    def create_query(self, from_username, to_username):
        from_user = self.get_user_by_name(from_username)
        to_user = self.get_user_by_name(to_username)
        query = Query(id=len(self.querys),from_user=from_user.id, to_user=to_user.id)
        self.querys.append(query)

    def delete_query(self, from_username, to_username):
        from_user = self.get_user_by_name(from_username)
        to_user = self.get_user_by_name(to_username)
        for query in self.querys:
            if query.from_user==from_user.id and query.to_user==to_user.id:
                self.querys.remove(query)
                return


    def get_query(self, from_username, to_username):
        from_user = self.get_user_by_name(from_username)
        to_user = self.get_user_by_name(to_username)
        for query in self.querys:
            if query.from_user == from_user.id and query.to_user == to_user.id:
                return query

    def create_friend(self, username1, username2):
        user1 = self.get_user_by_name(username1)
        user2 = self.get_user_by_name(username2)
        friend = Friend(user1=user1.id, user2=user2.id)
        self.friends.append(friend)


    def is_friend(self, username1, username2):
        user1 = self.get_user_by_name(username1)
        user2 = self.get_user_by_name(username2)
        for friend in self.friends:
            if (friend.user1 == user1.id and friend.user2 == user2.id) or  (friend.user1 == user2.id and friend.user2 == user1.id):
                return True
        return False


    def get_friends(self, username):
        user = self.get_user_by_name(username)
        ids = []
        result = []
        for friend in self.friends:
            if friend.user2 == user.id:
                ids.append(friend.user1)
            elif friend.user1 == user.id:
                ids.append(friend.user2)

        return [user for user in self.users if user.id in ids]

from datetime import datetime


from models.models import User, Message, Query, Friend, Group, GroupUser


class FakeDBManager:
    def __init__(self):
        self.users = []
        self.messages = []
        self.querys = []
        self.friends = []
        self.groups = []
        self.group_users = []


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

    def create_group(self, name, owner_name):
        user = self.get_user_by_name(owner_name)
        group = Group(id=len(self.groups), name=name, owner=user.id)
        self.groups.append(group)
        self.add_user_in_group(name, owner_name, True)


    def get_group_by_name(self, name):
        for group in self.groups:
            if group.name == name:
                return group
        return -1
    def add_user_in_group(self, groupname, username, is_admin):
        user = self.get_user_by_name(username)
        group = self.get_group_by_name(groupname)
        group_user = GroupUser(id=len(self.group_users), group=group.id, user=user.id, is_admin=is_admin)
        self.group_users.append(group_user)

    def get_group_user(self, groupname, username):
        user = self.get_user_by_name(username)
        group = self.get_group_by_name(groupname)
        for group_user in self.group_users:
            if group_user.group == group.id and group_user.user == user.id:
                return group_user
        return -1



    def get_messages_in_group(self, name):
        group = self.get_group_by_name(name)
        result = []
        for message in self.messages:
            if message.group == group.id:
                result.append(message)
        return result

    def get_owner(self, groupname):
        group = self.get_group_by_name(groupname)
        for user in self.users:
            if user.id == group.owner:
                return user
        return -1



    def is_admin_in_group(self, username,groupname):
        return self.get_group_user(groupname, username).is_admin


    def is_owner_in_group(self, username,groupname):
        user = self.get_user_by_name(username)
        group = self.get_group_by_name(groupname)
        return user.id == group.owner
    def get_groups_by_user(self, username):
        user = self.get_user_by_name(username)
        id_groups = [group_user.group for group_user in self.group_users if group_user.user == user.id]
        groups = [group for group in self.groups if group.id in id_groups]
        return groups

    def create_message_in_group(self,from_username, group,content):
        user = self.get_user_by_name(from_username)
        group = self.get_group_by_name(group)
        message = Message(id=len(self.messages), from_user=user.id, group=group.id, content=content, created_at=datetime.now())
        self.messages.append(message)
        return message

    def get_users_in_group(self,groupname):
        group = self.get_group_by_name(groupname)
        id_users= [group_user.user for group_user in self.group_users if group_user.group == group.id]
        users = [user for user in self.users if user.id in id_users]
        return users

    def get_users_in_group_no_admin(self, groupname):
        group = self.get_group_by_name(groupname)
        id_users = [group_user.user for group_user in self.group_users if group_user.group == group.id and not group_user.is_admin]
        users = [user for user in self.users if user.id in id_users]
        return users

    def get_user_in_group_only_admin(self, groupname):
        group = self.get_group_by_name(groupname)
        id_users = [group_user.user for group_user in self.group_users if group_user.group == group.id and group_user.is_admin]
        users = [user for user in self.users if user.id in id_users]
        return users

    def add_user_in_admin(self, username, groupname):
        group_user = self.get_group_user(groupname, username)
        group_user.is_admin = True


    def delete_admin_from_group(self, username, groupname):
        group_user = self.get_group_user(groupname, username)
        group_user.is_admin = False

    def delete_from_group(self, username, groupname):
        group_user = self.get_group_user(groupname, username)
        self.group_users.remove(group_user)


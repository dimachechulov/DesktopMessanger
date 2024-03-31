from configs.default import ACTION, SENDER, DESTINATION, PREVIOUS, MESSAGE_TEXT


class GroupManager:
    def __init__(self, db):
        self.db = db


    def create_group(self, request):

        self.db.create_group(request['NAME'], request['ADMIN'])
        response = {

            ACTION: 'CREATE_GROUP',
            'CREATED': True,
            'GROUP' : request['NAME']
        }
        return response

    # request = {
    #     'TOKEN': self.token,
    #     ACTION: 'OPEN_GROUP',
    #     'USER': self.user['name'],
    #     'NAME': name
    # }

    def open_group(self, request):
        previous_messages = self.db.get_messages_in_group(request['NAME'])
        all_users = self.db.get_users_in_group(request['NAME'])
        all_users_json = {user.id : user.name for user in all_users}
        messages_json = [{'CONTENT': msg.content, SENDER: all_users_json[msg.from_user],
                          'CREATE_AT': msg.created_at.strftime("%I:%M")} for msg in previous_messages]
        responce = {
            ACTION: 'OPEN_GROUP',
            'GROUP': request['NAME'],
            'MESSAGES': messages_json,
        }

        is_owner = self.db.is_owner_in_group(request['USER'], request['NAME'])
        if is_owner:
            responce['STATUS'] = 'OWNER'
        else:
            is_admin = self.db.is_admin_in_group(request['USER'], request['NAME'])
            if is_admin:
                responce['STATUS'] = 'ADMIN'
            else:
                responce['STATUS'] = 'NOTHING'
        return responce

    # request = {
    #     'TOKEN': self.token,
    #     ACTION: 'GROUPS_BY_USER',
    #     'USER': self.user['name'],
    # }

    def groups_by_user(self, request):
        groups = self.db.get_groups_by_user(request['USER'])
        groups_json = [{'NAME': group.name} for group in groups]
        responce = {
            ACTION: 'GROUPS_BY_USER',
            'GROUPS': groups_json,
        }
        return responce



    # request = {
    #     'TOKEN': self.token,
    #     ACTION: 'ADD_IN_GROUP',
    #     'USER': username,
    #     'GROUP': self.selected_group['NAME']
    # }

    # request = {
    #     ACTION: "GET_USERS_IN_GROUPS",
    #     "GROUP": self.selected_group,
    #     "USER": self.user['name'],
    #     'METHOD': method
    # }
    def add_in_group(self, request):
        self.db.add_user_in_group(username=request['USER'], groupname=request['GROUP'], is_admin=False)
        responce = {
            ACTION: 'ADD_IN_GROUP',
            'USER': request['USER'],
            'GROUP': request['GROUP'],
            'ADDED' : True
        }
        return responce

    def add_in_admin(self, request):
        self.db.add_user_in_admin(username=request['USER'], groupname=request['GROUP'])
        responce = {
            ACTION: 'ADD_IN_ADMIN',
            'USER': request['USER'],
            'GROUP': request['GROUP'],
            'ADDED' : True
        }
        return responce

    def delete_admin(self, request):
        self.db.delete_admin_from_group(username=request['USER'], groupname=request['GROUP'])
        responce = {
            ACTION: 'DELETE_ADMIN',
            'USER': request['USER'],
            'GROUP': request['GROUP'],
            'DELETED': True
        }
        return responce

    def delete_from_group(self, request):
        self.db.delete_from_group(username=request['USER'], groupname=request['GROUP'])
        responce = {
            ACTION: 'DELETE_FROM_GROUP',
            'USER': request['USER'],
            'GROUP': request['GROUP'],
            'DELETED': True
        }
        return responce

    def get_users_in_group(self, request):
        owner = self.db.get_owner(request['GROUP'])
        if request['METHOD'] == 'DELETE_ADMIN':
            users = self.db.get_user_in_group_only_admin(request['GROUP'])
            users_json = [{'NAME': user.name} for user in users if user.id != owner.id]
        elif request['METHOD'] == 'ADD_IN_ADMIN':
            users = self.db.get_users_in_group_no_admin(request['GROUP'])
            users_json = [{'NAME': user.name} for user in users if user.id != owner.id]
        elif request['METHOD'] == 'DELETE_FROM_CHAT':
            users = self.db.get_users_in_group(request['GROUP'])
            users_json = [{'NAME': user.name} for user in users if user.id != owner.id]
        else:
            users = self.db.get_users_in_group(request['GROUP'])
            users_json = [{'NAME': user.name} for user in users]



        responce = {
            ACTION: 'GET_USERS_IN_GROUP',
            'USERS': users_json,
            'METHOD': request['METHOD']
        }
        return responce










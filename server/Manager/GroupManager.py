from configs.default import ACTION, SENDER, DESTINATION, PREVIOUS, MESSAGE_TEXT


class GroupManager:
    def __init__(self, db):
        self.db = db


    def create_group(self, request):

        self.db.create_group(request['NAME'])

        self.db.add_user_in_group(name=request['NAME'], username=request['ADMIN'], is_admin=True)

        response = {
            ACTION: 'CREATE_GROUP',
            'CREATED': True
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

        is_admin = self.db.is_admin_in_group(request['USER'], request['NAME'])
        responce = {
            ACTION: 'OPEN_GROUP',
            'GROUP': request['NAME'],
            'MESSAGES': messages_json,
            'IS_ADMIN':is_admin
        }
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

    def get_users_in_group(self, request):
        if request['NO_ADMIN']:
            users = self.db.get_users_in_group_no_admin(request['GROUP'])
        else:
            users = self.db.get_users_in_group(request['GROUP'])

        users_json = [{'NAME': user.name} for user in users]
        responce = {
            ACTION: 'GET_USERS_IN_GROUP',
            'USERS': users_json,
            'METHOD': request['METHOD']
        }
        return responce










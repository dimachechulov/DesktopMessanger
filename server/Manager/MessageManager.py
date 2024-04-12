from configs.default import ACTION, SENDER, DESTINATION, PREVIOUS, MESSAGE_TEXT


class MessageManager:
    def __init__(self, db):
        self.db = db


    def get_previous_messages(self, request):
        messages = self.db.get_messages_by_two_users(from_username=request[SENDER], to_username=request[DESTINATION])
        messages_json = [{'CONTENT': msg.content, SENDER: msg.from_user, DESTINATION: msg.to_user,
                          'CREATE_AT': msg.created_at.strftime("%I:%M"), "ID": msg.id} for msg in messages]
        response = {
            ACTION: PREVIOUS,
            SENDER: request[SENDER],
            DESTINATION: request[DESTINATION],
            'MESSAGE': messages_json
        }
        return response

    def create_message(self, request):
        msg = self.db.create_message(from_username=request[SENDER], to_username=request[DESTINATION],
                                content=request[MESSAGE_TEXT])
        msg_json = {
            SENDER: request[SENDER],
            DESTINATION: request[DESTINATION],
            MESSAGE_TEXT: request[MESSAGE_TEXT],
            "CREATE_AT": msg.created_at.strftime("%I:%M"),
            "ID": msg.id,
        }
        return msg_json

    def create_message_in_group(self, request):
        msg = self.db.create_message_in_group(from_username=request[SENDER], group=request['GROUP'],
                                content=request[MESSAGE_TEXT])
        responce = {
            ACTION: "MESSAGE_IN_GROUP",
            SENDER: request[SENDER],
            "GROUP" : request['GROUP'],
            MESSAGE_TEXT: msg.content,
            "CREATE_AT": msg.created_at.strftime("%I:%M"),
            "ID": msg.id,
        }
        users = self.db.get_users_in_group(groupname=request['GROUP'])
        return responce, users

    def delete_message(self, request):
        msg = self.db.delete_message(request["MESSAGE_ID"])
        to, group = None, None
        if msg.group:
            group = self.db.get_group_by_id(msg.group)
            users = [{'NAME': user.name} for user in self.db.get_users_in_group(group.name)]
        else:
            to = self.db.get_user_by_id(msg.to_user).name
            users = [{'NAME':to}, {'NAME':self.db.get_user_by_id(msg.from_user).name}]

        responce = {
            ACTION: "DELETED_MESSAGE",
            "USERS" : users,
            "DELETED" : True,
            "MESSAGE_ID" : msg.id,
            DESTINATION : to,
            "GROUP" : group.name
        }
        return responce

    def update_message(self, request):
        to, group = None, None
        msg = self.db.update_message(request['MESSAGE_ID'], request['UPDATE_TEXT'])
        if msg.group:
            group = self.db.get_group_by_id(msg.group)
            users = [{'NAME': user.name} for user in self.db.get_users_in_group(group.name)]
        else:
            to = self.db.get_user_by_id(msg.to_user).name
            users = [{'NAME':to}, {'NAME':self.db.get_user_by_id(msg.from_user).name}]

        responce = {
            ACTION: "UPDATED_MESSAGE",
            "USERS": users,
            "UPDATED": True,
            "MESSAGE_ID": msg.id,
            SENDER: self.db.get_user_by_id(msg.from_user).name,
            "UPDATE_TEXT": request['UPDATE_TEXT'],
            DESTINATION: to,
            "GROUP": group.name
        }
        return responce

    # request = {
    #     'TOKEN': self.token,
    #     ACTION: 'SEARCH_MESSAGE',
    #     "SEARCH_TEXT": search_text,
    #     "USERNAME": self.user['name'],
    #     "GROUP": self.selected_group,
    #     "TO": self.receiver_name
    # }

    def search_message(self, request):
        if request['GROUP']:
            msgs = self.db.search_message_in_group(search_text=request['SEARCH_TEXT'], groupname= request['GROUP'])
        else:
            msgs = self.db.search_message_in_chat(search_text=request['SEARCH_TEXT'], to_name= request['TO'])
        msgs_id = [msg.id for msg in msgs]

        responce = {
            ACTION: "SEARCH_MESSAGE",
            "MESSAGES_ID": msgs_id,
        }
        return responce



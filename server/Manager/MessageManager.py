from configs.default import ACTION, SENDER, DESTINATION, PREVIOUS, MESSAGE_TEXT


class MessageManager:
    def __init__(self, db):
        self.db = db


    def get_previous_messages(self, request):
        messages = self.db.get_messages_by_two_users(from_username=request[SENDER], to_username=request[DESTINATION])
        messages_json = [{'CONTENT': msg.content, SENDER: msg.from_user, DESTINATION: msg.to_user,
                          'CREATE_AT': msg.created_at.strftime("%I:%M")} for msg in messages]
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
        # messages_list.append(message)
        msg_json = {
            SENDER: request[SENDER],
            DESTINATION: request[DESTINATION],
            MESSAGE_TEXT: request[MESSAGE_TEXT],
            "CREATE_AT": msg.created_at.strftime("%I:%M")
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
            "CREATE_AT": msg.created_at.strftime("%I:%M")
        }
        users = self.db.get_users_in_group(groupname=request['GROUP'])
        return responce, users

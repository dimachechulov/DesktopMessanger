from SerializerDeserializerModels.SerializerDeserializerModels import SerializerDeSerializerModels

from configs.default import ACTION, SENDER, DESTINATION


class UserManager:
    def __init__(self, db):
        self.db = db


    def get_friend(self, request):
        friends = self.db.get_friends(request['USER'])
        friends_json = [SerializerDeSerializerModels.user_to_json(friend) for friend in friends]
        response = {
            ACTION: 'GET_FRIEND_GROUP',
            'FRIENDS': friends_json
        }
        return response

    def get_user_by_name(self, request):
        users = self.db.find_users_by_name(request['NAME'])
        users_json = [SerializerDeSerializerModels.user_to_json(user) for user in users if user.name != request['USERNAME']]
        response = {
            ACTION: 'GET_USER_BY_NAME',
            'USERS': users_json,
            'METHOD': request['METHOD'],
        }
        return response

    def friend_status(self, request):
        query_from = self.db.get_query(from_username=request[SENDER], to_username=request[DESTINATION])
        if query_from:
            return "SENTED_QUIRY"
        else:
            query_to = self.db.get_query(to_username=request[SENDER], from_username=request[DESTINATION])
            if query_to:
                return  "TO_HE_SENTED_QUIRY"
            else:
                friend = self.db.is_friend(username1=request[SENDER], username2=request[DESTINATION])
                if friend:
                    return "FRIEND"
                else:
                    return "NOTHING"

    def get_profile(self, request):
        groups = self.db.get_groups_by_user(username=request['USERNAME'])
        friends = self.db.get_friends(username=request['USERNAME'])
        user = self.db.get_user_by_name(username=request['USERNAME'])
        friends_json = [SerializerDeSerializerModels.user_to_json(friend) for friend in friends]
        groups_json = [SerializerDeSerializerModels.group_to_json(group) for group in groups]
        responce = {
            ACTION: 'VIEW_PROFILE',
            'FRIENDS': friends_json,
            'GROUPS': groups_json,
            'USER': SerializerDeSerializerModels.user_to_json(user),
        }
        return responce
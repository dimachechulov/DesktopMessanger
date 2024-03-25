from configs.default import ACTION, SENDER, DESTINATION


class UserManager:
    def __init__(self, db):
        self.db = db


    def get_friend(self, request):
        friends = self.db.get_friends(request['USER'])
        friends_json = [{'NAME': friend.name} for friend in friends]
        response = {
            ACTION: 'GET_FRIEND',
            'FRIENDS': friends_json
        }
        return response

    def get_user_by_name(self, request):
        users = self.db.find_users_by_name(request['NAME'])
        users_json = [{'NAME': user.name} for user in users]
        response = {
            ACTION: 'GET_USER_BY_NAME',
            'USERS': users_json
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
                    return  "FRIEND"
                else:
                    return "NOTHING"
from configs.default import ACTION


class QueryManager:
    def __init__(self, db):
        self.db =db


    def create_query(self, request):
        self.db.create_query(from_username=request['FROM_USERNAME'], to_username=request['TO_USERNAME'])
        response_from = {
            ACTION: 'CREATE_QUERY',
            'CREATED': True
        }

        response_to = {
            ACTION: 'DISPLAY_QUERY',
            'FROM_USERNAME': request['FROM_USERNAME']
        }
        return response_from,response_to

    def accept_query(self, request):
        self.db.create_friend(username1=request['FROM_USERNAME'], username2=request['TO_USERNAME'])
        self.db.delete_query(from_username=request['FROM_USERNAME'], to_username=request['TO_USERNAME'])
        response_from = {
            ACTION: 'ACCEPT_QUERY',
            'FRIEND': request['TO_USERNAME'],
        }
        response_to = {
            ACTION: 'ACCEPT_QUERY',
            'FRIEND': request['FROM_USERNAME']
        }
        return response_from, response_to

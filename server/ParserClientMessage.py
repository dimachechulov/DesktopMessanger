import sys
import json
import socket
import select
import argparse
import time
import logging
import logs.server_log_config
from DBManager import DBManager

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, EXIT, RESPONSE_200, RESPONSE_400, PREVIOUS
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from decorators.decorators import MyLogger


server_logger = logging.getLogger('server')

class ParserClientMessage:

    @staticmethod
    def parse_client_msg(request, messages_in_route_list, sock, clients_list, names, db, auth):
        """
        Обработчик сообщений клиентов
        :param message: словарь сообщения
        :param messages_list: список сообщений
        :param sock: клиентский сокет
        :param clients_list: список клиентских сокетов
        :param names: список зарегистрированных клиентов
        :return: словарь ответа
        """
        server_logger.debug(f'Разбор сообщения от клиента: {request}')
        print(f'Разбор сообщения от клиента: {request}')
        if "TOKEN" in request and auth.verify_token(request['TOKEN']):
            if ACTION in request and request[ACTION] == PRESENCE and \
                    TIME in request and USER in request:

                if request[USER][ACCOUNT_NAME] not in names.keys():
                    names[request[USER][ACCOUNT_NAME]] = sock
                    send_message(sock, RESPONSE_200)
                else:
                    response = RESPONSE_400
                    response[ERROR] = 'Имя пользователя уже занято.'
                    send_message(sock, response)
                    clients_list.remove(sock)
                    sock.close()
                return

            # формирует очередь сообщений
            elif ACTION in request and request[ACTION] == MESSAGE and \
                    SENDER in request and DESTINATION in request and \
                    MESSAGE_TEXT in request and TIME in request:
                msg = db.create_message(from_username=request[SENDER], to_username=request[DESTINATION], content=request[MESSAGE_TEXT])
                # messages_list.append(message)
                msg_json = {
                    SENDER : request[SENDER],
                    DESTINATION : request[DESTINATION],
                    MESSAGE_TEXT : request[MESSAGE_TEXT],
                    "CREATE_AT" : msg.created_at.strftime("%I:%M")
                }
                print(f"Add in route {request}")
                messages_in_route_list.append(msg_json)
                return

            elif ACTION in request and request[ACTION] == PREVIOUS and \
                SENDER in request and DESTINATION in request:
                messages = db.get_messages_by_two_users(from_username=request[SENDER], to_username=request[DESTINATION])
                messages_json = [{'CONTENT' : msg.content, SENDER : msg.from_user, DESTINATION : msg.to_user, 'CREATE_AT': msg.created_at.strftime("%I:%M")} for msg in messages]
                response={
                    ACTION:PREVIOUS,
                    SENDER:request[SENDER],
                    DESTINATION : request[DESTINATION],
                    'MESSAGE' :messages_json
                }

                query_from = db.get_query(from_username=request[SENDER], to_username=request[DESTINATION])
                if query_from:
                    response['STATUS'] = "SENTED_QUIRY"
                else:
                    query_to = db.get_query(to_username=request[SENDER], from_username=request[DESTINATION])
                    if query_to:
                        response['STATUS'] = "TO_HE_SENTED_QUIRY"
                    else:
                        friend = db.is_friend(username1=request[SENDER], username2=request[DESTINATION])
                        if friend:
                            response['STATUS'] = "FRIEND"
                        else:
                            response['STATUS'] = "NOTHING"
                send_message(sock, response)

                print(f"Server responce {response}")
                return

            elif ACTION in request and request[ACTION] == 'GET_USER_BY_NAME' and \
                    'NAME' in request:
                users = db.find_users_by_name(request['NAME'])
                users_json = [{'NAME' : user.name}for user in users]
                response={
                    ACTION:'GET_USER_BY_NAME',
                    'USERS' :users_json
                }
                send_message(sock, response)
                print(f"Server responce get user{response}")
                return

            elif ACTION in request and request[ACTION] == 'CREATE_QUERY' and \
                    'TO_USERNAME' in request and 'FROM_USERNAME' in request:

                db.create_query(from_username=request['FROM_USERNAME'], to_username=request['TO_USERNAME'])
                response_from={
                    ACTION:'CREATE_QUERY',
                    'CREATED': True
                }

                response_to = {
                    ACTION: 'DISPLAY_QUERY',
                    'FROM_USERNAME' : request['FROM_USERNAME']
                }
                send_message(sock, response_from)
                print(f"Server responce create query{response_from}")
                if request['TO_USERNAME'] in names and names[request['TO_USERNAME']] in clients_list:
                    send_message(names[request['TO_USERNAME']], response_to)
                    print(f"Server responce display query{response_to}")
                return

            elif ACTION in request and request[ACTION] == 'ACCEPT_QUERY' and \
                    'TO_USERNAME' in request and 'FROM_USERNAME' in request:

                db.create_friend(username1=request['FROM_USERNAME'], username2=request['TO_USERNAME'])
                db.delete_query(from_username=request['FROM_USERNAME'], to_username=request['TO_USERNAME'])
                response_from={
                    ACTION:'ACCEPT_QUERY',
                    'FRIEND': request['TO_USERNAME'],
                }
                response_to = {
                    ACTION: 'ACCEPT_QUERY',
                    'FRIEND' : request['FROM_USERNAME']
                }
                send_message(sock, response_to)
                print(f"Server responce accept query{response_to}")
                if request['FROM_USERNAME'] in names and names[request['FROM_USERNAME']] in clients_list:
                    send_message(names[request['FROM_USERNAME']], response_from)
                    print(f"Server accept query{response_from}")
                return

            # request = {
            #     'TOKEN': self.token,
            #     ACTION: 'GET_FRIEND_STATUS',
            #     'FROM_USERNAME': self.user.name,
            #     'TO_USERNAME': to_username
            # }



            elif ACTION in request and request[ACTION] == 'GET_FRIEND' and \
                    'USER' in request:
                friends = db.get_friends(request['USER'])
                friends_json = [{'NAME' : friend.name}for friend in friends]
                response={
                    ACTION:'GET_FRIEND',
                    'FRIENDS' :friends_json
                }
                send_message(sock, response)
                print(f"Server responce get friends{response}")
                return

            # выход клиента
            elif ACTION in request and request[ACTION] == EXIT and \
                    ACCOUNT_NAME in request:
                clients_list.remove(names[request[USER][ACCOUNT_NAME]])
                names[request[USER][ACCOUNT_NAME]].close()
                del names[request[USER][ACCOUNT_NAME]]
                return

            # возвращает сообщение об ошибке
            else:
                response = RESPONSE_400
                response[ERROR] = 'Некорректный запрос.'
                send_message(sock, response)
                return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Некорректный токен.'
            send_message(sock, response)
            return

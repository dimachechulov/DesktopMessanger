
import logging
from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, EXIT, RESPONSE_200, RESPONSE_400, PREVIOUS
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from decorators.decorators import MyLogger


server_logger = logging.getLogger('server')

class ParserClientMessage:

    @staticmethod
    def parse_client_msg(request, messages_in_route_list, sock, clients_list, names, db, auth, manager):
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
                msg_json = manager.message_manager.create_message(request)
                print(f"Add in route {request}")
                messages_in_route_list.append(msg_json)
                return

            elif ACTION in request and request[ACTION] == PREVIOUS and \
                SENDER in request and DESTINATION in request:
                response = manager.message_manager.get_previous_messages(request)
                response['STATUS'] = manager.user_manager.friend_status(request)
                send_message(sock, response)
                print(f"Server responce {response}")
                return

            elif ACTION in request and request[ACTION] == 'GET_USER_BY_NAME' and \
                    'NAME' in request:
                response = manager.user_manager.get_user_by_name(request)
                send_message(sock, response)
                print(f"Server responce get user{response}")
                return

            elif ACTION in request and request[ACTION] == 'CREATE_QUERY' and \
                    'TO_USERNAME' in request and 'FROM_USERNAME' in request:
                response_from, response_to = manager.quary_manager.create_query(request)
                send_message(sock, response_from)
                print(f"Server responce create query{response_from}")
                if request['TO_USERNAME'] in names and names[request['TO_USERNAME']] in clients_list:
                    send_message(names[request['TO_USERNAME']], response_to)
                    print(f"Server responce display query{response_to}")
                return

            elif ACTION in request and request[ACTION] == 'ACCEPT_QUERY' and \
                    'TO_USERNAME' in request and 'FROM_USERNAME' in request:

                response_from, response_to = manager.quary_manager.accept_quary(request)
                send_message(sock, response_to)
                print(f"Server responce accept query{response_to}")
                if request['FROM_USERNAME'] in names and names[request['FROM_USERNAME']] in clients_list:
                    send_message(names[request['FROM_USERNAME']], response_from)
                    print(f"Server accept query{response_from}")
                return

            elif ACTION in request and request[ACTION] == 'GET_FRIEND' and \
                    'USER' in request:
                response = manager.user_manager.get_friend(request)
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

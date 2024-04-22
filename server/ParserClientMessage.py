
import logging

from psycopg2 import DataError

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, EXIT, RESPONSE_200, RESPONSE_400, PREVIOUS
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from decorators.decorators import MyLogger


server_logger = logging.getLogger('server')

class ParserClientMessage:

    @staticmethod
    def parse_client_msg(request, sock, clients_list, names,  auth, manager):
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
        if ACTION in request and request[ACTION]=="LOGIN" and 'USERNAME' in request and 'PASS' in request:

            response = {
                ACTION: 'LOGIN'
            }
            try:
                token,  user  =  auth.login_user(request['USERNAME'], request['PASS'])
                response["TOKEN"] = token
                response["USER"] = {
                    "name" : user.name,
                    "age" : user.age,
                    "id" : user.id
                }
                names[request["USERNAME"]] = sock
            except ValueError as err:
                response["ERROR"] = err.args
            except DataError as err:
                response['ERROR'] = "Err input in fields"
            except Exception as ex:
                print(ex.args)
            finally:
                send_message(sock, response)
                print(f"Server responce {response}")


        elif ACTION in request and request[ACTION]=="REGISTER" and 'USERNAME' in request and 'PASS' in request\
                and 'AGE' in request and 'EMAIL' in request:

            response = {
                ACTION: 'REGISTER'
            }
            try:
                token,  user  =  auth.register_user(request['USERNAME'], request['PASS'], request['EMAIL'], request['AGE'])
                response["TOKEN"] = token
                response["USER"] = {
                    "name" : user.name,
                    "age" : user.age,
                    "id" : user.id
                }
                names[request["USERNAME"]] = sock
            except ValueError as err:
                response["ERROR"] = err.args
            except DataError as err:
                response['ERROR'] = "Err input in fields"
            except Exception as ex:
                print(ex.args)
            finally:
                send_message(sock, response)
                print(f"Server responce {response}")

        elif "TOKEN" in request and auth.verify_token(request['TOKEN']):

            # формирует очередь сообщений
            if ACTION in request and request[ACTION] == MESSAGE and \
                    SENDER in request and DESTINATION in request and \
                    MESSAGE_TEXT in request and TIME in request:
                message = manager.message_manager.create_message(request)
                responce = {
                    ACTION: MESSAGE,
                    SENDER: message[SENDER],
                    DESTINATION: message[DESTINATION],
                    MESSAGE_TEXT: message[MESSAGE_TEXT],
                    "CREATE_AT": message["CREATE_AT"],
                    "ID" : message["ID"]
                }
                send_message(names[message[SENDER]], responce)
                if message[DESTINATION] in names and names[message[DESTINATION]] in clients_list:
                    send_message(names[message[DESTINATION]], responce)
                    print(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                          f'от пользователя {message[DESTINATION]}.')
                    server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                                       f'от пользователя {message[SENDER]}.')
                elif message[DESTINATION] in names and names[message[SENDER]] not in clients_list:
                    print(f"ConnectionError")
                    raise ConnectionError
                else:
                    print(f"ConnectionError")
                    server_logger.error(
                        f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                        f'отправка сообщения невозможна.')
                return



            if ACTION in request and request[ACTION] == 'MESSAGE_IN_GROUP' and \
                    SENDER in request and 'GROUP' in request and \
                    MESSAGE_TEXT in request and TIME in request:
                responce, users = manager.message_manager.create_message_in_group(request)
                for user in users:
                    if user.name in names and names[user.name] in clients_list:
                        send_message(names[user.name], responce)
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

                response_from, response_to = manager.quary_manager.accept_query(request)
                send_message(sock, response_to)
                print(f"Server responce accept query{response_to}")
                if request['FROM_USERNAME'] in names and names[request['FROM_USERNAME']] in clients_list:
                    send_message(names[request['FROM_USERNAME']], response_from)
                    print(f"Server accept query{response_from}")
                return

            elif ACTION in request and request[ACTION] == 'GET_FRIEND_GROUP' and \
                    'USER' in request:
                response = manager.user_manager.get_friend(request)
                response['GROUPS'] = manager.group_manager.groups_by_user(request)['GROUPS']
                send_message(sock, response)
                print(f"Server responce get friends{response}")
                return

            elif ACTION in request and request[ACTION] == 'CREATE_GROUP' and \
                    'ADMIN' in request and 'NAME' in request:
                response = manager.group_manager.create_group(request)
                send_message(sock, response)
                print(f"Server responce create group{response}")
                return


            elif ACTION in request and request[ACTION] == 'GROUPS_BY_USER' and \
                    'USER' in request:
                response = manager.group_manager.groups_by_user(request)
                send_message(sock, response)
                print(f"Server responce group by user{response}")
                return

            elif ACTION in request and request[ACTION] == 'OPEN_GROUP' and \
                    'USER' in request and 'NAME' in request:
                response = manager.group_manager.open_group(request)
                send_message(sock, response)
                print(f"Server responce open group{response}")
                return


            elif ACTION in request and request[ACTION] == 'GET_USERS_IN_GROUPS' and \
                    'USER' in request and 'GROUP' in request:
                response = manager.group_manager.get_users_in_group(request)
                send_message(sock, response)
                print(f"Server responce get users in group{response}")
                return

            elif ACTION in request and request[ACTION] == 'CLEAR_ADD_IN_GROUP':
                responce = {
                    ACTION: 'CLEAR_ADD_IN_GROUP'
                }
                send_message(sock, responce)
                return



            elif ACTION in request and request[ACTION] == 'ADD_IN_GROUP' and \
                    'USER' in request and 'GROUP' in request:
                response = manager.group_manager.add_in_group(request)
                send_message(sock, response)
                if response['USER'] in names and names[response['USER']] in clients_list:
                    response[ACTION] = "ADDED_IN_GROUP"
                    send_message(names[response['USER']], response)
                print(f"Server responce add in group{response}")
                return

            elif ACTION in request and request[ACTION] == 'DELETE_FROM_GROUP' and \
                    'USER' in request and 'GROUP' in request:
                response = manager.group_manager.delete_from_group(request)
                send_message(sock, response)
                if response['USER'] in names and names[response['USER']] in clients_list:
                    response[ACTION] = "DELETED_FROM_GROUP"
                    send_message(names[response['USER']], response)
                print(f"Server responce delete from group{response}")
                return

            elif ACTION in request and request[ACTION] == 'ADD_IN_ADMIN' and \
                    'USER' in request and 'GROUP' in request:
                response = manager.group_manager.add_in_admin(request)
                send_message(sock, response)
                if response['USER'] in names and names[response['USER']] in clients_list:
                    response[ACTION] = "ADDED_IN_ADMIN"
                    send_message(names[response['USER']], response)
                print(f"Server responce add in group{response}")
                return


            elif ACTION in request and request[ACTION] == 'DELETE_ADMIN' and \
                    'USER' in request and 'GROUP' in request:
                response = manager.group_manager.delete_admin(request)
                send_message(sock, response)
                if response['USER'] in names and names[response['USER']] in clients_list:
                    response[ACTION] = "DELETED_ADMIN"
                    send_message(names[response['USER']], response)
                print(f"Server responce add in group{response}")
                return

            elif ACTION in request and request[ACTION] == 'DELETE_MESSAGE' and \
                    'MESSAGE_ID' in request:
                response = manager.message_manager.delete_message(request)
                for user in response['USERS']:
                    if user['NAME'] in names and names[user['NAME']] in clients_list:
                        send_message(names[user['NAME']], response)
                return
            elif ACTION in request and request[ACTION] == 'UPDATE_MESSAGE' and \
                    'MESSAGE_ID' in request and 'UPDATE_TEXT' in request:
                response = manager.message_manager.update_message(request)
                for user in response['USERS']:
                    if user['NAME'] in names and names[user['NAME']] in clients_list:
                        send_message(names[user['NAME']], response)
                        print(f"Server responce {response}")
                return

            elif ACTION in request and request[ACTION] == 'SEARCH_MESSAGE' and \
                    'SEARCH_TEXT' in request and 'USERNAME' in request:
                response = manager.message_manager.search_message(request)
                send_message(names[request['USERNAME']], response)
                return


            # выход клиента
            elif ACTION in request and request[ACTION] == EXIT and \
                    ACCOUNT_NAME in request:
                print(f"User {request[USER][ACCOUNT_NAME]} exit")
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

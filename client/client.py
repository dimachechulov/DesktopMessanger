import sys
import json
import time
import socket
import argparse
import logging
import threading

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont

import logs.client_log_config



from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, EXIT, PREVIOUS
from configs.utils import send_message, receive_message
from decorators.decorators import my_logger

client_logger = logging.getLogger('client')

class Client:

    def __init__(self,server_addr,server_port ):
        self.server_addr = server_addr
        self.server_port =server_port
        self.sock = None
        self.user = {'name' : 'Anom'}
        self.receiver_name = None
        self.token = None
        self.connected = True
        self.selected_group = None
        self.connect_server()
    def connect_server(self):
        try:

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Соединяется с сервером
            self.sock.connect((self.server_addr, self.server_port))
        except ConnectionRefusedError:
            # client_logger.critical(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
            #                     f'запрос на подключение отклонён')
            print(f'Не удалось подключиться к серверу {self.server_addr}:{self.server_port}, '
                  f'запрос на подключение отклонён')
        else:
            pass
            # presence_msg = self.create_presence_msg()
            #
            # # Отправляет сообщение о присутствии серверу
            # send_message(self.sock, presence_msg)
            #
            # # Получает и разбирает сообщение от сервера
            # server_answer = self.parser_first_message()
            # # client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
            # print(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
            # self.connected = True

    def login_user(self, username, password):
        request = {
            ACTION : 'LOGIN',
            'USERNAME' : username,
            'PASS' : password,
        }
        try:
            send_message(self.sock, request)
            # client_logger.info(f'Запрошено сообщения с {self.receiver_name}')
        except Exception as ex:
            print(ex)
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def register_user(self, name, password, email, age):
        request = {
            ACTION: 'REGISTER',
            'USERNAME': name,
            'PASS': password,
            'EMAIL': email,
            'AGE' : age
        }
        try:
            send_message(self.sock, request)
            # client_logger.info(f'Запрошено сообщения с {self.receiver_name}')
        except Exception as ex:
            print(ex)
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def logout_user(self):
        request = {
            ACTION: 'LOGOUT',
            'NAME': self.user['name']
        }
        try:
            send_message(self.sock, request)
            # client_logger.info(f'Запрошено сообщения с {self.receiver_name}')
        except Exception as ex:
            print(ex)
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    def display_previous_message(self):
        request = {
            'TOKEN': self.token,
            ACTION: PREVIOUS,
            SENDER: self.user['name'],
            DESTINATION: self.receiver_name,
        }
        try:
            send_message(self.sock, request)
            #client_logger.info(f'Запрошено сообщения с {self.receiver_name}')
        except Exception:
            #client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def create_client_msg(self, message_str):
        """
        Формирование и отправка на сервер сообщения клиента
        :param sock: клиентский сокет
        :param account_name: строка псевдонима
        :return message_dict: словарь сообщения клиента
        """


        request = {
            'TOKEN': self.token,
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.user['name'],
            DESTINATION: self.receiver_name,
            MESSAGE_TEXT: message_str
        }
        #print(f'Сформировано сообщение: {request}')
        #client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            #print(f'Отправлено сообщение для пользователя {self.receiver_name}')
            #client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            #client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def create_client_msg_in_group(self, message_str):
        request = {
            'TOKEN': self.token,
            ACTION: "MESSAGE_IN_GROUP",
            TIME: time.time(),
            SENDER: self.user['name'],
            "GROUP" : self.selected_group,
            MESSAGE_TEXT: message_str
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # print(f'Отправлено сообщение для пользователя {self.receiver_name}')
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    # @my_logger
    def send_exit_message(self):
        """
        Формирование сообщения о выходе
        :param account_name: строка псевдонима
        :return: словарь ответа о выходе клиента
        """
        if self.user:
            request = {
                'TOKEN': self.token,
                ACTION: EXIT,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.user['name']
                }
            }

            #client_logger.debug(f'Сформировано {EXIT} сообщение для пользователя {self.user['name']}')
            send_message(self.sock, request)

    def get_user_by_name(self, name, method):
        request = {
            'TOKEN': self.token,
            ACTION: 'GET_USER_BY_NAME',
            TIME: time.time(),
            'NAME': name,
            'METHOD' : method
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    def create_query(self, to_username):
        request = {
            'TOKEN': self.token,
            ACTION: 'CREATE_QUERY',
            'FROM_USERNAME': self.user['name'],
            'TO_USERNAME': to_username,
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    def accept_query(self, from_username):
        request = {
            'TOKEN': self.token,
            ACTION: 'ACCEPT_QUERY',
            'FROM_USERNAME':from_username ,
            'TO_USERNAME': self.user['name']
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    # def get_friend_status(self, to_username):
    #     request = {
    #         'TOKEN': self.token,
    #         ACTION: 'GET_FRIEND_STATUS',
    #         'FROM_USERNAME': self.user['name'],
    #         'TO_USERNAME': to_username
    #     }
    #     print(f'Сформировано сообщение: {request}')
    #     # client_logger.debug(f'Сформировано сообщение: {message_dict}')
    #
    #     try:
    #         send_message(self.sock, request)
    #         # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
    #     except Exception as ex:
    #         print(ex)
    #         print('Потеряно соединение с сервером.')
    #         # client_logger.critical('Потеряно соединение с сервером.')
    #         sys.exit(1)


    def init_friends_group(self):
        request = {
            'TOKEN': self.token,
            ACTION: 'GET_FRIEND_GROUP',
            'USER': self.user['name'],
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def create_group(self, name):
        request = {
            'TOKEN': self.token,
            ACTION: 'CREATE_GROUP',
            'ADMIN': self.user['name'],
            'NAME' : name
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def open_group(self, name):
        request = {
            'TOKEN': self.token,
            ACTION: 'OPEN_GROUP',
            'USER': self.user['name'],
            'NAME': name
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def get_users_in_group(self, method):
        request = {
            ACTION : "GET_USERS_IN_GROUPS",
            'TOKEN': self.token,
            "GROUP" : self.selected_group,
            "USER" : self.user['name'],
            'METHOD' : method,
            'NO_ADMIN' : True
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    def groups_by_user(self):
        request = {
            'TOKEN': self.token,
            ACTION: 'GROUPS_BY_USER',
            'USER': self.user['name'],
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def add_in_group(self, username):
        request = {
            'TOKEN': self.token,
            ACTION: 'ADD_IN_GROUP',
            'USER': username,
            'GROUP' : self.selected_group
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def add_in_admin(self, name):
        request = {
            'TOKEN': self.token,
            ACTION: 'ADD_IN_ADMIN',
            'USER': name,
            'GROUP': self.selected_group
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def delete_from_admin(self, name):
        request = {
            'TOKEN': self.token,
            ACTION: 'DELETE_ADMIN',
            'USER': name,
            'GROUP': self.selected_group
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def delete_from_group(self, name):
        request = {
            'TOKEN': self.token,
            ACTION: 'DELETE_FROM_GROUP',
            'USER': name,
            'GROUP': self.selected_group
        }
        print(f'Сформировано сообщение: {request}')
        # client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, request)
            # client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            # client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)



    def __del__(self):
        if self.sock:
            self.send_exit_message()
        self.sock.close()



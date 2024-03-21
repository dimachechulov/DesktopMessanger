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
user_status=None
class Client:

    def __init__(self,server_addr,server_port ):
        self.server_addr = server_addr
        self.server_port =server_port
        self.sock = None
        self.user = None
        self.receiver_name = None
        self.token = None
        self.connected = None
        #self.connect_server()
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
            presence_msg = self.create_presence_msg()

            # Отправляет сообщение о присутствии серверу
            send_message(self.sock, presence_msg)

            # Получает и разбирает сообщение от сервера
            server_answer = self.parser_first_message()
            # client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
            print(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
            self.connected = True
    def parser_first_message(self):
        while True:
            try:
                message = receive_message(self.sock)
                print(message)
                # приветственное сообщение
                if RESPONSE in message:
                    if message[RESPONSE] == 200:
                        pass
                        # client_logger.debug(f'Получено приветственное сообщение от сервера: {message[RESPONSE]} OK')

                    elif message[RESPONSE] == 400:
                        pass
                        # client_logger.debug(f'Получено сообщение от сервера: {message[RESPONSE]} {message[ERROR]}')
                return
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                client_logger.critical(f'Потеряно соединение с сервером.')
                break
        return message
    def display_previous_message(self):
        message_dict = {
            ACTION: PREVIOUS,
            SENDER: self.user.name,
            DESTINATION: self.receiver_name,
        }
        try:
            send_message(self.sock, message_dict)
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


        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.user.name,
            DESTINATION: self.receiver_name,
            MESSAGE_TEXT: message_str
        }
        print(f'Сформировано сообщение: {message_dict}')
        #client_logger.debug(f'Сформировано сообщение: {message_dict}')

        try:
            send_message(self.sock, message_dict)
            print(f'Отправлено сообщение для пользователя {self.receiver_name}')
            #client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as ex:
            print(ex)
            print('Потеряно соединение с сервером.')
            #client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def create_presence_msg(self):
        """
        Формирование сообщения о присутствии
        :param account_name: строка псевдонима
        :return: словарь ответа о присутствии клиента
        """
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.user.name
            }
        }

        #client_logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.user_name}')
        return out

    # @my_logger
    def create_exit_message(self):
        """
        Формирование сообщения о выходе
        :param account_name: строка псевдонима
        :return: словарь ответа о выходе клиента
        """
        out = {
            ACTION: EXIT,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.user.name
            }
        }

        #client_logger.debug(f'Сформировано {EXIT} сообщение для пользователя {self.user_name}')
        return out

    def __del__(self):
        if self.sock:
            exit_msg = self.create_exit_message()
            send_message(self.sock, exit_msg)


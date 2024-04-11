import sys
import json
import time
import socket
import argparse
import logging
import threading

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont, QStandardItem

import logs.client_log_config

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, EXIT, PREVIOUS
from configs.utils import send_message, receive_message
from decorators.decorators import my_logger
from client import *

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget
from PyQt5 import QtCore


class ParserServerMessage(QThread):
    def __init__(self,ex):
        super().__init__()
        self.ex = ex

    def run(self):
        while True:
            try:
                if self.ex.client.sock is None or not self.ex.client.connected:
                    continue
                responce = receive_message(self.ex.client.sock)
                print(responce)
                # сообщение от другого клиента
                if ACTION in responce and responce[ACTION] == MESSAGE and \
                        SENDER in responce and DESTINATION in responce \
                        and MESSAGE_TEXT in responce:
                    self.ex.display_message_other_user(responce)
                    #client_logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
                # предыдущие сообщения
                elif ACTION in responce and responce[ACTION] == PREVIOUS and \
                        SENDER in responce and responce[SENDER] == self.ex.client.user["name"]:
                    self.ex.display_previous_message(responce)
                elif ACTION in responce and responce[ACTION] == 'GET_USER_BY_NAME' and \
                        'USERS' in responce:
                    self.ex.display_users_by_name(responce)

                elif ACTION in responce and responce[ACTION] == 'CREATE_QUERY':
                    self.ex.display_created_query(responce)
                elif ACTION in responce and responce[ACTION] == 'DISPLAY_QUERY':
                    self.ex.display_query(responce)
                elif ACTION in responce and responce[ACTION] == 'ACCEPT_QUERY':
                    self.ex.accept_query(responce)
                elif ACTION in responce and responce[ACTION] == 'GET_FRIEND_GROUP' and \
                        'FRIENDS' in responce:
                    self.ex.display_friend(responce)
                elif ACTION in responce and (responce[ACTION] == 'LOGIN' or responce[ACTION] == 'REGISTER'):
                    self.ex.display_login_register(responce)
                elif ACTION in responce and responce[ACTION] == 'CREATE_GROUP':
                    self.ex.display_created_group(responce)
                elif ACTION in responce and responce[ACTION] == 'OPEN_GROUP':
                    self.ex.display_open_group(responce)
                elif ACTION in responce and responce[ACTION] == 'GROUPS_BY_USER':
                    self.ex.display_group_by_user(responce)
                elif ACTION in responce and responce[ACTION] == 'ADD_IN_GROUP':
                    self.ex.display_add_user_in_group(responce)
                elif ACTION in responce and responce[ACTION] == 'ADDED_IN_GROUP':
                    self.ex.display_added_user_in_group(responce)
                elif ACTION in responce and responce[ACTION] == 'MESSAGE_IN_GROUP':
                    self.ex.display_message_other_user_in_group(responce)


                elif ACTION in responce and responce[ACTION] == 'GET_USERS_IN_GROUP':
                    self.ex.display_users_in_group(responce)
                elif ACTION in responce and responce[ACTION] == 'ADD_IN_ADMIN':
                    self.ex.display_users_add_in_admin(responce)
                elif ACTION in responce and responce[ACTION] == 'ADDED_IN_ADMIN':
                    self.ex.display_users_added_in_admin(responce)
                elif ACTION in responce and responce[ACTION] == 'DELETE_ADMIN':
                    self.ex.display_users_delete_admin(responce)
                elif ACTION in responce and responce[ACTION] == 'DELETED_ADMIN':
                    self.ex.display_users_deleted_admin(responce)

                elif ACTION in responce and responce[ACTION] == 'DELETE_FROM_GROUP':
                    self.ex.display_delete_from_group(responce)
                elif ACTION in responce and responce[ACTION] == 'DELETED_FROM_GROUP':
                    self.ex.display_deleted_from_group(responce)

                elif ACTION in responce and responce[ACTION] == 'DELETED_MESSAGE':
                    self.ex.display_deleted_message(responce)
                elif ACTION in responce and responce[ACTION] == 'UPDATED_MESSAGE':
                    self.ex.display_updated_message(responce)








                else:
                    print(f'Получено некорректное сообщение с сервера: {responce}')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError) as ex:
                #client_logger.critical(f'Потеряно соединение с сервером.')
                print("Error connection with server")
                print(ex)
                break


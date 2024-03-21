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
from client import *

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget
from PyQt5 import QtCore


class ParserServerMessage(QThread):
    def __init__(self,client,ex):
        super().__init__()
        self.client = client

        self.ex = ex

    def run(self):
        while True:
            try:
                if self.client.sock is None or not self.client.connected:
                    continue
                message = receive_message(self.client.sock)
                print(message)
                # приветственное сообщение
                if RESPONSE in message:
                    if message[RESPONSE] == 200:
                        #client_logger.debug(f'Получено приветственное сообщение от сервера: {message[RESPONSE]} OK')
                        return
                    elif message[RESPONSE] == 400:
                        #client_logger.debug(f'Получено сообщение от сервера: {message[RESPONSE]} {message[ERROR]}')
                        return

                # сообщение от другого клиента
                elif ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.client.user.name:
                    if message[SENDER] == self.client.receiver_name:
                        self.ex.main_window.chat.setText(self.ex.main_window.chat.text() +f'[{message[SENDER]}]: {message[MESSAGE_TEXT]}\n')
                        print(f'[{message[SENDER]}]: {message[MESSAGE_TEXT]}')
                    else:
                        print(f'                                  Hoвое сообщение от {message[SENDER]}')
                    #client_logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
                # предыдущие сообщения
                elif ACTION in message and message[ACTION] == PREVIOUS and \
                        SENDER in message and message[SENDER] == self.client.user.name:
                    result = (f"               chat with {self.ex.client.receiver_name}\n ")
                    for msg in message['MESSAGE_TEXT_FROM']:
                        result+=f'[you] {msg}\n'
                    for msg in message['MESSAGE_TEXT_TO']:
                        result+=f'[{message[SENDER]}] {msg}\n'
                    self.ex.main_window.chat.setText(result)



                # некорректное сообщение
                else:
                    client_logger.error(f'Получено некорректное сообщение с сервера: {message}')

            # ошибка соединения с сервером
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError) as ex:
                #client_logger.critical(f'Потеряно соединение с сервером.')
                print(f"ERRRORR")
                print(ex)
                break


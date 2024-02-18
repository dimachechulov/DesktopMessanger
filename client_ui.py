# подключаем библиотеки

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


user_status=None
def onBtnClick():
    print("Hy Button is clicked!")


class MyFunctionThread(QThread):
    def __init__(self,sock, user_name,ex):
        super().__init__()
        self.sock=sock
        self.user_name = user_name

        self.ex = ex

    def run(self):
        while True:
            try:
                message = receive_message(self.sock)

                # приветственное сообщение
                if RESPONSE in message:
                    if message[RESPONSE] == 200:
                        client_logger.debug(f'Получено приветственное сообщение от сервера: {message[RESPONSE]} OK')
                        return f'{message[RESPONSE]} OK'
                    elif message[RESPONSE] == 400:
                        client_logger.debug(f'Получено сообщение от сервера: {message[RESPONSE]} {message[ERROR]}')
                        return f'{message[RESPONSE]} {message[ERROR]}'

                # сообщение от другого клиента
                elif ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.user_name:
                    if message[SENDER] == user_status:
                        self.ex.chat.setText(self.ex.chat.text() +f'[{message[SENDER]}]: {message[MESSAGE_TEXT]}\n')
                        print(f'[{message[SENDER]}]: {message[MESSAGE_TEXT]}')
                    else:
                        print(f'                                  Hoвое сообщение от {message[SENDER]}')
                    client_logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
                # предыдущие сообщения
                elif ACTION in message and message[ACTION] == PREVIOUS and \
                        SENDER in message and message[SENDER] == self.user_name:
                    result = (f"               chat with {self.ex.receiver_name}\n ")
                    for msg in message['messages']:
                        if self.user_name == msg[SENDER]:
                            result+=f'[you] {msg[MESSAGE_TEXT]}\n'
                        else:
                            result+=f'[{msg[SENDER]}] {msg[MESSAGE_TEXT]}'
                    self.ex.chat.setText(result)



                # некорректное сообщение
                else:
                    client_logger.error(f'Получено некорректное сообщение с сервера: {message}')

            # ошибка соединения с сервером
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                client_logger.critical(f'Потеряно соединение с сервером.')
                break


class MyApp(QWidget):
    def __init__(self,sock, user_name):
        super().__init__()
        self.sock=sock
        self.user_name=user_name
        self.receiver_name=None
        self.initUI()

    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")
        # Label Text
        self.chat = QLabel(self)
        self.chat.setText("")
        self.chat.move(5, 5)
        self.chat.resize(400, 500)
        self.chat.setFont(QFont('Arial', 25))
        self.chat.setAlignment(QtCore.Qt.AlignRight)
        self.chat.setStyleSheet("background-color: grey")
        self.btn_send_message = QPushButton(self)
        self.btn_send_message.setText("Отправить сообщение")
        self.btn_send_message.move(5, 505)
        self.btn_send_message.resize(140, 50)
        self.btn_send_message.clicked.connect(self.create_client_msg)
        self.tb_send_message = QLineEdit(self)
        self.tb_send_message.move(150, 505)
        self.tb_send_message.resize(250, 50)
        self.btn_change_chat = QPushButton(self)
        self.btn_change_chat.setText("Сменить чат")
        self.btn_change_chat.move(405, 5)
        self.btn_change_chat.resize(250, 40)
        self.btn_change_chat.clicked.connect(self.change_chat)
        self.tb_change_chat = QLineEdit(self)
        self.tb_change_chat.move(405, 40)
        self.tb_change_chat.resize(250, 50)
        self.name = QLabel(self)
        self.name.setText(f"You name is {self.user_name}")
        self.name.move(410, 400)
        self.name.resize(200, 40)
        self.name.setFont(QFont('Arial', 16))



    def onBtnClick(self):
        print("Okeyyy")

    def change_chat(self):
        global user_status
        self.chat.setText(f"               chat with {self.tb_change_chat.text()}\n ")

        self.receiver_name=self.tb_change_chat.text()
        display_previous_message(self.sock,self.user_name,self.receiver_name)
        user_status = self.receiver_name

    #GOTOLCLIENT
    def display_previous_message(self, sock, account_name, receiver_name):
        message_dict = {
            ACTION: PREVIOUS,
            SENDER: account_name,
            DESTINATION: receiver_name,
        }
        try:
            send_message(sock, message_dict)
            client_logger.info(f'Запрошено сообщения с {receiver_name}')
        except Exception:
            client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)
    def create_client_msg(self):
        """
        Формирование и отправка на сервер сообщения клиента
        :param sock: клиентский сокет
        :param account_name: строка псевдонима
        :return message_dict: словарь сообщения клиента
        """

        message_str = self.tb_send_message.text()
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.user_name,
            DESTINATION: self.receiver_name,
            MESSAGE_TEXT: message_str
        }
        client_logger.debug(f'Сформировано сообщение: {message_dict}')
        self.chat.setText(self.chat.text() + f'[you]: {message_str}\n')
        try:
            send_message(self.sock, message_dict)
            client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception:
            client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)
def main():
    # Получает ip-адрес, порт сервера, режим клиента из командной строки
    server_addr, server_port, client_name = parse_cmd_arguments()
    all_messages = []
    global user_status  # none if you choose friend or name of friend which chose
    user_status = None
    client_name = input('Введите имя пользователя: ')

    client_logger.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_addr}, порт: {server_port}, имя пользователя: {client_name}')
    print(f'Запущен клиент с парамертами: '
          f'адрес сервера: {server_addr}, порт: {server_port}, имя пользователя: {client_name}')

    # Начало работы, приветственное сообщение
    try:
        # Создается TCP-сокет клиента
        client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Соединяется с сервером
        client_tcp.connect((server_addr, server_port))

        # Формирует сообщение о присутствии
        presence_msg = create_presence_msg(client_name)

        # Отправляет сообщение о присутствии серверу
        send_message(client_tcp, presence_msg)

        # Получает и разбирает сообщение от сервера
        server_answer = parse_server_msg(client_tcp, client_name, user_status)

        client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
        print(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')

    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную json-строку')
        print('Не удалось декодировать полученную json-строку')
        sys.exit(1)

    except ConnectionRefusedError:
        client_logger.critical(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
                               f'запрос на подключение отклонён')
        print(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
              f'запрос на подключение отклонён')

    # Обмен сообщениями
    else:
        app = QApplication(sys.argv)
        ex = MyApp(client_tcp, client_name)
        ex.show()
        worker = MyFunctionThread(client_tcp, client_name,ex)
        worker.start()
        sys.exit(app.exec_())




main()

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
from PyQt5 import QtGui
from sqlalchemy.exc import DataError

import logs.client_log_config
from auth import AuthService
from client.ParserServerMessage import ParserServerMessage

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, EXIT, PREVIOUS
from configs.utils import send_message, receive_message
from decorators.decorators import my_logger

from client.client import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QStackedWidget, \
    QVBoxLayout
from PyQt5 import QtCore

from configs.utils import parse_cmd_arguments


class LoginWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Регистрация пользователя')
        self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login_click)

        self.go_to_login_button = QPushButton('У меня нет аккаунта')
        self.go_to_login_button.clicked.connect(self.go_to_register)
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.go_to_login_button)
        self.setLayout(layout)

    def login_click(self):
        username = self.username_input.text()
        password = self.password_input.text()


        try:
            self.client.token,  self.client.user  =  self.reg_service.login_user(username, password)
            self.client.connect_server()
        except ValueError as err:
            print(err.args)
            self.error_label.setText(err.args[0])
            return
        except DataError as err:
            print(err.args)
            self.error_label.setText("Err input in fields")
            return
        except Exception as ex:
            print(ex.args)
            return
        self.stacked_widget.setCurrentIndex(2)

    def go_to_register(self):
        self.stacked_widget.setCurrentIndex(0)



class RegistrationWidget(QWidget):
    def __init__(self, stacked_widget, client):
        self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Регистрация пользователя')
        self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()

        self.age_label = QLabel('Возраст:')
        self.age_input = QLineEdit()

        self.register_button = QPushButton('Зарегистрироваться')
        self.register_button.clicked.connect(self.register_click)


        self.go_to_login_button = QPushButton('У меня есть уже аккаунт')
        self.go_to_login_button.clicked.connect(self.go_to_login)
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.go_to_login_button)
        self.setLayout(layout)

    def register_click(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        age = self.age_input.text()

        try:
            self.client.token,  self.client.user = self.reg_service.register_user(username,password, email, age)
            self.client.connect_server()
        except ValueError as err:
            print(err.args)
            self.error_label.setText(err.args[0])
            return
        except DataError as err:
            print(err.args)
            self.error_label.setText("Err input in fields")
            return
        except Exception as ex:
            print(ex.args)
            return
        self.stacked_widget.setCurrentIndex(2)

    def go_to_login(self):
        self.stacked_widget.setCurrentIndex(1)


class MyApp(QWidget):
    def __init__(self, stacked_widget, client):

        super().__init__()
        self.stacked_widget = stacked_widget
        self.client = client
        self.initUI()

    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")
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
        if self.client.user:
            self.name.setText(f"You name is {self.client.user.name}")
        else:
            self.name.setText(f"You name is anom")
        self.name.move(410, 400)
        self.name.resize(200, 40)
        self.name.setFont(QFont('Arial', 16))
        self.button2 = QPushButton(self)
        self.button2.setText("TEmp")
        self.button2.move(405, 205)
        self.button2.resize(250, 40)
        self.button2.clicked.connect(self.show_page1)



    def create_client_msg(self):
        message_str = self.tb_send_message.text()
        self.chat.setText(self.chat.text() + f'[you]: {message_str}\n')
        self.client.create_client_msg(message_str)
    def change_chat(self):
        self.chat.setText(f"               chat with {self.tb_change_chat.text()}\n ")
        self.client.receiver_name = self.tb_change_chat.text()
        self.client.display_previous_message()

    def show_page1(self):
        self.stacked_widget.setCurrentIndex(2)



class MainWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.stacked_widget = QStackedWidget()
        self.page1 = RegistrationWidget(self.stacked_widget, client)
        self.page2 = LoginWidget(self.stacked_widget, client)
        self.main_window = MyApp(self.stacked_widget, client)

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.main_window)
        self.setCentralWidget(self.stacked_widget)



def main():
    # Получает ip-адрес, порт сервера, режим клиента из командной строки
    server_addr, server_port, client_name = parse_cmd_arguments()
    app = QApplication(sys.argv)
    client = Client(server_addr, server_port)
    ex = MainWindow(client)
    ex.show()
    worker = ParserServerMessage(client,ex)
    worker.start()
    sys.exit(app.exec_())




main()

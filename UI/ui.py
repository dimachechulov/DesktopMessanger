# подключаем библиотеки
import datetime
import sys
import json
import time
import socket
import argparse
import logging
import threading

from PyQt5.QtCore import QThread, QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from sqlalchemy.exc import DataError

import logs.client_log_config

from client.ParserServerMessage import ParserServerMessage

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, EXIT, PREVIOUS
from configs.utils import send_message, receive_message
from decorators.decorators import my_logger

from client.client import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QStackedWidget, \
    QVBoxLayout, QTextBrowser, QListView
from PyQt5 import QtCore

from configs.utils import parse_cmd_arguments
from pages.LoginPage import LoginWidget
from pages.MainPage import MyApp
from pages.RegisterPage import RegistrationWidget


class MainWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.stacked_widget = QStackedWidget()
        self.main_window = MyApp(self.stacked_widget, self.client)
        self.reg_window = RegistrationWidget(self.stacked_widget, client, self.main_window)
        self.login_page = LoginWidget(self.stacked_widget, client, self.main_window)
        self.stacked_widget.addWidget(self.reg_window)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.main_window)
        self.setCentralWidget(self.stacked_widget)

    def display_message_other_user(self, responce):
        self.main_window.display_message_other_user(responce)

    def display_previous_message(self, responce):
        self.main_window.display_previous_message(responce)

    def display_users_by_name(self, responce):
        self.main_window.display_users_by_name(responce)

    def display_created_query(self, responce):
        self.main_window.display_created_qery(responce)

    def display_query(self, responce):
        self.main_window.display_query(responce)

    def accept_query(self, responce):
        self.main_window.accept_query(responce)

    def display_friend(self, responce):
        self.main_window.display_friend(responce)

    def display_login_register(self, responce):
        if 'ERROR' in responce:
            self.login_page.error_label.setText(responce["ERROR"])
        else:
            self.client.token = responce["TOKEN"]
            self.client.user = responce["USER"]
            self.main_window.initAfterLogin()
            self.stacked_widget.setCurrentIndex(2)




def main():
    # Получает ip-адрес, порт сервера, режим клиента из командной строки
    server_addr, server_port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
    app = QApplication(sys.argv)
    client = Client(server_addr, server_port)
    ex = MainWindow(client)
    ex.show()
    worker = ParserServerMessage(ex)
    worker.start()
    sys.exit(app.exec_())




main()

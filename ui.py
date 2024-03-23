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
        self.page1 = RegistrationWidget(self.stacked_widget, client, self.main_window)
        self.page2 = LoginWidget(self.stacked_widget, client, self.main_window)


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
    worker = ParserServerMessage(ex)
    worker.start()
    sys.exit(app.exec_())




main()

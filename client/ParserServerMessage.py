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
                # приветственное сообщение
                if RESPONSE in responce:
                    if responce[RESPONSE] == 200:
                        #client_logger.debug(f'Получено приветственное сообщение от сервера: {message[RESPONSE]} OK')
                        return
                    elif responce[RESPONSE] == 400:
                        #client_logger.debug(f'Получено сообщение от сервера: {message[RESPONSE]} {message[ERROR]}')
                        return

                # сообщение от другого клиента
                elif ACTION in responce and responce[ACTION] == MESSAGE and \
                        SENDER in responce and DESTINATION in responce \
                        and MESSAGE_TEXT in responce and responce[DESTINATION] == self.ex.client.user.name:
                    if responce[SENDER] == self.ex.client.receiver_name:
                        self.ex.main_window.chat.append(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
                        print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
                    else:
                        print(f'                                  Hoвое сообщение от {responce[SENDER]}')
                    #client_logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
                # предыдущие сообщения
                elif ACTION in responce and responce[ACTION] == PREVIOUS and \
                        SENDER in responce and responce[SENDER] == self.ex.client.user.name:
                    result=""
                    messages = responce['MESSAGE']
                    for index in range(len(messages)):
                        if messages[index][SENDER] == self.ex.client.user.id:
                            result += f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'
                        else:
                            result+=f'{messages[index]["CREATE_AT"]}[{responce[SENDER]}] {messages[index]["CONTENT"]}'
                        if index +1  != len(messages):
                            result +='\n'
                    try:
                        self.ex.main_window.chat.append(result)
                        if responce['STATUS'] == 'SENTED_QUIRY':
                            self.ex.main_window.btn_add_friend.setEnabled(False)
                            self.ex.main_window.btn_add_friend.setVisible(True)
                            self.ex.main_window.btn_add_friend.setText('Query to friend\nsuccessfully sent')
                        elif responce['STATUS'] == 'TO_HE_SENTED_QUIRY':
                            self.ex.main_window.btn_add_friend.setVisible(True)
                            self.ex.main_window.btn_add_friend.setEnabled(True)
                            self.ex.main_window.btn_add_friend.setText('Accept')
                        elif responce['STATUS'] == 'FRIEND':
                            self.ex.main_window.btn_add_friend.setVisible(False)
                        elif responce['STATUS'] == 'NOTHING':
                            self.ex.main_window.btn_add_friend.setVisible(True)
                            self.ex.main_window.btn_add_friend.setEnabled(True)
                            self.ex.main_window.btn_add_friend.setText('Add Friend')
                    except Exception as ex:
                        print(ex)

                elif ACTION in responce and responce[ACTION] == 'GET_USER_BY_NAME' and \
                        'USERS' in responce:
                    self.ex.main_window.model.clear()
                    self.ex.main_window.listUsers.setModel(self.ex.main_window.model)
                    self.ex.main_window.listUsers.setVisible(True)
                    self.ex.main_window.lb_search_users.setVisible(True)
                    for user in responce['USERS']:
                        if user['NAME'] != self.ex.client.user.name:
                            self.ex.main_window.model.appendRow(QStandardItem(user['NAME']))

                elif ACTION in responce and responce[ACTION] == 'CREATE_QUERY':
                    if responce['CREATED']:
                        self.ex.main_window.btn_add_friend.setText('Query to friend\nsuccessfully sent')
                        self.ex.main_window.btn_add_friend.setEnabled(False)

                elif ACTION in responce and responce[ACTION] == 'DISPLAY_QUERY':
                    if responce['FROM_USERNAME'] == self.ex.client.receiver_name:
                        self.ex.main_window.btn_add_friend.setText('Accept')

                elif ACTION in responce and responce[ACTION] == 'ACCEPT_QUERY':
                    self.ex.main_window.btn_add_friend.setVisible(False)
                    self.ex.main_window.modelFriend.appendRow(QStandardItem(responce['FRIEND']))


                elif ACTION in responce and responce[ACTION] == 'GET_FRIEND' and \
                        'FRIENDS' in responce:
                    for friend in responce['FRIENDS']:
                        self.ex.main_window.modelFriend.appendRow(QStandardItem(friend['NAME']))






                else:
                    print(f'Получено некорректное сообщение с сервера: {responce}')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError) as ex:
                #client_logger.critical(f'Потеряно соединение с сервером.')
                print("Error connection with server")
                print(ex)
                break


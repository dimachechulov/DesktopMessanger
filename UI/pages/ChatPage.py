from datetime import datetime

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QListView
from PyQt5 import QtCore

from configs.default import SENDER, MESSAGE_TEXT, DESTINATION


class ChatWidget(QWidget):
    def __init__(self, stacked_widget, client):

        super().__init__()
        self.stacked_widget = stacked_widget
        self.client = client
        self.initUI()


    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")

        self.chat = QTextBrowser(self)
        self.chat.setText("")
        self.chat.move(5, 5)
        self.chat.resize(610, 700)
        self.chat.setFont(QFont('Arial', 25))
        self.chat.setAlignment(QtCore.Qt.AlignRight)
        self.chat.setStyleSheet("background-color: grey")
        self.chat.setObjectName('chat')


        self.btn_send_message = QPushButton(self)
        self.btn_send_message.setText("Отправить сообщение")
        self.btn_send_message.move(5, 705)
        self.btn_send_message.resize(140, 50)
        self.btn_send_message.clicked.connect(self.create_client_msg)

        self.tb_send_message = QLineEdit(self)
        self.tb_send_message.move(145, 705)
        self.tb_send_message.resize(470, 50)

        self.btn_add_friend = QPushButton(self)
        self.btn_add_friend.move(615, 5)
        self.btn_add_friend.resize(140, 50)
        self.btn_add_friend.setText("Add Friend")
        self.btn_add_friend.clicked.connect(self.create_query)
        self.btn_add_friend.setVisible(False)

        self.btn_add_in_group = QPushButton(self)
        self.btn_add_in_group.move(615, 5)
        self.btn_add_in_group.resize(140, 50)
        self.btn_add_in_group.setText("Add in Group")
        self.btn_add_in_group.clicked.connect(self.add_in_group)
        self.btn_add_in_group.setVisible(False)

        self.btn_add_in_admin = QPushButton(self)
        self.btn_add_in_admin.move(615, 55)
        self.btn_add_in_admin.resize(140, 50)
        self.btn_add_in_admin.setText("Add in Admins")
        self.btn_add_in_admin.clicked.connect(self.add_in_admin)
        self.btn_add_in_admin.setVisible(False)

        self.btn_delete_from_group = QPushButton(self)
        self.btn_delete_from_group.move(615, 105)
        self.btn_delete_from_group.resize(140, 50)
        self.btn_delete_from_group.setText("Delete from chat")
        self.btn_delete_from_group.clicked.connect(self.delete_from_group)
        self.btn_delete_from_group.setVisible(False)

        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setText("Выйти")
        self.btn_cancel.move(660, 750)
        self.btn_cancel.resize(140, 50)
        self.btn_cancel.clicked.connect(self.cancel)



    def init_friends(self):
        self.client.init_friends()

    def create_query(self):
        if self.btn_add_friend.text() == 'Add Friend':
            self.client.create_query(self.client.receiver_name)
        else:
            self.client.accept_query(self.client.receiver_name)

    def accept_query(self, responce):
        self.btn_add_friend.setVisible(False)




    def add_in_group(self):
        self.stacked_widget.setCurrentIndex(4)

    def add_in_admin(self):
        self.client.get_users_in_group(method='ADD_IN_ADMIN')
        self.stacked_widget.setCurrentIndex(5)

    def delete_from_group(self):
        pass

    def create_client_msg(self):
        if self.client.receiver_name:
            message_str = self.tb_send_message.text()
            now = datetime.now().strftime("%I:%M")
            self.chat.append(f'{now}[you]: {message_str}')
            self.client.create_client_msg(message_str)
        elif self.client.selected_group:
            message_str = self.tb_send_message.text()
            now = datetime.now().strftime("%I:%M")
            self.chat.append(f'{now}[you]: {message_str}')
            self.client.create_client_msg_in_group(message_str)


    def display_message_other_user(self, responce):
        if responce[DESTINATION] == self.client.user["name"]:
            if responce[SENDER] == self.client.receiver_name:
                self.chat.append(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
                print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
            else:
                print(f'                                  Hoвое сообщение от {responce[SENDER]}')

    def display_previous_message(self, responce):
        result = f"               chat with {self.client.receiver_name}\n "
        messages = responce['MESSAGE']
        for index in range(len(messages)):
            if messages[index][SENDER] == self.client.user['id']:
                result += f'{messages[index]["CREATE_AT"]}[{responce[SENDER]}] {messages[index]["CONTENT"]}'
            else:
                result += f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'
            if index + 1 != len(messages):
                result += '\n'
        try:
            self.chat.append(result)
            if responce['STATUS'] == 'SENTED_QUIRY':
                self.btn_add_friend.setEnabled(False)
                self.btn_add_friend.setVisible(True)
                self.btn_add_friend.setText('Query to friend\nsuccessfully sent')
            elif responce['STATUS'] == 'TO_HE_SENTED_QUIRY':
                self.btn_add_friend.setVisible(True)
                self.btn_add_friend.setEnabled(True)
                self.btn_add_friend.setText('Accept')
            elif responce['STATUS'] == 'FRIEND':
                self.btn_add_friend.setVisible(False)
            elif responce['STATUS'] == 'NOTHING':
                self.btn_add_friend.setVisible(True)
                self.btn_add_friend.setEnabled(True)
                self.btn_add_friend.setText('Add Friend')
        except Exception as ex:
            print(ex)



    def display_created_query(self, responce):
        if responce['CREATED']:
            self.btn_add_friend.setText('Query to friend\nsuccessfully sent')
            self.btn_add_friend.setEnabled(False)

    def display_query(self, responce):
        if responce['FROM_USERNAME'] == self.client.receiver_name:
            self.btn_add_friend.setText('Accept')


    def display_open_group(self, responce):
        messages = responce['MESSAGES']
        result = f"               group {responce['GROUP']}\n "
        for index in range(len(messages)):
            if messages[index][SENDER] != self.client.user['name']:
                result += f'{messages[index]["CREATE_AT"]}[{messages[index][SENDER]}] {messages[index]["CONTENT"]}'
            else:
                result += f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'
            if index + 1 != len(messages):
                result += '\n'
        self.chat.append(result)
        self.client.selected_group = responce['GROUP']
        self.client.receiver_name = None
        if responce['IS_ADMIN']:
            self.btn_add_in_group.setVisible(True)
            self.btn_add_in_admin.setVisible(True)
            self.btn_delete_from_group.setVisible(True)
        else:
            self.btn_add_in_group.setVisible(False)
            self.btn_add_in_admin.setVisible(False)
            self.btn_delete_from_group.setVisible(False)

    def display_message_other_user_in_group(self, responce):
        if responce["GROUP"] == self.client.selected_group:
            self.chat.append(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
            print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
        else:
            print(f'                                  Hoвое сообщение от {responce[SENDER]}')


    def display_users_added_in_admin(self, responce):
        if self.client.selected_group == responce['GROUP']:
            self.btn_add_in_group.setVisible(True)
            self.btn_add_in_admin.setVisible(True)
            self.btn_delete_from_group.setVisible(True)




    def display_deleted_from_group(self, responce):
        if self.client.selected_group == responce['group']:
            self.chat.clear()
            self.client.selected_group = None


    def cancel(self):
        self.client.receiver_name = None
        self.client.group = None
        self.stacked_widget.setCurrentIndex(2)





# responce = {
#     ACTION: 'OPEN_GROUP',
#     'MESSAGES': messages_json,
#     'IS_ADMIN': self.db.is_admin_in_group(request['USER'], request['NAME'])
# }


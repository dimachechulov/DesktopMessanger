from datetime import datetime

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QListView
from PyQt5 import QtCore

class MyApp(QWidget):
    def __init__(self, stacked_widget, client):

        super().__init__()
        self.stacked_widget = stacked_widget
        self.client = client
        self.initUI()

    def initAfterLogin(self):

        self.init_friends()
        if self.client.user:
            self.name.setText(f"You name is {self.client.user['name']}")
        else:
            self.name.setText(f"You name is anom")
    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")

        self.chat = QTextBrowser(self)
        self.chat.setText("")
        self.chat.move(5, 5)
        self.chat.resize(550, 500)
        self.chat.setFont(QFont('Arial', 25))
        self.chat.setAlignment(QtCore.Qt.AlignRight)
        self.chat.setStyleSheet("background-color: grey")

        self.btn_add_friend = QPushButton(self)
        self.btn_add_friend.move(410, 5)
        self.btn_add_friend.resize(140,50)
        self.btn_add_friend.setText("Add Friend")
        self.btn_add_friend.clicked.connect(self.create_query)
        self.btn_add_friend.setVisible(False)

        self.btn_send_message = QPushButton(self)
        self.btn_send_message.setText("Отправить сообщение")
        self.btn_send_message.move(5, 505)
        self.btn_send_message.resize(140, 50)
        self.btn_send_message.clicked.connect(self.create_client_msg)

        self.tb_send_message = QLineEdit(self)
        self.tb_send_message.move(145, 505)
        self.tb_send_message.resize(405, 50)

        self.lb_search_users = QLabel(self)
        self.lb_search_users.move(5, 555)
        self.lb_search_users.setFont(QFont('Arial', 14))
        self.lb_search_users.setText("You Friends")

        self.listFriend = QListView(self)
        self.listFriend.move(5, 575)
        self.listFriend.resize(550,200)
        self.modelFriend = QStandardItemModel()
        self.listFriend.clicked[QModelIndex].connect(self.change_chat)
        self.listFriend.setModel(self.modelFriend)
        self.listFriend.setObjectName("listView-2")



        self.btn_change_chat = QPushButton(self)
        self.btn_change_chat.setText("Поиск чата")
        self.btn_change_chat.move(555, 5)
        self.btn_change_chat.resize(250, 40)
        self.btn_change_chat.clicked.connect(self.get_users_by_name)

        self.tb_change_chat = QLineEdit(self)
        self.tb_change_chat.move(555, 40)
        self.tb_change_chat.resize(250, 50)

        self.lb_search_users = QLabel(self)
        self.lb_search_users.move(555, 95)
        self.lb_search_users.setFont(QFont('Arial', 14))
        self.lb_search_users.setText("Result")
        self.lb_search_users.setVisible(False)

        self.listUsers = QListView(self)
        self.listUsers.move(555, 120)
        self.listUsers.resize(250, 250)
        self.listUsers.setVisible(False)
        self.model = QStandardItemModel()
        self.listUsers.clicked[QModelIndex].connect(self.change_chat)
        self.listUsers.setModel(self.model)
        self.listUsers.setObjectName("listView-1")

        self.name = QLabel(self)

        self.name.move(555, 500)
        self.name.resize(200, 40)
        self.name.setFont(QFont('Arial', 16))



    def init_friends(self):
        self.client.init_friends()

    def create_query(self):
        selected_index = self.listUsers.selectedIndexes()[0]  # Get the selected index
        to_username = self.model.itemData(selected_index)[0]
        if self.btn_add_friend.text() == 'Add Friend':
            self.client.create_query(to_username)
        else:
            self.client.accept_query(to_username)

    def create_client_msg(self):
        message_str = self.tb_send_message.text()
        now = datetime.now().strftime("%I:%M")
        self.chat.append(f'{now}[you]: {message_str}')
        self.client.create_client_msg(message_str)

    def get_users_by_name(self):
        name = self.tb_change_chat.text()
        self.client.get_user_by_name(name)
    def change_chat(self, index):

        if self.model.itemFromIndex(index):
            self.client.receiver_name = self.model.itemFromIndex(index).text()
            self.chat.setText(f"               chat with {self.model.itemFromIndex(index).text()}\n ")
        else:
            self.client.receiver_name = self.modelFriend.itemFromIndex(index).text()
            self.chat.setText(f"               chat with {self.modelFriend.itemFromIndex(index).text()}\n ")
        self.client.display_previous_message()

    def show_page1(self):
        self.stacked_widget.setCurrentIndex(2)
from datetime import datetime

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QListView
from PyQt5 import QtCore

from configs.default import SENDER, MESSAGE_TEXT, DESTINATION


class MyApp(QWidget):
    def __init__(self, stacked_widget, client):

        super().__init__()
        self.stacked_widget = stacked_widget
        self.client = client
        self.initUI()

    def initAfterLogin(self):

        self.init_friends_group()
        # self.init_group()
        if self.client.user:
            self.name.setText(f"You name is {self.client.user['name']}")
        else:
            self.name.setText(f"You name is anom")
    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")

        # self.chat = QTextBrowser(self)
        # self.chat.setText("")
        # self.chat.move(5, 5)
        # self.chat.resize(550, 500)
        # self.chat.setFont(QFont('Arial', 25))
        # self.chat.setAlignment(QtCore.Qt.AlignRight)
        # self.chat.setStyleSheet("background-color: grey")
        # self.chat.setObjectName('chat')
        # self.btn_add_friend = QPushButton(self)
        # self.btn_add_friend.move(410, 5)
        # self.btn_add_friend.resize(140,50)
        # self.btn_add_friend.setText("Add Friend")
        # self.btn_add_friend.clicked.connect(self.create_query)
        # self.btn_add_friend.setVisible(False)
        #
        # self.btn_add_in_group = QPushButton(self)
        # self.btn_add_in_group.move(410, 5)
        # self.btn_add_in_group.resize(140, 50)
        # self.btn_add_in_group.setText("Add in Group")
        # self.btn_add_in_group.clicked.connect(self.add_in_group)
        # self.btn_add_in_group.setVisible(False)
        #
        # self.btn_add_in_admin = QPushButton(self)
        # self.btn_add_in_admin.move(410, 55)
        # self.btn_add_in_admin.resize(140, 50)
        # self.btn_add_in_admin.setText("Add in Admins")
        # self.btn_add_in_admin.clicked.connect(self.add_in_admin)
        # self.btn_add_in_admin.setVisible(False)

        # self.btn_delete_from_group = QPushButton(self)
        # self.btn_delete_from_group.move(410, 105)
        # self.btn_delete_from_group.resize(140, 50)
        # self.btn_delete_from_group.setText("Delete from chat")
        # self.btn_delete_from_group.clicked.connect(self.delete_from_group)
        # self.btn_delete_from_group.setVisible(False)
        #
        # self.btn_send_message = QPushButton(self)
        # self.btn_send_message.setText("Отправить сообщение")
        # self.btn_send_message.move(5, 505)
        # self.btn_send_message.resize(140, 50)
        # self.btn_send_message.clicked.connect(self.create_client_msg)
        #
        # self.tb_send_message = QLineEdit(self)
        # self.tb_send_message.move(145, 505)
        # self.tb_send_message.resize(405, 50)

        self.lb_search_users = QLabel(self)
        self.lb_search_users.move(5, 455)
        self.lb_search_users.setFont(QFont('Arial', 14))
        self.lb_search_users.setText("You Friends")

        self.listFriend = QListView(self)
        self.listFriend.move(5, 475)
        self.listFriend.resize(550,300)
        self.modelFriend = QStandardItemModel()
        self.listFriend.clicked[QModelIndex].connect(self.change_chat)
        self.listFriend.setModel(self.modelFriend)
        self.listFriend.setObjectName("listView-2")
        self.name_label = QLabel(self)
        self.name_label.setText('Ваши группы:')
        self.name_label.move(5, 5)
        self.name_label.setFont(QFont('Arial', 14))
        self.name_label.setText("You Groups")
        self.listGroup = QListView(self)
        self.listGroup.move(5, 25)
        self.listGroup.resize(550, 430)
        self.modelGroup = QStandardItemModel()
        self.listGroup.clicked[QModelIndex].connect(self.open_group)
        self.listGroup.setModel(self.modelGroup)
        self.listGroup.setObjectName("listView-2")

        #self.btnOpenUserGroup.clicked.connect(self.open_user_group)
        self.btnCreateGroup = QPushButton(self)
        self.btnCreateGroup.move(555, 725)
        self.btnCreateGroup.resize(200, 50)
        self.btnCreateGroup.setText("Create Group")
        self.btnCreateGroup.clicked.connect(self.create_group)






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



    def init_friends_group(self):
        self.client.init_friends_group()

    def create_query(self):
        selected_index = self.listUsers.selectedIndexes()[0]  # Get the selected index
        to_username = self.model.itemData(selected_index)[0]
        if self.btn_add_friend.text() == 'Add Friend':
            self.client.create_query(to_username)
        else:
            self.client.accept_query(to_username)

    def create_group(self):
        self.stacked_widget.setCurrentIndex(3)

    def init_group(self):
        #self.chat.clear()
        self.client.groups_by_user()
        self.stacked_widget.setCurrentIndex(4)

    def open_group(self, index):
        self.stacked_widget.setCurrentIndex(6)
        name = self.modelGroup.itemFromIndex(index).text()
        self.client.selected_group = name
        self.client.open_group(name)

    def add_in_group(self):
        self.stacked_widget.setCurrentIndex(5)



    def delete_from_group(self):
        pass


    def get_users_by_name(self):
        name = self.tb_change_chat.text()
        self.client.get_user_by_name(name, method="ToOpenChat")
    def change_chat(self, index):
        self.stacked_widget.setCurrentIndex(6)
        if self.model.itemFromIndex(index):
            self.client.receiver_name = self.model.itemFromIndex(index).text()
        else:
            self.client.receiver_name = self.modelFriend.itemFromIndex(index).text()
        self.client.display_previous_message()



    # def display_message_other_user(self, responce):
    #     if responce[DESTINATION] == self.client.user["name"]:
    #         if responce[SENDER] == self.client.receiver_name:
    #             self.chat.append(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
    #             print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
    #         else:
    #             print(f'                                  Hoвое сообщение от {responce[SENDER]}')

    # def display_previous_message(self, responce):
    #     result = ""
    #     messages = responce['MESSAGE']
    #     for index in range(len(messages)):
    #         if messages[index][SENDER] == self.client.user['id']:
    #             result += f'{messages[index]["CREATE_AT"]}[{responce[SENDER]}] {messages[index]["CONTENT"]}'
    #         else:
    #             result += f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'
    #         if index + 1 != len(messages):
    #             result += '\n'
    #     try:
    #         self.chat.append(result)
    #         if responce['STATUS'] == 'SENTED_QUIRY':
    #             self.btn_add_friend.setEnabled(False)
    #             self.btn_add_friend.setVisible(True)
    #             self.btn_add_friend.setText('Query to friend\nsuccessfully sent')
    #         elif responce['STATUS'] == 'TO_HE_SENTED_QUIRY':
    #             self.btn_add_friend.setVisible(True)
    #             self.btn_add_friend.setEnabled(True)
    #             self.btn_add_friend.setText('Accept')
    #         elif responce['STATUS'] == 'FRIEND':
    #             self.btn_add_friend.setVisible(False)
    #         elif responce['STATUS'] == 'NOTHING':
    #             self.btn_add_friend.setVisible(True)
    #             self.btn_add_friend.setEnabled(True)
    #             self.btn_add_friend.setText('Add Friend')
    #     except Exception as ex:
    #         print(ex)

    def display_users_by_name(self, responce):
        self.model.clear()
        self.listUsers.setModel(self.model)
        self.listUsers.setVisible(True)
        self.lb_search_users.setVisible(True)
        for user in responce['USERS']:
            if user['NAME'] != self.client.user["name"]:
                self.model.appendRow(QStandardItem(user['NAME']))

    # def display_created_query(self, responce):
    #     if responce['CREATED']:
    #         self.ex.main_window.btn_add_friend.setText('Query to friend\nsuccessfully sent')
    #         self.ex.main_window.btn_add_friend.setEnabled(False)

    # def display_query(self, responce):
    #     if responce['FROM_USERNAME'] == self.ex.client.receiver_name:
    #         self.btn_add_friend.setText('Accept')

    def display_group_by_user(self, responce):
        self.modelGroup.clear()
        for group in responce['GROUPS']:
            self.modelGroup.appendRow(QStandardItem(group['NAME']))

    def display_friend(self, responce):
        self.modelGroup.clear()
        for group in responce['GROUPS']:
            self.modelGroup.appendRow(QStandardItem(group['NAME']))
        for friend in responce['FRIENDS']:
            self.modelFriend.appendRow(QStandardItem(friend['NAME']))

    # def accept_query(self, responce):
    #     self.btn_add_friend.setVisible(False)
    #     self.modelFriend.appendRow(QStandardItem(responce['FRIEND']))

    # def display_open_group(self, responce):
    #     messages = responce['MESSAGES']
    #     result = f"               group {responce['GROUP']}\n "
    #     for index in range(len(messages)):
    #         if messages[index][SENDER] != self.client.user['name']:
    #             result += f'{messages[index]["CREATE_AT"]}[{messages[index][SENDER]}] {messages[index]["CONTENT"]}'
    #         else:
    #             result += f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'
    #         if index + 1 != len(messages):
    #             result += '\n'
    #     self.stacked_widget.setCurrentIndex(2)
    #     self.chat.append(result)
    #     self.client.selected_group = responce['GROUP']
    #     self.client.receiver_name = None
    #     if responce['IS_ADMIN']:
    #         self.btn_add_in_group.setVisible(True)
    #         self.btn_add_in_admin.setVisible(True)
    #         self.btn_delete_from_group.setVisible(True)
    #     else:
    #         self.btn_add_in_group.setVisible(False)
    #         self.btn_add_in_admin.setVisible(False)
    #         self.btn_delete_from_group.setVisible(False)



        #ADD sucs message

    # responce = {
    #     ACTION: "MESSAGE_IN_GROUP",
    #     SENDER: msg.from_user,
    #     "GROUP": request['GROUP'],
    #     MESSAGE_TEXT: msg.content,
    #     "CREATE_AT": msg.created_at.strftime("%I:%M")
    # }
    # def display_message_other_user_in_group(self, responce):
    #     if responce["GROUP"] == self.client.selected_group:
    #         self.chat.append(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
    #         print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
    #     else:
    #         print(f'                                  Hoвое сообщение от {responce[SENDER]}')


    # def display_users_added_in_admin(self, responce):
    #     if self.client.selected_group == responce['GROUP']:
    #         self.btn_add_in_group.setVisible(True)
    #         self.btn_add_in_admin.setVisible(True)
    #         self.btn_delete_from_group.setVisible(True)




    # def display_deleted_from_group(self, responce):
    #     if self.client.selected_group == responce['group']:
    #         self.chat.clear()
    #         self.client.selected_group = None






# responce = {
#     ACTION: 'OPEN_GROUP',
#     'MESSAGES': messages_json,
#     'IS_ADMIN': self.db.is_admin_in_group(request['USER'], request['NAME'])
# }


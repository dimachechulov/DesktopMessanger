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
        self.selected_message = None
        self.messages = None


    def initUI(self):

        self.setGeometry(800, 800, 800, 650)
        self.setWindowTitle("Pyqt5 Tutorial")


        self.lbl_info_chat = QLabel(self)
        self.lbl_info_chat.move(240, 5)
        self.lbl_info_chat.setFont(QFont('Arial', 14))
        self.lbl_info_chat.setText("CHANGEMECHANGEME")
        self.chat = QListView(self)
        self.chat.move(5, 40)
        self.chat.resize(610, 660)
        self.modelchat = QStandardItemModel()
        self.chat.clicked[QModelIndex].connect(self.select_message)
        self.chat.setModel(self.modelchat)
        self.chat.setObjectName("listView-2")

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

        self.btn_delete_from_group = QPushButton(self)
        self.btn_delete_from_group.move(615, 55)
        self.btn_delete_from_group.resize(140, 50)
        self.btn_delete_from_group.setText("Delete from chat")
        self.btn_delete_from_group.clicked.connect(self.delete_from_group)
        self.btn_delete_from_group.setVisible(False)

        self.btn_add_in_admin = QPushButton(self)
        self.btn_add_in_admin.move(615, 105)
        self.btn_add_in_admin.resize(140, 50)
        self.btn_add_in_admin.setText("Add in Admins")
        self.btn_add_in_admin.clicked.connect(self.add_in_admin)
        self.btn_add_in_admin.setVisible(False)

        self.btn_delete_admin = QPushButton(self)
        self.btn_delete_admin.move(615, 155)
        self.btn_delete_admin.resize(140, 50)
        self.btn_delete_admin.setText("Delete from Admins")
        self.btn_delete_admin.clicked.connect(self.delete_admin)
        self.btn_delete_admin.setVisible(False)

        self.btn_delete_message = QPushButton(self)
        self.btn_delete_message.move(615, 215)
        self.btn_delete_message.resize(140, 50)
        self.btn_delete_message.setText("Delete selected message")
        self.btn_delete_message.clicked.connect(self.delete_message)
        self.btn_delete_message.setVisible(False)

        self.btn_change_message = QPushButton(self)
        self.btn_change_message.move(615, 265)
        self.btn_change_message.resize(140, 50)
        self.btn_change_message.setText("Change selected message")
        self.btn_change_message.clicked.connect(self.change_message)
        self.btn_change_message.setVisible(False)
        self.change_message_input = QLineEdit(self)
        self.change_message_input.move(615, 320)
        self.change_message_input.setFont(QFont('Arial', 14))
        self.change_message_input.setPlaceholderText("Enter changed text")
        self.change_message_input.setVisible(False)

        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setText("Выйти")
        self.btn_cancel.move(660, 750)
        self.btn_cancel.resize(140, 50)
        self.btn_cancel.clicked.connect(self.cancel)





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
        self.client.get_users_in_group(method='DELETE_FROM_CHAT')
        self.stacked_widget.setCurrentIndex(5)

    def delete_admin(self):
        self.client.get_users_in_group(method='DELETE_ADMIN')
        self.stacked_widget.setCurrentIndex(5)


    def create_client_msg(self):
        if self.client.receiver_name:
            message_str = self.tb_send_message.text()
            now = datetime.now().strftime("%I:%M")
            #self.modelchat.appendRow(QStandardItem(f'{now}[you]: {message_str}'))

            self.client.create_client_msg(message_str)
        elif self.client.selected_group:
            message_str = self.tb_send_message.text()
            now = datetime.now().strftime("%I:%M")
            #self.modelchat.appendRow(QStandardItem(f'{now}[you]: {message_str}'))
            self.client.create_client_msg_in_group(message_str)

    def select_message(self, index):
        self.selected_message = self.messages[index.row()]
        if self.selected_message[SENDER] == self.client.user['name']:
            self.btn_change_message.setVisible(True)
            self.btn_delete_message.setVisible(True)
            self.change_message_input.setVisible(True)
        else:
            self.btn_change_message.setVisible(False)
            self.btn_delete_message.setVisible(False)
            self.change_message_input.setVisible(False)

    def delete_message(self):
        self.modelchat.removeRow(self.messages.index(self.selected_message))
        self.messages.remove(self.selected_message)
        self.client.delete_message(message_id=self.selected_message["ID"])

    def change_message(self):
        updated_text = self.change_message_input.text()
        item = self.modelchat.itemFromIndex(self.modelchat.index(self.messages.index(self.selected_message),0))
        item.setText(f'{self.selected_message["CREATE_AT"]}[you]: {updated_text}')
        self.selected_message['TEXT'] = updated_text
        self.client.update_message(message_id=self.selected_message["ID"], text=updated_text)


    def display_message_other_user(self, responce):

        if responce[DESTINATION] == self.client.user["name"]:
            if responce[SENDER] == self.client.receiver_name:
                self.modelchat.appendRow(QStandardItem(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}'))
                self.messages.append({"CREATE_AT":responce["CREATE_AT"], "ID" : responce["ID"], SENDER:responce[SENDER], "TEXT": responce[MESSAGE_TEXT]})

                print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
            else:
                print(f'                                  Hoвое сообщение от {responce[SENDER]}')
        else:
            self.modelchat.appendRow(
                QStandardItem(f'{responce["CREATE_AT"]}[you]: {responce[MESSAGE_TEXT]}'))
            self.messages.append({"CREATE_AT": responce["CREATE_AT"], "ID": responce["ID"], SENDER: responce[SENDER],
                                  "TEXT": responce[MESSAGE_TEXT]})


    def display_previous_message(self, responce):
        self.btn_add_in_group.setVisible(False)
        self.btn_delete_from_group.setVisible(False)
        self.btn_delete_admin.setVisible(False)
        self.btn_add_in_admin.setVisible(False)
        self.btn_change_message.setVisible(False)
        self.btn_delete_message.setVisible(False)
        self.change_message_input.setVisible(False)
        self.lbl_info_chat.setText(f'Chat with {self.client.receiver_name}')
        messages = responce['MESSAGE']
        self.messages = []
        for index in range(len(messages)):

            if messages[index][SENDER] != self.client.user['id']:
                self.messages.append({"CREATE_AT": messages[index]["CREATE_AT"], "ID": messages[index]["ID"],
                                      SENDER: responce[DESTINATION], "TEXT": messages[index]['CONTENT']})
                self.modelchat.appendRow(QStandardItem(f'{messages[index]["CREATE_AT"]}[{responce[DESTINATION]}] {messages[index]["CONTENT"]}'))
            else:
                self.messages.append({"CREATE_AT": messages[index]["CREATE_AT"], "ID": messages[index]["ID"],
                                      SENDER: self.client.user['name'], "TEXT": messages[index]['CONTENT']})

                self.modelchat.appendRow(QStandardItem(f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'))

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




    def display_created_query(self, responce):
        if responce['CREATED']:
            self.btn_add_friend.setText('Query to friend\nsuccessfully sent')
            self.btn_add_friend.setEnabled(False)

    def display_query(self, responce):
        if responce['FROM_USERNAME'] == self.client.receiver_name:
            self.btn_add_friend.setText('Accept')


    def display_open_group(self, responce):
        self.btn_add_friend.setVisible(False)
        self.btn_change_message.setVisible(False)
        self.btn_delete_message.setVisible(False)
        self.change_message_input.setVisible(False)
        self.lbl_info_chat.setText(f'{responce["GROUP"]}')
        self.messages = []
        messages = responce['MESSAGES']
        for index in range(len(messages)):
            self.messages.append({"CREATE_AT": messages[index]["CREATE_AT"], "ID": messages[index]["ID"],
                                  SENDER: messages[index][SENDER], "TEXT": messages[index]['CONTENT']})
            if messages[index][SENDER] != self.client.user['name']:
                self.modelchat.appendRow(
                    QStandardItem(
                        f'{messages[index]["CREATE_AT"]}[{messages[index][SENDER]}] {messages[index]["CONTENT"]}'))
            else:
                self.modelchat.appendRow(
                    QStandardItem(f'{messages[index]["CREATE_AT"]}[you] {messages[index]["CONTENT"]}'))
        self.client.selected_group = responce['GROUP']
        self.client.receiver_name = None
        if responce['STATUS'] == 'OWNER':
            self.btn_add_in_group.setVisible(True)
            self.btn_add_in_admin.setVisible(True)
            self.btn_delete_from_group.setVisible(True)
            self.btn_delete_admin.setVisible(True)
        elif responce['STATUS'] == 'ADMIN':
            self.btn_add_in_group.setVisible(True)
            self.btn_delete_from_group.setVisible(True)
            self.btn_delete_admin.setVisible(False)
            self.btn_add_in_admin.setVisible(False)
        else:
            self.btn_add_in_group.setVisible(False)
            self.btn_delete_from_group.setVisible(False)
            self.btn_delete_admin.setVisible(False)
            self.btn_add_in_admin.setVisible(False)

    def display_message_other_user_in_group(self, responce):

        self.messages.append(
        {"CREATE_AT": responce["CREATE_AT"], "ID": responce["ID"], SENDER: responce[SENDER],
         "TEXT": responce[MESSAGE_TEXT]})
        if responce["GROUP"] == self.client.selected_group:
            if responce[SENDER] != self.client.user['name']:
                print(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}')
                self.modelchat.appendRow(
                    QStandardItem(f'{responce["CREATE_AT"]}[{responce[SENDER]}]: {responce[MESSAGE_TEXT]}'))
            else:
                self.modelchat.appendRow(
                    QStandardItem(f'{responce["CREATE_AT"]}[you]: {responce[MESSAGE_TEXT]}'))
                print(f'{responce["CREATE_AT"]}[you]: {responce[MESSAGE_TEXT]}')
        else:
            print(f'                                  Hoвое сообщение от {responce[SENDER]}')


    def display_users_added_in_admin(self, responce):
        if self.client.selected_group == responce['GROUP']:
            self.btn_add_in_group.setVisible(True)
            self.btn_delete_from_group.setVisible(True)

    def display_users_deleted_in_admin(self, responce):
        if self.client.selected_group == responce['GROUP']:
            self.btn_add_in_group.setVisible(False)
            self.btn_delete_from_group.setVisible(False)
            self.btn_delete_admin.setVisible(False)
            self.btn_add_in_admin.setVisible(False)


    def display_deleted_from_group(self, responce):
        if self.client.selected_group == responce['GROUP']:
            self.client.selected_group = None
            self.stacked_widget.setCurrentIndex(2)
            # add message

    def display_deleted_message(self, responce):
        msg_id = responce['MESSAGE_ID']
        list_id = None
        for id, message in enumerate(self.messages):
            if message["ID"] == msg_id:
                list_id = id
                self.messages.remove(message)
                break
        self.modelchat.removeRow(list_id)

    def display_updated_message(self, responce):
        msg_id = responce['MESSAGE_ID']
        for id, message in enumerate(self.messages):
            if message["ID"] == msg_id:
                message['TEXT'] = responce["UPDATE_TEXT"]
                item = self.modelchat.itemFromIndex(self.modelchat.index(id, 0))
                item.setText(f'{message["CREATE_AT"]}[{responce[SENDER]}]: {responce["UPDATE_TEXT"]}')
                break






    def cancel(self):
        self.client.receiver_name = None
        self.client.group = None
        self.modelchat.clear()
        self.stacked_widget.setCurrentIndex(2)





# responce = {
#     ACTION: 'OPEN_GROUP',
#     'MESSAGES': messages_json,
#     'IS_ADMIN': self.db.is_admin_in_group(request['USER'], request['NAME'])
# }


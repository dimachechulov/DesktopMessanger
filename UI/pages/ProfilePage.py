from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QListView, \
    QAbstractItemView
class ProfileWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        # self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        self.user = None
        super().__init__()
        self.InitUi()


    def InitUi(self):
        self.setWindowTitle('Профиль')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.info_label = QLabel('Информация о пользователе:')
        self.info_label.setFont(QFont('Arial', 25))
        self.friend_info_label = QLabel('Его друзья:')
        self.friend_info_label.setFont(QFont('Arial', 25))
        self.listFriend = QListView(self)
        self.listFriend.move(5, 575)
        self.listFriend.resize(550, 200)
        self.modelFriend = QStandardItemModel()
        self.listFriend.setModel(self.modelFriend)
        self.listFriend.setObjectName("listView-2")
        self.listFriend.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.group_info_label = QLabel('Его группы:')
        self.group_info_label.setFont(QFont('Arial', 25))
        self.listGroup= QListView(self)
        self.listGroup.move(5, 575)
        self.listGroup.resize(550, 200)
        self.modelGroup = QStandardItemModel()
        self.listGroup.setModel(self.modelGroup)
        self.listGroup.setObjectName("listView-2")
        self.listGroup.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.friend_info_label)
        layout.addWidget(self.listFriend)
        layout.addWidget(self.group_info_label)
        layout.addWidget(self.listGroup)
        self.setLayout(layout)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setText("Выйти")
        self.btn_cancel.move(660, 750)
        self.btn_cancel.resize(140, 50)
        self.btn_cancel.clicked.connect(self.cancel)

    def display_profile(self, response):
        self.user = response['USER']
        info_user = f'Информация о пользователе:\n Имя: {self.user["NAME"]} \nemail: {self.user["EMAIL"]} \nвозраст: {self.user["AGE"]}'
        self.info_label.setText(info_user)
        self.modelFriend.clear()
        self.modelGroup.clear()
        for friend in response['FRIENDS']:
            self.modelFriend.appendRow(QStandardItem(friend['NAME']))
        for group in response['GROUPS']:
            self.modelGroup.appendRow(QStandardItem(group['NAME']))

    def cancel(self):
        if self.client.user['name'] == self.user['NAME']:
            self.stacked_widget.setCurrentIndex(2)
        else:
            self.stacked_widget.setCurrentIndex(6)




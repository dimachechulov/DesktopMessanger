from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListView, QAbstractItemView
from sqlalchemy.exc import DataError




class AddAdminWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        # self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()
        self.method  = None


    def InitUi(self):
        self.setWindowTitle('Добавление в админы')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.info_label = QLabel('Выберите имя, того, кого хотите добавить в админы:')
        self.info_label.setFont(QFont('Arial', 25))
        self.listUser = QListView(self)
        self.listUser.move(5, 575)
        self.listUser.resize(550, 200)
        self.modelUser = QStandardItemModel()
        self.listUser.clicked[QModelIndex].connect(self.add)
        self.listUser.setModel(self.modelUser)
        self.listUser.setObjectName("listView-2")
        self.listUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.listUser)
        self.setLayout(layout)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setText("Выйти")
        self.btn_cancel.move(660, 750)
        self.btn_cancel.resize(140, 50)
        self.btn_cancel.clicked.connect(self.cancel)




    def add(self, index):
        name = self.modelUser.itemFromIndex(index).text()
        if self.info_label.text() == 'Выберите имя, того, кого хотите добавить в админы:':
            self.client.add_in_admin(name)
        elif self.info_label.text() == 'Выберите имя, того, кого хотите удалить из группы:':
            self.client.delete_from_group(name)
        elif self.info_label.text() == 'Выберите имя, того, кого хотите убрать из админов:':
            self.client.delete_from_admin(name)



    def display_users_in_group(self, responce):
        if responce['METHOD'] == 'ADD_IN_ADMIN':
            self.info_label.setText('Выберите имя, того, кого хотите добавить в админы:')
        elif responce['METHOD']=='DELETE_FROM_CHAT':
            self.info_label.setText('Выберите имя, того, кого хотите удалить из группы:')
        elif responce['METHOD'] == 'DELETE_ADMIN':
            self.info_label.setText('Выберите имя, того, кого хотите убрать из админов:')
        self.modelUser.clear()
        for user in responce['USERS']:
            self.modelUser.appendRow(QStandardItem(user['NAME']))

    def cancel(self):
        self.stacked_widget.setCurrentIndex(6)











from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListView, QAbstractItemView
from sqlalchemy.exc import DataError




class AddInGroupWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        # self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()


    def InitUi(self):
        self.setWindowTitle('Добавление в группу')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.info_label = QLabel('Введите имя, того, кого хотите добавить:')
        self.info_label.setFont(QFont('Arial', 25))
        self.user_input = QLineEdit()
        self.user_input.setFont(QFont('Arial', 25))
        self.user_input.setPlaceholderText('Enter name of user')
        self.btn_search = QPushButton('Поиск')
        self.btn_search.setFixedHeight(50)
        self.btn_search.clicked.connect(self.search)
        self.listUser = QListView(self)
        self.listUser.move(5, 575)
        self.listUser.resize(550, 200)
        self.modelUser = QStandardItemModel()
        self.listUser.clicked[QModelIndex].connect(self.add)
        self.listUser.setModel(self.modelUser)
        self.listUser.setObjectName("listView-2")
        self.listUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setText("Выйти")
        self.btn_cancel.move(660, 750)
        self.btn_cancel.resize(140, 50)
        self.btn_cancel.clicked.connect(self.cancel)
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.listUser)


        self.setLayout(layout)




    def add(self, index):
        name = self.modelUser.itemFromIndex(index).text()
        self.client.add_in_group(name)

    def search(self):
        name = self.user_input.text()
        self.client.get_user_by_name(name, method="InAddGroup")

    def display_search(self, responce):
        self.modelUser.clear()
        for user in responce['USERS']:
            self.modelUser.appendRow(QStandardItem(user['NAME']))


    def cancel(self):
        self.stacked_widget.setCurrentIndex(6)










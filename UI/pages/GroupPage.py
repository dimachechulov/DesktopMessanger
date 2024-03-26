from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListView
from sqlalchemy.exc import DataError




class GroupWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        # self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()


    def InitUi(self):
        self.setWindowTitle('Ваши группы')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.name_label = QLabel('Ваши группы:')
        self.listGroup = QListView(self)
        self.listGroup.move(5, 575)
        self.listGroup.resize(550, 200)
        self.modelGroup = QStandardItemModel()
        self.listGroup.clicked[QModelIndex].connect(self.open_group)
        self.listGroup.setModel(self.modelGroup)
        self.listGroup.setObjectName("listView-2")
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.listGroup)
        self.setLayout(layout)




    def open_group(self, index):
        name = self.modelGroup.itemFromIndex(index).text()
        self.client.open_group(name)

    def display_group_by_user(self, responce):
        self.modelGroup.clear()
        for group in responce['GROUPS']:
            self.modelGroup.appendRow(QStandardItem(group['NAME']))







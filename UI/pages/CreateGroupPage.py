from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from sqlalchemy.exc import DataError




class CreateGroupWidget(QWidget):
    def __init__(self, stacked_widget,  client):
        # self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Создание группы')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.name_label = QLabel('Название группы:')
        self.name_label.setFont(QFont('Arial', 25))
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont('Arial', 25))
        self.name_input.setPlaceholderText('Enter name of group')
        self.btn_create = QPushButton('Создать')
        self.btn_create.setFixedHeight(50)
        self.btn_create.clicked.connect(self.create)

        self.go_to_back = QPushButton('Отмена')
        self.go_to_back.setFixedHeight(50)
        self.go_to_back.clicked.connect(self.cansel)

        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.btn_create)
        layout.addWidget(self.go_to_back)

        self.setLayout(layout)

    def create(self):
        name = self.name_input.text()

        self.client.create_group(name)

    def cansel(self):
        self.stacked_widget.setCurrentIndex(2)


    def display_created_group(self, responce):
        if responce['CREATED']:
            self.stacked_widget.setCurrentIndex(2)




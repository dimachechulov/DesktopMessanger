from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from sqlalchemy.exc import DataError

from auth.auth import AuthService
from pages.MainPage import MyApp


class LoginWidget(QWidget):
    def __init__(self, stacked_widget,  client, main_window):
        self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        self.main_window = main_window
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Регистрация пользователя')
        self.setFixedSize(800,800)
        #self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.username_label = QLabel('Имя пользователя:')
        self.username_label.setFont(QFont('Arial', 25))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Arial', 25))
        self.username_input.setPlaceholderText('Enter your username')
        self.password_label = QLabel('Пароль:')
        self.password_label.setFont(QFont('Arial', 25))
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont('Arial', 25))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter your password')
        self.login_button = QPushButton('Войти')
        self.login_button.setFixedHeight(50)
        self.login_button.clicked.connect(self.login_click)

        self.go_to_login_button = QPushButton('У меня нет аккаунта')
        self.go_to_login_button.setFixedHeight(50)
        self.go_to_login_button.clicked.connect(self.go_to_register)
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.go_to_login_button)
        self.setLayout(layout)

    def login_click(self):
        username = self.username_input.text()
        password = self.password_input.text()


        try:
            self.client.token,  self.client.user  =  self.reg_service.login_user(username, password)
            self.client.connect_server()
        except ValueError as err:
            print(err.args)
            self.error_label.setText(err.args[0])
            return
        except DataError as err:
            print(err.args)
            self.error_label.setText("Err input in fields")
            return
        except Exception as ex:
            print(ex.args)
            return
        self.main_window.initAfterLogin()
        self.stacked_widget.setCurrentIndex(2)

    def go_to_register(self):
        self.stacked_widget.setCurrentIndex(0)

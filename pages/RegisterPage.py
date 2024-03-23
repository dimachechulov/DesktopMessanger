from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from sqlalchemy.exc import DataError

from auth.auth import AuthService
from pages.MainPage import MyApp


class RegistrationWidget(QWidget):
    def __init__(self, stacked_widget, client, main_window):
        self.reg_service = AuthService()
        self.stacked_widget = stacked_widget
        self.client = client
        self.main_window = main_window
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Registration User')
        self.setGeometry(800, 800, 800, 650)
        self.error_label = QLabel('')
        self.username_label = QLabel('Username:')
        self.username_label.setFont(QFont('Arial', 25))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Arial', 25))
        self.username_input.setPlaceholderText('Enter your username')
        self.password_label = QLabel('Password:')
        self.password_label.setFont(QFont('Arial', 25))
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont('Arial', 25))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter your password')

        self.email_label = QLabel('Email:')
        self.email_label.setFont(QFont('Arial', 25))
        self.email_input = QLineEdit()
        self.email_input.setFont(QFont('Arial', 25))
        self.email_input.setPlaceholderText('Enter your email')

        self.age_label = QLabel('Возраст:')
        self.age_label.setFont(QFont('Arial', 25))
        self.age_input = QLineEdit()
        self.age_input.setFont(QFont('Arial', 25))
        self.age_input.setPlaceholderText('Enter your age')

        self.register_button = QPushButton('Register')
        self.register_button.setFixedHeight(50)
        self.register_button.clicked.connect(self.register_click)


        self.go_to_login_button = QPushButton('I have account')
        self.go_to_login_button.setFixedHeight(50)
        self.go_to_login_button.clicked.connect(self.go_to_login)
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.go_to_login_button)
        self.setLayout(layout)

    def register_click(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        age = self.age_input.text()

        try:
            self.client.token,  self.client.user = self.reg_service.register_user(username,password, email, age)
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

    def go_to_login(self):
        self.stacked_widget.setCurrentIndex(1)
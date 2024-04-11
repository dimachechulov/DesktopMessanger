import socket
import select
import logging

from auth.auth import AuthService
from DBManager import DBManager
from configs.default import ACTION, SENDER, DESTINATION, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, DEFAULT_PORT, \
    test_db_url, current_db_url
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from ParserClientMessage import ParserClientMessage
from Manager.Manager import Manager
from FakeDBManager import FakeDBManager

# Инициализация серверного логера
server_logger = logging.getLogger('server')




class Server:
    def __init__(self, listen_addr, listen_port, db):
        self.all_clients = []
        self.all_messages_in_router = []
        self.all_messages = []
        self.all_names = dict()
        self.DBManager = db
        self.auth_service = AuthService(self.DBManager)
        self.Manager = Manager(self.DBManager)
        self.run_server(listen_addr, listen_port)


    def run_server(self,listen_addr, listen_port):


        # Создает TCP-сокет сервера
        self.server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Связывает сокет с ip-адресом и портом сервера
        self.server_tcp.bind((listen_addr, listen_port))

        # Таймаут для операций с сокетом
        self.server_tcp.settimeout(0.5)

        # Запускает режим прослушивания
        self.server_tcp.listen(MAX_CONNECTIONS)

        server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                           f'адрес с которого принимаются подключения: {listen_addr}. '
                           f'Если адрес не указан, принимаются соединения с любых адресов.')

        print(f'Запущен сервер, порт для подключений: {listen_port}, '
              f'адрес с которого принимаются подключения: {listen_addr}.')


    def run(self):
        while True:
            try:
                client_tcp, client_addr = self.server_tcp.accept()
            except OSError:
                pass
            else:
                server_logger.info(f'Установлено соедение с клиентом {client_addr}')
                print(f'Установлено соедение с клиентом {client_addr}')
                self.all_clients.append(client_tcp)

            r_clients = []
            w_clients = []
            errs = []

            # Запрашивает информацию о готовности к вводу, выводу и о наличии исключений для группы дескрипторов сокетов
            try:
                if self.all_clients:
                    r_clients, w_clients, errs = select.select(self.all_clients, self.all_clients, [], 0)
            except OSError:
                pass
            # print(f"all_clients : {all_clients}\n ")
            # Чтение запросов из списка клиентов
            if r_clients:
                for r_sock in r_clients:
                    try:
                        ParserClientMessage.parse_client_msg(receive_message(r_sock), self.all_messages_in_router, r_sock,
                                         self.all_clients, self.all_names,  self.auth_service, self.Manager)
                    except Exception as ex:
                        server_logger.error(f'Клиент отключился от сервера. '
                                            f'Тип исключения: {type(ex).__name__}, аргументы: {ex.args}')

                        self.all_clients.remove(r_sock)
                        inverted_all_names = {v: k for k, v in self.all_names.items()}
                        if r_sock in inverted_all_names:
                            key_to_remove = inverted_all_names.pop(r_sock)
                            del self.all_names[key_to_remove]

            # print(f"All messages: {all_messages}")
            # print(f"All messages in router: {all_messages_in_router}")
            # Роутинг сообщений адресатам








if __name__ == '__main__':
    is_test = server_parse_cmd_arguments()
    if is_test == 'test':
        db = FakeDBManager()
    else:
        db = DBManager(current_db_url)
    listen_addr, listen_port = '', DEFAULT_PORT
    server = Server(listen_addr, listen_port, db)
    server.run()



    # Список клиентов и очередь сообщений
    # all_clients = []
    # all_messages_in_router = []
    # all_messages = []
    # # Словарь зарегистрированных клиентов: ключ - имя пользователя, значение - сокет
    # all_names = dict()



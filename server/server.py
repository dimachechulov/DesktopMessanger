import socket
import select
import logging

from auth.auth import AuthService
from DBManager import DBManager
from configs.default import ACTION, SENDER, DESTINATION, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from ParserClientMessage import ParserClientMessage
from Manager.Manager import Manager

# Инициализация серверного логера
server_logger = logging.getLogger('server')




class Server:
    def __init__(self, server_tcp):
        self.all_clients = []
        self.all_messages_in_router = []
        self.all_messages = []
        self.all_names = dict()
        self.server_tcp = server_tcp
        self.DBManager = DBManager()
        self.auth_service = AuthService(self.DBManager)
        self.Manager = Manager(self.DBManager)

    def route_client_msg(self,message, names, clients):
        """
        Адресная отправка сообщений.
        :param message: словарь сообщения
        :param names: список зарегистрированных клиентов
        :param clients: список слушающих клиентских сокетов
        :return:
        """
        print(f"message in route: {message}")
        print(f"message to: {message[DESTINATION]} message sender: {message[SENDER]}")
        if message[DESTINATION] in names and names[message[DESTINATION]] in clients:
            responce = {
                ACTION: MESSAGE,
                SENDER:message[SENDER],
                DESTINATION : message[DESTINATION],
                MESSAGE_TEXT:message[MESSAGE_TEXT],
                "CREATE_AT": message["CREATE_AT"]
            }
            send_message(names[message[DESTINATION]], responce)
            print(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[DESTINATION]}.')
            server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in names and names[message[SENDER]] not in clients:
            print(f"ConnectionError")
            raise ConnectionError
        else:
            print(f"ConnectionError")
            server_logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

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
                        key_to_remove = inverted_all_names.pop(r_sock)
                        del self.all_names[key_to_remove]

            # print(f"All messages: {all_messages}")
            # print(f"All messages in router: {all_messages_in_router}")
            # Роутинг сообщений адресатам
            for msg in self.all_messages_in_router:
                try:
                    self.route_client_msg(msg, self.all_names, w_clients)
                except Exception as  ex:
                    print(ex)
                    server_logger.info(f'Связь с клиентом {msg[DESTINATION]} была потеряна')
                    if self.all_names[msg[DESTINATION]] in self.all_clients:
                        self.all_clients.remove(self.all_names[msg[DESTINATION]])
                    del self.all_names[msg[DESTINATION]]
            self.all_messages_in_router.clear()







if __name__ == '__main__':

    # Извлекает ip-адрес и порт из командной строки
    listen_addr, listen_port= server_parse_cmd_arguments()

    # Создает TCP-сокет сервера
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Связывает сокет с ip-адресом и портом сервера
    server_tcp.bind((listen_addr, listen_port))

    # Таймаут для операций с сокетом
    server_tcp.settimeout(0.5)

    # Запускает режим прослушивания
    server_tcp.listen(MAX_CONNECTIONS)

    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_addr}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    print(f'Запущен сервер, порт для подключений: {listen_port}, '
          f'адрес с которого принимаются подключения: {listen_addr}.')

    server = Server(server_tcp)
    server.run()



    # Список клиентов и очередь сообщений
    # all_clients = []
    # all_messages_in_router = []
    # all_messages = []
    # # Словарь зарегистрированных клиентов: ключ - имя пользователя, значение - сокет
    # all_names = dict()



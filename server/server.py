import sys
import json
import socket
import select
import argparse
import time
import logging
import logs.server_log_config

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, EXIT, RESPONSE_200, RESPONSE_400, PREVIOUS
from configs.utils import send_message, receive_message,  server_parse_cmd_arguments
from decorators.decorators import MyLogger

# Инициализация серверного логера
server_logger = logging.getLogger('server')

class ParserClientMessage:
    @MyLogger
    @staticmethod
    def parse_client_msg(message, messages_list,messages_in_route_list, sock, clients_list, names):
        """
        Обработчик сообщений клиентов
        :param message: словарь сообщения
        :param messages_list: список сообщений
        :param sock: клиентский сокет
        :param clients_list: список клиентских сокетов
        :param names: список зарегистрированных клиентов
        :return: словарь ответа
        """
        server_logger.debug(f'Разбор сообщения от клиента: {message}')
        print(f'Разбор сообщения от клиента: {message}')

        if ACTION in message and message[ACTION] == PRESENCE and \
                TIME in message and USER in message:

            if message[USER][ACCOUNT_NAME] not in names.keys():
                names[message[USER][ACCOUNT_NAME]] = sock
                send_message(sock, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(sock, response)
                clients_list.remove(sock)
                sock.close()
            return

        # формирует очередь сообщений
        elif ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and DESTINATION in message and \
                MESSAGE_TEXT in message and TIME in message:
            messages_list.append(message)
            messages_in_route_list.append(message)
            return

        elif ACTION in message and message[ACTION] == PREVIOUS and \
            SENDER in message and DESTINATION in message:
            list_of_messages = []
            for msg in messages_list:
                if (msg[SENDER] == message[SENDER] and msg[DESTINATION] == message[DESTINATION]) or (msg[SENDER] == message[DESTINATION] and msg[DESTINATION] == message[SENDER]):
                    print(f'msg[SENDER] : {msg[SENDER]}, message[SENDER]: {message[SENDER]}, msg[DESTINATION]: {msg[DESTINATION]}, message[DESTINATION]: {message[DESTINATION]}')
                    list_of_messages.append(msg)
            response={
                ACTION:PREVIOUS,
                SENDER:message[SENDER],
                'messages':list_of_messages
            }
            send_message(sock, response)
            return

        # выход клиента
        elif ACTION in message and message[ACTION] == EXIT and \
                ACCOUNT_NAME in message:
            clients_list.remove(names[message[USER][ACCOUNT_NAME]])
            names[message[USER][ACCOUNT_NAME]].close()
            del names[message[USER][ACCOUNT_NAME]]
            return

        # возвращает сообщение об ошибке
        else:
            response = RESPONSE_400
            response[ERROR] = 'Некорректный запрос.'
            send_message(sock, response)
            return


class Server:
    def __init__(self, server_tcp):
        self.all_clients = []
        self.all_messages_in_router = []
        self.all_messages = []
        self.all_names = dict()
        self.server_tcp = server_tcp
    def route_client_msg(self,message, names, clients):
        """
        Адресная отправка сообщений.
        :param message: словарь сообщения
        :param names: список зарегистрированных клиентов
        :param clients: список слушающих клиентских сокетов
        :return:
        """
        print(f"message in route: {message}")
        print(f"message destination: {message[DESTINATION]} message sender: {message[SENDER]}")
        if message[DESTINATION] in names and names[message[DESTINATION]] in clients:
            send_message(names[message[DESTINATION]], message)
            print(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
            server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in names and names[message[DESTINATION]] not in clients:
            raise ConnectionError
        else:
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
                        ParserClientMessage.parse_client_msg(receive_message(r_sock), self.all_messages, self.all_messages_in_router, r_sock,
                                         self.all_clients, self.all_names)
                    except Exception as ex:
                        server_logger.error(f'Клиент отключился от сервера. '
                                            f'Тип исключения: {type(ex).__name__}, аргументы: {ex.args}')
                        self.all_clients.remove(r_sock)
            # print(f"All messages: {all_messages}")
            # print(f"All messages in router: {all_messages_in_router}")
            # Роутинг сообщений адресатам
            for msg in self.all_messages_in_router:
                try:
                    self.route_client_msg(msg, self.all_names, w_clients)
                except Exception:
                    server_logger.info(f'Связь с клиентом {msg[DESTINATION]} была потеряна')
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



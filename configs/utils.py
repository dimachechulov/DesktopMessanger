import json

from configs.default import ENCODING, MAX_PACKAGE_LENGTH
import argparse
import sys

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, EXIT, PREVIOUS

def receive_message(sock):
    """
    Получение сообщения
    :param sock: сокет
    :return: словарь ответа
    """

    # Получает байты
    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        # Декодирует байтстроку в строку
        json_response = encoded_response.decode(ENCODING)
        # Десериализует строку, содержащую документ JSON, в объект Python
        response = json.loads(json_response)
        if isinstance(response, dict):
            # Возвращает словарь
            return response
        else:
            raise ValueError
    else:
        raise ValueError


def server_parse_cmd_arguments():
    """
    Парсер аргументов командной строки
    :return: ip-адрес и порт сервера
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("echo")
    args = parser.parse_args()
    return args.echo
def parse_cmd_arguments():
    """
    Парсер аргументов командной строки
    :return: ip-адрес и порт сервера, режим клиента
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default='None', nargs='?')

    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.a
    port = namespace.p
    name = namespace.name

    # проверим подходящий номер порта
    if port < 1024 or port > 65535:
        sys.exit(1)

    return addr, port, name
def send_message(sock, message):
    """
    Отправка сообщения
    :param sock: сокет
    :param message: словарь сообщения
    :return: None
    """

    # Сериализует message в JSON-подобный формат
    js_message = json.dumps(message)
    # Кодирует строку в байты / байтстроку
    encoded_message = js_message.encode(ENCODING)
    # Отправляет сообщение
    sock.send(encoded_message)

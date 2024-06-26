import logging
import os
from dotenv import load_dotenv
from pathlib import Path
# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 17184
# Кодировка проекта
ENCODING = 'utf-8'
# Уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'FROM'
DESTINATION = 'TO'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
PREVIOUS='previous'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'

# Ответы сервера
RESPONSE_200 = {
    RESPONSE: 200
}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}


path = Path('../.env')
load_dotenv(dotenv_path=path)
current_db_url = os.getenv('CURRENT_DB_URL')
test_db_url = os.getenv('TEST_DB_URL')

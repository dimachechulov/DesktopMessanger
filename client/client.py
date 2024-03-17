class Client:
    def display_previous_message(self, sock, account_name, receiver_name):
        message_dict = {
            ACTION: PREVIOUS,
            SENDER: account_name,
            DESTINATION: receiver_name,
        }
        try:
            send_message(sock, message_dict)
            client_logger.info(f'Запрошено сообщения с {receiver_name}')
        except Exception:
            client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)
    def create_client_msg(self):
        """
        Формирование и отправка на сервер сообщения клиента
        :param sock: клиентский сокет
        :param account_name: строка псевдонима
        :return message_dict: словарь сообщения клиента
        """

        message_str = self.tb_send_message.text()
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.user_name,
            DESTINATION: self.receiver_name,
            MESSAGE_TEXT: message_str
        }
        client_logger.debug(f'Сформировано сообщение: {message_dict}')
        self.chat.setText(self.chat.text() + f'[you]: {message_str}\n')
        try:
            send_message(self.sock, message_dict)
            client_logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception:
            client_logger.critical('Потеряно соединение с сервером.')
            sys.exit(1)
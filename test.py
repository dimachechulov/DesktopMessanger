import os
import time
import unittest

from dotenv import load_dotenv

from client.ParserServerMessage import ParserServerMessage
from client.client import Client
from configs.default import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from configs.utils import parse_cmd_arguments, receive_message



class TestServerMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server_addr, server_port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
        cls.client1 = Client(server_addr, server_port)
        cls.client1.register_user('1', '1', '1@gmail.com', '2')
        result = receive_message(cls.client1.sock)
        print(result)
        cls.client1.token = result['TOKEN']
        cls.client1.user = result['USER']
        cls.client2 = Client(server_addr, server_port)
        cls.client2.register_user('2', '2', '2@gmail.com', '2')
        result = receive_message(cls.client2.sock)
        print(result)
        cls.client2.token = result['TOKEN']
        cls.client2.user = result['USER']
    def test_send_message(self):
        self.client1.receiver_name = self.client2.user['name']
        self.client1.create_client_msg("Hiii")
        result = receive_message(self.client2.sock)
        self.assertEqual(result['from'], '1')
        self.assertEqual(result['to'], '2')
        self.assertEqual(result['message_text'], 'Hiii')
    def test_previous(self):
        self.client1.receiver_name = self.client2.user['name']
        self.client1.create_client_msg("Hiii")
        receive_message(self.client2.sock)
        self.client1.receiver_name = self.client2.user['name']
        self.client1.display_previous_message()
        result = receive_message(self.client1.sock)
        self.assertEqual(result['MESSAGE'][0]['CONTENT'], 'Hiii')
        self.assertEqual(result['MESSAGE'][0]['from'], 0)
        self.assertEqual(result['MESSAGE'][0]['to'], 1)
        self.assertEqual(result['STATUS'], 'NOTHING')


    def test_query(self):
        self.client1.create_query( self.client2.user['name'])
        result1 = receive_message(self.client1.sock)
        result2 = receive_message(self.client2.sock)
        self.assertEqual(result1['action'], 'CREATE_QUERY')
        self.assertEqual(result1['CREATED'], True)
        self.assertEqual(result2['action'], 'DISPLAY_QUERY')
        self.assertEqual(result2['FROM_USERNAME'], '1')
        self.client2.accept_query(self.client1.user['name'])
        result1 = receive_message(self.client1.sock)
        result2 = receive_message(self.client2.sock)
        self.assertEqual(result1['action'], 'ACCEPT_QUERY')
        self.assertEqual(result1['FRIEND'], '2')
        self.assertEqual(result2['action'], 'ACCEPT_QUERY')
        self.assertEqual(result2['FRIEND'], '1')
        self.client1.init_friends()
        result1 = receive_message(self.client1.sock)
        print(result1)
        self.assertEqual(result1['action'], 'GET_FRIEND')
        self.assertEqual(result1['FRIENDS'][0]['NAME'], '2')
        self.client2.init_friends()
        result2 = receive_message(self.client2.sock)
        print(result2)
        self.assertEqual(result2['action'], 'GET_FRIEND')
        self.assertEqual(result2['FRIENDS'][0]['NAME'], '1')






if __name__ == '__main__':
    unittest.main()

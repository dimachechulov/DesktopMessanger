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
        cls.client1.token = result['TOKEN']
        cls.client1.user = result['USER']
        cls.client2 = Client(server_addr, server_port)
        cls.client2.register_user('2', '2', '2@gmail.com', '2')
        result = receive_message(cls.client2.sock)
        cls.client2.token = result['TOKEN']
        cls.client2.user = result['USER']
        cls.client3 = Client(server_addr, server_port)
        cls.client3.register_user('3', '3', '3@gmail.com', '3')
        result = receive_message(cls.client3.sock)
        cls.client3.token = result['TOKEN']
        cls.client3.user = result['USER']
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
        self.client1.init_friends_group()
        result1 = receive_message(self.client1.sock)
        print(result1)
        self.assertEqual(result1['action'], 'GET_FRIEND_GROUP')
        self.assertEqual(result1['FRIENDS'][0]['NAME'], '2')
        self.client2.init_friends_group()
        result2 = receive_message(self.client2.sock)
        print(result2)
        self.assertEqual(result2['action'], 'GET_FRIEND_GROUP')
        self.assertEqual(result2['FRIENDS'][0]['NAME'], '1')

    def test_groups(self):
        self.client1.create_group("New Group")
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'CREATE_GROUP')
        self.assertEqual(responce['CREATED'], True)

        self.client1.selected_group = 'New Group'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.assertEqual(responce_from['action'], 'ADD_IN_GROUP')
        self.assertEqual(responce_from['ADDED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group')
        self.assertEqual(responce_to['action'], 'ADDED_IN_GROUP')
        self.assertEqual(responce_to['ADDED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group')

        self.client2.selected_group = 'New Group'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.assertEqual(responce_from['action'], 'ADD_IN_ADMIN')
        self.assertEqual(responce_from['ADDED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group')
        self.assertEqual(responce_to['action'], 'ADDED_IN_ADMIN')
        self.assertEqual(responce_to['ADDED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group')

        self.client2.add_in_group(self.client3.user['name'])
        receive_message(self.client2.sock)
        receive_message(self.client3.sock)
        self.client1.create_client_msg_in_group('Hiiii')
        responce_to = receive_message(self.client2.sock)
        responce_to1 = receive_message(self.client3.sock)
        print(responce_to, responce_to1)
        self.assertEqual(responce_to1['action'], 'MESSAGE_IN_GROUP')
        self.assertEqual(responce_to1['from'], '1')
        self.assertEqual(responce_to1['GROUP'], 'New Group')
        self.assertEqual(responce_to1['message_text'], 'Hiiii')
        self.assertEqual(responce_to['action'], 'MESSAGE_IN_GROUP')
        self.assertEqual(responce_to['from'], '1')
        self.assertEqual(responce_to['GROUP'], 'New Group')
        self.assertEqual(responce_to['message_text'], 'Hiiii')

        self.client3.open_group('New Group')
        responce = receive_message(self.client3.sock)
        self.assertEqual(responce['action'], 'OPEN_GROUP')
        self.assertEqual(responce['MESSAGES'][0]['CONTENT'],'Hiiii')
        self.assertEqual(responce['MESSAGES'][0]['from'], '1')
        self.assertEqual(responce['GROUP'], 'New Group')
        self.assertEqual(responce['STATUS'], 'NOTHING')

        self.client1.open_group('New Group')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['STATUS'], 'OWNER')

        self.client2.open_group('New Group')
        responce = receive_message(self.client2.sock)
        self.assertEqual(responce['STATUS'], 'ADMIN')

        self.client1.get_users_in_group('TEST')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'GET_USERS_IN_GROUP')
        self.assertEqual(responce['USERS'][0]['NAME'], '1')
        self.assertEqual(responce['USERS'][1]['NAME'], '2')
        self.assertEqual(responce['USERS'][2]['NAME'], '3')

        self.client1.delete_from_group(self.client3.user['name'])
        responce_to = receive_message(self.client1.sock)
        responce_from = receive_message(self.client3.sock)
        self.assertEqual(responce_to['action'], 'DELETE_FROM_GROUP')
        self.assertEqual(responce_to['DELETED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group')
        self.assertEqual(responce_from['action'], 'DELETED_FROM_GROUP')
        self.assertEqual(responce_from['DELETED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group')

        self.client1.get_users_in_group('TEST')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'GET_USERS_IN_GROUP')
        self.assertEqual(responce['USERS'][0]['NAME'], '1')
        self.assertEqual(responce['USERS'][1]['NAME'], '2')

        self.client1.get_users_in_group('DELETE_ADMIN')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'GET_USERS_IN_GROUP')
        self.assertEqual(responce['USERS'][0]['NAME'], '2')

        self.client1.delete_from_admin(self.client2.user['name'])
        responce_to = receive_message(self.client1.sock)
        responce_from = receive_message(self.client2.sock)
        self.assertEqual(responce_to['action'], 'DELETE_ADMIN')
        self.assertEqual(responce_to['DELETED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group')
        self.assertEqual(responce_from['action'], 'DELETED_ADMIN')
        self.assertEqual(responce_from['DELETED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group')










if __name__ == '__main__':
    unittest.main()

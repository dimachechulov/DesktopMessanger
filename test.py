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
        result_from = receive_message(self.client1.sock)
        result = receive_message(self.client2.sock)
        self.assertEqual(result['FROM'], '1')
        self.assertEqual(result['TO'], '2')
        self.assertEqual(result['message_text'], 'Hiii')
    def test_previous(self):
        self.client1.receiver_name = self.client2.user['name']
        self.client1.create_client_msg("Hiii")
        receive_message(self.client2.sock)
        receive_message(self.client1.sock)
        self.client1.receiver_name = self.client2.user['name']
        self.client1.display_previous_message()
        result = receive_message(self.client1.sock)
        self.assertEqual(result['MESSAGE'][0]['CONTENT'], 'Hiii')
        self.assertEqual(result['MESSAGE'][0]['FROM'], 0)
        self.assertEqual(result['MESSAGE'][0]['TO'], 1)
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
        self.assertEqual(result1['action'], 'GET_FRIEND_GROUP')
        self.assertEqual(result1['FRIENDS'][0]['NAME'], '2')
        self.client2.init_friends_group()
        result2 = receive_message(self.client2.sock)
        self.assertEqual(result2['action'], 'GET_FRIEND_GROUP')
        self.assertEqual(result2['FRIENDS'][0]['NAME'], '1')

    def test_groups_create_group(self):
        self.client1.create_group("New Group")
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'CREATE_GROUP')
        self.assertEqual(responce['CREATED'], True)



    def test_groups_add_in_group(self):
        self.client1.create_group("New Group1")
        responce = receive_message(self.client1.sock)
        self.client1.selected_group = 'New Group1'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.assertEqual(responce_from['action'], 'ADD_IN_GROUP')
        self.assertEqual(responce_from['ADDED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group1')
        self.assertEqual(responce_to['action'], 'ADDED_IN_GROUP')
        self.assertEqual(responce_to['ADDED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group1')


    def test_groups_add_in_admin(self):
        self.client1.create_group("New Group2")
        responce = receive_message(self.client1.sock)
        self.client1.selected_group = 'New Group2'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.client2.selected_group = 'New Group2'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.assertEqual(responce_from['action'], 'ADD_IN_ADMIN')
        self.assertEqual(responce_from['ADDED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group2')
        self.assertEqual(responce_to['action'], 'ADDED_IN_ADMIN')
        self.assertEqual(responce_to['ADDED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group2')

    def test_groups_send_message(self):
        self.client1.create_group("New Group3")
        responce = receive_message(self.client1.sock)
        self.client1.selected_group = 'New Group3'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.client2.selected_group = 'New Group3'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.client2.add_in_group(self.client3.user['name'])
        receive_message(self.client2.sock)
        receive_message(self.client3.sock)
        self.client1.create_client_msg_in_group('Hiiii')
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        responce_to1 = receive_message(self.client3.sock)
        self.assertEqual(responce_from['action'], 'MESSAGE_IN_GROUP')
        self.assertEqual(responce_from['FROM'], '1')
        self.assertEqual(responce_from['GROUP'], 'New Group3')
        self.assertEqual(responce_from['message_text'], 'Hiiii')
        self.assertEqual(responce_to1['action'], 'MESSAGE_IN_GROUP')
        self.assertEqual(responce_to1['FROM'], '1')
        self.assertEqual(responce_to1['GROUP'], 'New Group3')
        self.assertEqual(responce_to1['message_text'], 'Hiiii')
        self.assertEqual(responce_to['action'], 'MESSAGE_IN_GROUP')
        self.assertEqual(responce_to['FROM'], '1')
        self.assertEqual(responce_to['GROUP'], 'New Group3')
        self.assertEqual(responce_to['message_text'], 'Hiiii')


    def test_groups_status_group(self):
        self.client1.create_group("New Group4")
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'CREATE_GROUP')
        self.assertEqual(responce['CREATED'], True)

        self.client1.selected_group = 'New Group4'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.client2.selected_group = 'New Group4'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.client2.add_in_group(self.client3.user['name'])
        receive_message(self.client2.sock)
        receive_message(self.client3.sock)
        self.client1.create_client_msg_in_group('Hiiii')
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        responce_to1 = receive_message(self.client3.sock)
        self.client3.open_group('New Group4')
        responce = receive_message(self.client3.sock)
        self.assertEqual(responce['action'], 'OPEN_GROUP')
        self.assertEqual(responce['MESSAGES'][0]['CONTENT'], 'Hiiii')
        self.assertEqual(responce['MESSAGES'][0]['FROM'], '1')
        self.assertEqual(responce['GROUP'], 'New Group4')
        self.assertEqual(responce['STATUS'], 'NOTHING')
        self.client1.open_group('New Group4')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['STATUS'], 'OWNER')

        self.client2.open_group('New Group4')
        responce = receive_message(self.client2.sock)
        self.assertEqual(responce['STATUS'], 'ADMIN')


    def test_groups_delete_from_group(self):
        self.client1.create_group("New Group5")
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'CREATE_GROUP')
        self.assertEqual(responce['CREATED'], True)

        self.client1.selected_group = 'New Group5'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        self.assertEqual(responce_from['action'], 'ADD_IN_GROUP')
        self.assertEqual(responce_from['ADDED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group5')
        self.assertEqual(responce_to['action'], 'ADDED_IN_GROUP')
        self.assertEqual(responce_to['ADDED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group5')

        self.client2.selected_group = 'New Group5'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)


        self.client2.add_in_group(self.client3.user['name'])
        receive_message(self.client2.sock)
        receive_message(self.client3.sock)
        self.client1.create_client_msg_in_group('Hiiii')
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        responce_to1 = receive_message(self.client3.sock)


        self.client3.open_group('New Group5')
        responce = receive_message(self.client3.sock)
        self.client1.open_group('New Group5')
        responce = receive_message(self.client1.sock)
        self.client2.open_group('New Group5')
        responce = receive_message(self.client2.sock)
        self.client1.get_users_in_group('TEST')
        responce = receive_message(self.client1.sock)
        self.client1.delete_from_group(self.client3.user['name'])
        responce_to = receive_message(self.client1.sock)
        responce_from = receive_message(self.client3.sock)
        self.assertEqual(responce_to['action'], 'DELETE_FROM_GROUP')
        self.assertEqual(responce_to['DELETED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group5')
        self.assertEqual(responce_from['action'], 'DELETED_FROM_GROUP')
        self.assertEqual(responce_from['DELETED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group5')

    def test_groups_delete_from_admin(self):
        self.client1.create_group("New Group6")
        responce = receive_message(self.client1.sock)
        self.client1.selected_group = 'New Group6'
        self.client1.add_in_group(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)


        self.client2.selected_group = 'New Group6'
        self.client1.add_in_admin(self.client2.user['name'])
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)

        self.client2.add_in_group(self.client3.user['name'])
        receive_message(self.client2.sock)
        receive_message(self.client3.sock)
        self.client1.create_client_msg_in_group('Hiiii')
        responce_from = receive_message(self.client1.sock)
        responce_to = receive_message(self.client2.sock)
        responce_to1 = receive_message(self.client3.sock)


        self.client3.open_group('New Group6')
        responce = receive_message(self.client3.sock)


        self.client1.open_group('New Group6')
        responce = receive_message(self.client1.sock)


        self.client2.open_group('New Group6')
        responce = receive_message(self.client2.sock)


        self.client1.delete_from_group(self.client3.user['name'])
        responce_to = receive_message(self.client1.sock)
        responce_from = receive_message(self.client3.sock)


        self.client1.get_users_in_group('TEST')
        responce = receive_message(self.client1.sock)

        self.client1.get_users_in_group('DELETE_ADMIN')
        responce = receive_message(self.client1.sock)
        self.assertEqual(responce['action'], 'GET_USERS_IN_GROUP')
        self.assertEqual(responce['USERS'][0]['NAME'], '2')

        self.client1.delete_from_admin(self.client2.user['name'])
        responce_to = receive_message(self.client1.sock)
        responce_from = receive_message(self.client2.sock)
        self.assertEqual(responce_to['action'], 'DELETE_ADMIN')
        self.assertEqual(responce_to['DELETED'], True)
        self.assertEqual(responce_to['GROUP'], 'New Group6')
        self.assertEqual(responce_from['action'], 'DELETED_ADMIN')
        self.assertEqual(responce_from['DELETED'], True)
        self.assertEqual(responce_from['GROUP'], 'New Group6')

    def test_delete_message(self):
        self.client1.receiver_name = self.client2.user['name']
        self.client1.create_client_msg("Hiii")
        result_from = receive_message(self.client1.sock)
        result = receive_message(self.client2.sock)
        self.assertEqual(result['FROM'], '1')
        self.assertEqual(result['TO'], '2')
        self.assertEqual(result['message_text'], 'Hiii')
        self.client1.receiver_name = self.client2.user['name']
        self.client1.display_previous_message()
        result= receive_message(self.client1.sock)
        self.client1.delete_message(result['MESSAGE'][0]['ID'])
        result = receive_message(self.client1.sock)
        result_from = receive_message(self.client2.sock)
        self.client1.display_previous_message()
        result = receive_message(self.client1.sock)
        print(result)
        self.assertEqual(result['MESSAGE'], [])

    def test_update_message(self):
        self.client1.receiver_name = self.client3.user['name']
        self.client1.create_client_msg("Hiii")
        result_from = receive_message(self.client1.sock)
        result = receive_message(self.client3.sock)
        self.client1.receiver_name = self.client3.user['name']
        self.client1.display_previous_message()
        result= receive_message(self.client1.sock)
        self.client1.update_message(result['MESSAGE'][0]['ID'], "New_text")
        result = receive_message(self.client1.sock)
        result_from = receive_message(self.client3.sock)
        self.client1.display_previous_message()
        result = receive_message(self.client1.sock)
        self.assertEqual(result['MESSAGE'][0]['CONTENT'], 'New_text')

    def test_search_message(self):
        self.client2.receiver_name = self.client3.user['name']
        self.client2.create_client_msg("Hiii")
        result_from = receive_message(self.client2.sock)
        result = receive_message(self.client3.sock)
        self.client2.receiver_name = self.client3.user['name']
        self.client2.display_previous_message()
        result= receive_message(self.client2.sock)
        self.client2.search_message("Hi")
        result = receive_message(self.client2.sock)
        self.assertEqual(len(result['MESSAGES_ID']), 1)












if __name__ == '__main__':
    unittest.main()

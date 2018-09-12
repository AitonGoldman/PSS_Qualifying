import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from proxies.PssUsersProxy import PssUsersProxy

class PssUsersProxyTest(PssUnitTestBase):
    def setUp(self):
        self.pss_user_mock = MagicMock()        
        self.input_dict = {'test_value':'value'}
        self.pss_user_mock.to_dict.return_value=self.input_dict
        self.pss_user_mock.event_roles_for_user=[]
        self.mock_event = MagicMock()
        self.mock_event_role = MagicMock()
        self.mock_event_role.event_role_id=1        
        
        db_handle_mock = MagicMock()
        pss_user_model_mock = MagicMock()        
        self.deserializer_mock = MagicMock()                
        self.table_proxy_mock = MagicMock()
        self.table_proxy_mock.pssDeserializers.pss_user_schema.deserialize().data=self.pss_user_mock        
        
        self.pss_users_proxy = PssUsersProxy(db_handle_mock,
                                             self.table_proxy_mock,
                                             model=pss_user_model_mock)
        
        
    def test_get_pss_users_with_invalid_pss_user_id(self):                        
        self.pss_users_proxy.pss_users_model.query.filter_by().first.return_value=None
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(pss_user_id=1)
        self.assertEqual(pss_user,None)
        self.pss_users_proxy.pss_users_model.query.filter_by.assert_called_with(pss_user_id=1)        
        self.assertEqual(pss_user_dict,None)

    def test_get_pss_user_by_pss_user_id_with_serializer(self):
        
        self.pss_users_proxy.pss_users_model.query.filter_by().first.return_value=self.pss_user_mock
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(pss_user_id=1)
        self.assertEqual(pss_user,self.pss_user_mock)
        self.pss_users_proxy.pss_users_model.query.filter_by.assert_called_with(pss_user_id=1)        
        self.assertEqual(pss_user_dict,self.input_dict)

    def test_get_pss_user_by_pss_username_with_serializer(self):
        self.pss_users_proxy.pss_users_model.query.filter_by().first.return_value=self.pss_user_mock
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(username='poop')
        self.assertEqual(pss_user,self.pss_user_mock)
        self.pss_users_proxy.pss_users_model.query.filter_by.assert_called_with(username='poop')        
        self.assertEqual(pss_user_dict,self.input_dict)

    def test_get_pss_user_by_full_name_with_serializer(self):                
        self.pss_users_proxy.pss_users_model.query.filter_by().first.return_value=self.pss_user_mock
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(first_name='poop',last_name='mcpoop')
        self.assertEqual(pss_user,self.pss_user_mock)
        self.pss_users_proxy.pss_users_model.query.filter_by.assert_called_with(first_name='poop',last_name='mcpoop')        
        self.assertEqual(pss_user_dict,self.input_dict)

    def test_update_pss_user(self):        
        self.input_dict['pss_user_id']=1                
        self.pss_users_proxy.pss_users_model.query.filter_by().first.return_value=self.pss_user_mock                
        pss_user,pss_user_dict = self.pss_users_proxy.update_pss_user(self.input_dict)                        
        self.assertEqual(pss_user,self.pss_user_mock)        
        self.assertEqual(pss_user_dict,self.input_dict)
                
    def test_create_pss_user(self):
        self.input_dict['password'] = "password"
        self.table_proxy_mock.events_proxy.get_event.return_value=self.mock_event
        self.table_proxy_mock.event_roles.get_event_roles.return_value=[self.mock_event_role]
        pss_user,pss_user_dict = self.pss_users_proxy.create_pss_user(self.input_dict,event_id=1,role_id=1)                        
        self.assertTrue(len(pss_user.event_roles_for_user)==1)
        self.assertEqual(pss_user.event_roles_for_user[0].events,self.mock_event)
        self.assertEqual(pss_user.event_roles_for_user[0].event_roles,self.mock_event_role)        
        self.assertEqual(pss_user,self.pss_user_mock)        
        self.assertEqual(pss_user_dict,self.input_dict)        
        self.assertEqual(pss_user.event_creator,False)
        

    def test_create_event_creator(self):
        self.input_dict['password'] = "password"        
        pss_user,pss_user_dict = self.pss_users_proxy.create_event_creator(self.input_dict)                                                
        self.assertEqual(pss_user.event_creator,True)
        self.assertEqual(pss_user,self.pss_user_mock)        
        self.assertEqual(pss_user_dict,self.input_dict)        
    
    def get_pss_users_for_event(self):
        pass

import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from proxies.PssUsersProxy import PssUsersProxy

class PssUsersProxyTest(PssUnitTestBase):
    def setUp(self):
        self.pss_user_mock = MagicMock()        
        self.db_handle_mock = MagicMock()
        self.pss_user_model_mock = MagicMock()        
        self.deserializer_mock = MagicMock()                

    def test_get_pss_users_with_invalid_pss_user_id(self):                        
        self.pss_user_model_mock.query.filter_by().first.return_value=None
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,
                                             self.deserializer_mock,                                             
                                             model=self.pss_user_model_mock)
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(pss_user_id=1)
        self.assertEqual(pss_user,None)
        self.pss_user_model_mock.query.filter_by.assert_called_with(pss_user_id=1)        
        self.assertEqual(pss_user_dict,None)

    def test_get_pss_user_by_pss_user_id_with_serializer(self):
        test_dict = {'test_value':'value'}                
        self.pss_user_mock.to_dict.return_value=test_dict
        self.pss_user_model_mock.query.filter_by().first.return_value=self.pss_user_mock
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,
                                             self.deserializer_mock,
                                             model=self.pss_user_model_mock)
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(pss_user_id=1)
        self.assertEqual(pss_user,self.pss_user_mock)
        self.pss_user_model_mock.query.filter_by.assert_called_with(pss_user_id=1)        
        self.assertEqual(pss_user_dict,test_dict)

    def test_get_pss_user_by_pss_username_with_serializer(self):
        test_dict = {'test_value':'value'}                
        self.pss_user_mock.to_dict.return_value=test_dict
        self.pss_user_model_mock.query.filter_by().first.return_value=self.pss_user_mock
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,
                                             self.deserializer_mock,
                                             model=self.pss_user_model_mock)
        pss_user,pss_user_dict = self.pss_users_proxy.get_pss_user(username='poop')
        self.assertEqual(pss_user,self.pss_user_mock)
        self.pss_user_model_mock.query.filter_by.assert_called_with(username='poop')        
        self.assertEqual(pss_user_dict,test_dict)

    def test_create_pss_user(self):
        pass

    def get_pss_users_for_event(self):
        pass

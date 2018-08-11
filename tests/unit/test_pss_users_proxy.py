import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from proxies.PssUsersProxy import PssUsersProxy
from proxies.TableProxy import PssDeserializers

class PssUsersProxyTest(PssUnitTestBase):
    def setUp(self):
        self.pss_user_mock = MagicMock()
        self.pss_user_dict_mock = {}
        self.db_handle_mock = MagicMock()
        self.model_mock = MagicMock()
        self.serializer_mock = MagicMock()                

    def initialize_pss_model_query_and_serializer_mocks(self,query_results,serializer_result):
        self.model_mock.query.filter_by().first.return_value=query_results
        self.serializer_mock.pss_user_schema.dump().data=serializer_result
    
    def test_get_pss_user_with_invalid_pss_user_id(self):
        self.initialize_pss_model_query_and_serializer_mocks(None,None)
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,self.serializer_mock,model=self.model_mock)
        fake_pss_user_returned,fake_pss_user_returned_dict = self.pss_users_proxy.get_pss_user(pss_user_id=999)        
        self.assertEquals(fake_pss_user_returned_dict,None)
        self.assertEquals(fake_pss_user_returned,None)        
        self.model_mock.query.filter_by.assert_called_with(pss_user_id=999)        
        
    def test_get_pss_user_by_id_with_serializer(self):
        self.initialize_pss_model_query_and_serializer_mocks(self.pss_user_mock,self.pss_user_dict_mock)
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,self.serializer_mock,model=self.model_mock)
        fake_pss_user_returned,fake_pss_user_returned_dict = self.pss_users_proxy.get_pss_user(pss_user_id=1)        
        self.assertEquals(fake_pss_user_returned_dict,self.pss_user_dict_mock)
        self.assertEquals(fake_pss_user_returned,self.pss_user_mock)        
        self.model_mock.query.filter_by.assert_called_with(pss_user_id=1)
        self.serializer_mock.pss_user_schema.dump.assert_called_with(self.pss_user_mock)
        
    def test_get_pss_username_with_serializer(self):
        self.initialize_pss_model_query_and_serializer_mocks(self.pss_user_mock,self.pss_user_dict_mock)
        self.pss_users_proxy = PssUsersProxy(self.db_handle_mock,self.serializer_mock,model=self.model_mock)
        fake_pss_user_returned,fake_pss_user_returned_dict = self.pss_users_proxy.get_pss_user(username='aitong')        
        self.assertEquals(fake_pss_user_returned_dict,self.pss_user_dict_mock)
        self.assertEquals(fake_pss_user_returned,self.pss_user_mock)        
        self.model_mock.query.filter_by.assert_called_with(username='aitong')
        self.serializer_mock.pss_user_schema.dump.assert_called_with(self.pss_user_mock)
 

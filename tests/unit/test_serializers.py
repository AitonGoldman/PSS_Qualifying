import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.serialization.PssUserSchema import gen_pss_users_schema
from lib.serialization.PssUserSchema import gen_pss_users_event_roles_schema
from lib.serialization.PssEventsSchema import gen_events_schema
from lib.serialization.PssEventRolesSchema import gen_event_roles_schema

class SerializersTest(PssUnitTestBase):
    def setUp(self):
        self.fake_model = MagicMock()
    
    def test_smoke_test_pss_user_serializer(self):                
        pss_user_dict = gen_pss_users_schema(self.fake_app,
                                             None,
                                             pss_model=self.fake_pss_users_model).dump(self.fake_model).data
        self.assertIsInstance(pss_user_dict,dict)
        self.assertTrue(pss_user_dict.get('event_roles_for_user',None) is not None)        

    def test_password_removed_by_pss_user_serializer(self):                
        pss_user_dict = gen_pss_users_schema(self.fake_app,
                                             None,
                                             pss_model=self.fake_pss_users_model).dump(self.fake_model).data
        self.assertTrue(pss_user_dict.get('password',None) is None)

    def test_smoke_test_pss_user_event_roles_serializer(self):
        pss_user_event_roles_dict = gen_pss_users_event_roles_schema(self.fake_app,
                                                                     None,
                                                                     pss_model=self.fake_pss_users_event_roles_model).dump(self.fake_model).data
        self.assertIsInstance(pss_user_event_roles_dict,dict)
        self.assertTrue(pss_user_event_roles_dict.get('events',None) is not None)                
        self.assertTrue(pss_user_event_roles_dict.get('event_roles',None) is not None)                
        
    def test_smoke_test_events_serializer(self):                
        events_dict = gen_events_schema(self.fake_app,
                                          None,
                                          pss_model=self.fake_events_model).dump(self.fake_model).data
        self.assertIsInstance(events_dict,dict)
        
    def test_smoke_test_event_roles_serializer(self):                
        event_roles_dict = gen_event_roles_schema(self.fake_app,
                                                  None,
                                                  pss_model=self.fake_event_roles_model).dump(self.fake_model).data
        self.assertIsInstance(event_roles_dict,dict)
        


    

import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from proxies.EventsProxy import EventsProxy
from flask_restless.helpers import to_dict

class EventsProxyTest(PssUnitTestBase):
    def setUp(self):
        self.db_handle_mock = MagicMock()
        self.mock_event = MagicMock()
        self.event_model_mock = MagicMock()                        
    
    def test_get_event_with_invalid_event_id(self):                        
        self.event_model_mock.query.filter_by().first.return_value=None
        self.events_proxy = EventsProxy(self.db_handle_mock,
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.get_event(1)
        self.assertEqual(event,None)
        self.event_model_mock.query.filter_by.assert_called_with(event_id=1)        
        self.assertEqual(event_dict,None)
        
    def test_get_event(self):                
        dict_to_return = {}
        self.mock_event.to_dict.return_value=dict_to_return
        self.event_model_mock.query.filter_by().first.return_value=self.mock_event
        
        self.events_proxy = EventsProxy(self.db_handle_mock,                                        
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.get_event(1)
        self.assertEqual(event,self.mock_event)
        self.event_model_mock.query.filter_by.assert_called_with(event_id=1)
        self.assertEqual(event_dict,dict_to_return)
        
                

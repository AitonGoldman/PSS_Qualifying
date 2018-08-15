import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from proxies.EventsProxy import EventsProxy

class EventsProxyTest(PssUnitTestBase):
    def setUp(self):
        self.db_handle_mock = MagicMock()
        self.mock_event = MagicMock()
        self.event_model_mock = MagicMock()
        self.event_settings_model_mock = MagicMock()
        self.event_model_associations_mock = MagicMock()
        self.deserializer_mock = MagicMock()                
    
    def test_get_event_with_invalid_event_id(self):                        
        self.event_model_mock.query.filter_by().first.return_value=None
        self.events_proxy = EventsProxy(self.db_handle_mock,
                                        self.deserializer_mock,
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.get_event(event_id=1)
        self.assertEqual(event,None)
        self.event_model_mock.query.filter_by.assert_called_with(event_id=1)        
        self.assertEqual(event_dict,None)
        
    def test_get_event_with_event_id(self):        
        test_dict = {'test_value':'value'}        
        self.mock_event.to_dict.return_value=test_dict
        self.event_model_mock.query.filter_by().first.return_value=self.mock_event
        self.events_proxy = EventsProxy(self.db_handle_mock,
                                        self.deserializer_mock,
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.get_event(event_id=1)
        self.assertEqual(event,self.mock_event)
        self.event_model_mock.query.filter_by.assert_called_with(event_id=1)
        self.assertDictEqual(event_dict,test_dict)
        self.assertEqual(event_dict,test_dict)

    def test_get_event_with_event_name(self):        
        test_dict = {'test_value':'value'}        
        self.mock_event.to_dict.return_value=test_dict
        self.event_model_mock.query.filter_by().first.return_value=self.mock_event
        self.events_proxy = EventsProxy(self.db_handle_mock,
                                        self.deserializer_mock,
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.get_event(event_name='test_event')
        self.assertEqual(event,self.mock_event)
        self.event_model_mock.query.filter_by.assert_called_with(event_name='test_event')
        self.assertDictEqual(event_dict,test_dict)
        self.assertEqual(event_dict,test_dict)

    def test_create_event(self):        
        test_dict = {'event_name':'test_event'}                
        self.deserializer_mock.event_schema.load().data=self.mock_event
        self.events_proxy = EventsProxy(self.db_handle_mock,
                                        self.deserializer_mock,
                                        event_model=self.event_model_mock)
        event,event_dict = self.events_proxy.create_event(test_dict)
        self.assertEqual(event,self.mock_event)
        self.deserializer_mock.event_schema.load.assert_called_with(test_dict)        
        self.mock_event.to_dict.assert_called()
        self.db_handle_mock.session.add.assert_called_with(self.mock_event)

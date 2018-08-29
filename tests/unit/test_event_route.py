import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from routes.event import get_event
from flask_restless.helpers import to_dict
from werkzeug.exceptions import NotFound

class EventRouteTest(PssUnitTestBase):
    def setUp(self):
        self.table_proxy_mock = MagicMock()                
    
    def test_get_event(self):
        mock_event = MagicMock()
        serialized_event_to_return = {}        
        self.table_proxy_mock.events_proxy.get_event.return_value=(mock_event,serialized_event_to_return)
        returned_serialized_event = get_event(self.table_proxy_mock,1)
        self.assertEqual(returned_serialized_event,serialized_event_to_return)                
        
    def test_get_event_throws_exception_when_event_id_is_invalid(self):
        self.table_proxy_mock.events_proxy.get_event.return_value=(None,None)
        with self.assertRaises(NotFound):
            get_event(self.table_proxy_mock,1)
                    
 

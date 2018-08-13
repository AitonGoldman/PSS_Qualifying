from tests.integration import static_setup
from flask_restless.helpers import to_dict
import pytest
import json
import unittest
        
class IntegrationTestEvents(unittest.TestCase):
    def setUp(self):
        self.app = static_setup()
        
    def test_get_event(self):                
        client = self.app.test_client()
        event_instance = self.app.table_proxy.events_proxy.event_model(event_id=1,event_name='test_event')
        self.app.table_proxy.sqlAlchemyHandle.session.add(event_instance)
        self.app.table_proxy.commit_changes()
        rv = client.get('/event/1')
        self.assertEqual(rv.status,'200 OK')
        event_json = json.loads(rv.get_data(as_text=True))        
        self.assertDictEqual(event_json,{'data':to_dict(event_instance)})


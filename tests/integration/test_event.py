import unittest
from tests.integration import static_setup
import json 

import pytest
        
class IntegrationTestEvents(unittest.TestCase):
    def setUp(self):
        self.app = static_setup()
        
    def test_get_event(self):                
        client = self.app.test_client()
        event_instance = self.app.table_proxy.events_proxy.event_model(event_id=1,event_name='test_event')
        event_setting_instance = self.app.table_proxy.event_settings_proxy.event_settings_model(event_setting_id=1,event_setting_name='test_setting')        
        event_settings_mapping_instance = self.app.table_proxy.event_settings_association(extra_data='poop')
        event_settings_mapping_instance.event_setting=event_setting_instance
        event_instance.event_settings_values = [event_settings_mapping_instance]        
        self.app.table_proxy.sqlAlchemyHandle.session.add(event_instance)
        self.app.table_proxy.commit_changes()
        rv = client.get('/event/1')
        self.assertEqual(rv.status,'200 OK')
        event_json = json.loads(rv.get_data(as_text=True))        
        self.assertDictEqual(event_json,{'data':event_instance.to_dict()})


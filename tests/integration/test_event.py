import json 
from tests.integration.pss_integration_test_base import PssIntegrationTestBase

class IntegrationTestEvents(PssIntegrationTestBase):

    def setUp(self):
        super(IntegrationTestEvents,self).setUp()
        self.event_creator_pss_user = self.create_user(event_creator=True)        
        self.flask_headers = self.login_user(self.event_creator_pss_user)            
        
    def test_get_event(self):                
        client = self.app.test_client()
        event_instance = self.create_event()
        rv = client.get('/event/%s'%event_instance.event_id)
        self.assertEqual(rv.status,'200 OK')
        event_json = json.loads(rv.get_data(as_text=True))        
        self.assertDictEqual(event_json,{'data':event_instance.to_dict()})
    
    def test_create_event(self):                                        
        event_name = self.generate_unique_name('test_event')                                
        rv = self.app.test_client().post('/event',
                                         headers=self.flask_headers,
                                         data=json.dumps({'event_name':event_name}))            
        self.assertEqual(rv.status,'200 OK')
        event_json = json.loads(rv.get_data(as_text=True))
        new_event,new_event_dict = self.app.table_proxy.events_proxy.get_event(event_name=event_name)
        self.assertTrue(new_event is not None)
        self.assertDictEqual(event_json,{'data':new_event_dict})
            

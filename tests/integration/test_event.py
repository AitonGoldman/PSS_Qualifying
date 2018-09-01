import json 
from tests.integration.pss_integration_test_base import PssIntegrationTestBase

class IntegrationTestEvents(PssIntegrationTestBase):

    def setUp(self):
        super(IntegrationTestEvents,self).setUp()
        self.event_creator_pss_user = self.create_user(event_creator=True)        
        self.flask_headers = self.login_user(self.event_creator_pss_user)            

    def post_pss_endpoint(self,endpoint,data):
        rv = self.app.test_client().post(endpoint,
                                         headers=self.flask_headers,
                                         data=json.dumps(data))        
        self.assertEqual(rv.status,'200 OK',str(rv.data))        
        return json.loads(rv.get_data(as_text=True))        

    def put_pss_endpoint(self,endpoint,data):
        rv = self.app.test_client().put(endpoint,
                                        headers=self.flask_headers,
                                        data=json.dumps(data))        
        self.assertEqual(rv.status,'200 OK',str(rv.data))        
        return json.loads(rv.get_data(as_text=True))        
    
    def get_pss_endpoint(self,endpoint):
        rv = self.app.test_client().get(endpoint,
                                        headers=self.flask_headers)        
        self.assertEqual(rv.status,'200 OK',str(rv.data))        
        return json.loads(rv.get_data(as_text=True))                        

    def create_event(self,data):
        return self.post_pss_endpoint('/event',data)['data']

    def update_event(self,data):
        return self.put_pss_endpoint('/event',data)['data']

    def get_event(self,event_id):
        return self.get_pss_endpoint('/event/%s' % event_id)['data']        
    
    def get_event_template(self):
        return self.get_pss_endpoint('/event_template')['data']        
    
    def test_get_event(self):                                        
        event_name = self.generate_unique_name('test_event')
        event_instance = self.create_event({'event_name':event_name})
        event_json = self.get_event(event_instance['event_id'])
        self.assertDictEqual(event_json,event_instance)        
        
    def test_create_event(self):                                        
        event_name = self.generate_unique_name('test_event')        
        event_json_template = {}
        event_json_template['event_name']=event_name
        event_json = self.create_event(event_json_template)        
        new_event,new_event_dict = self.app.table_proxy.events_proxy.get_event(event_name=event_name)
        self.assertTrue(new_event is not None)
        self.assertDictEqual(event_json,new_event_dict)

    def test_update_event(self):                                        
        event_name = self.generate_unique_name('test_event')
        self.app.table_proxy.event_settings_proxy.create_event_setting("string_test_setting","test setting")
        self.app.table_proxy.commit_changes()        
        event_json_template = {}
        event_json_template['event_name']=event_name        
        event_json = self.create_event(event_json_template)        
        event_json['event_settings_values'][0]['extra_data']="poop"        
        updated_event_json = self.update_event(event_json)                
        self.assertTrue(event_json['event_settings_values'][0]['extra_data']=="poop")
        
        

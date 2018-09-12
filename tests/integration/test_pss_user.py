import json 
from tests.integration.pss_integration_test_base import PssIntegrationTestBase

class IntegrationTestPssUsers(PssIntegrationTestBase):

    def setUp(self):
        super(IntegrationTestPssUsers,self).setUp()
        self.event_creator_pss_user = self.create_user(event_creator=True)        
        self.flask_headers = self.login_user(self.event_creator_pss_user)            

    def create_event_creator(self,data):
        return self.post_pss_endpoint('/event_creator',data)['data']
        
    def create_pss_user(self,data,event_id,role_id):
        return self.post_pss_endpoint('/event/%s/pss_user/role/%s' % (event_id,role_id),data)['data']

    def update_pss_user(self,data,event_id):
        return self.put_pss_endpoint('/event/%s/pss_user' % event_id,data)['data']

    def test_create_event_creator(self):
        last_name = self.generate_unique_name('testerson')
        new_event_creator_dict = self.create_event_creator({'first_name':'test',
                                                            'last_name':'%s'% last_name,
                                                            'password':'test_password'})                
        self.assertEqual(new_event_creator_dict['username'],'test%s' % last_name)
        self.assertTrue(new_event_creator_dict['event_creator'],True)
        self.assertIsNone(new_event_creator_dict.get('crypt_password',None))

        self.assertIsNotNone(new_event_creator_dict['pss_user_id'],None)
        new_event_creator,new_event_creator_dict_from_db = self.app.table_proxy.pss_users.get_pss_user(pss_user_id=new_event_creator_dict.get('pss_user_id',None))
        self.assertIsNotNone(new_event_creator)
        self.assertDictEqual(new_event_creator_dict_from_db,new_event_creator_dict)
        
    def test_create_pss_user(self):
        new_role = self.app.table_proxy.event_roles.event_roles_model(event_role_name='POOP_ROLE')                
        self.app.table_proxy.sqlAlchemyHandle.session.add(new_role)        
        self.app.table_proxy.commit_changes()
        new_role_id = new_role.event_role_id
        event_name = self.generate_unique_name('test_event')                
        event_json_template = {}
        event_json_template['event_name']=event_name        
        event_json = self.create_event(event_json_template)        
        last_name = self.generate_unique_name('testerson')
        new_pss_user_dict = self.create_pss_user({'first_name':'test',
                                                  'last_name':'%s'% last_name,
                                                  'password':'test_password'},
                                                 event_json['event_id'],
                                                 new_role_id)                
        self.assertEqual(new_pss_user_dict['username'],'test%s' % last_name)
        self.assertFalse(new_pss_user_dict.get('event_creator',None))
        self.assertIsNone(new_pss_user_dict.get('crypt_password',None))
        self.assertIsNotNone(new_pss_user_dict['pss_user_id'],None)
        self.assertEqual(len(new_pss_user_dict['event_roles_for_user']),1)
        
    
    def test_update_pss_user(self):
        new_role = self.app.table_proxy.event_roles.event_roles_model(event_role_name='POOP_ROLE')        
        self.app.table_proxy.sqlAlchemyHandle.session.add(new_role)        
        new_role2 = self.app.table_proxy.event_roles.event_roles_model(event_role_name='POOP_ROLE_2')        
        self.app.table_proxy.sqlAlchemyHandle.session.add(new_role2)
        self.app.table_proxy.commit_changes()
        new_role_id = new_role.event_role_id        
        last_name = self.generate_unique_name('testerson')
        pss_user_json_template = {'username':'pooping',
                                  'first_name':'looping',
                                  'last_name':'%s'% last_name,
                                  'password':'test'}

        event_name = self.generate_unique_name('test_event')                
        event_json_template = {}
        event_json_template['event_name']=event_name        
        event_json = self.create_event(event_json_template)        

        event_name_2 = self.generate_unique_name('test_event')                
        event_json_template_2 = {}
        event_json_template_2['event_name']=event_name_2        
        event_json_2 = self.create_event(event_json_template_2)        
        
        pss_user_json = self.create_pss_user(pss_user_json_template,event_json['event_id'],new_role_id)                        
        
        pss_user_json['event_roles_for_user'].append({'event_id':event_json_2['event_id'],'event_role_id':new_role_id,'pss_user_id':pss_user_json['pss_user_id']})
        updated_pss_user_json = self.update_pss_user(pss_user_json,event_json_2['event_id'])                
        self.assertEqual(len(updated_pss_user_json['event_roles_for_user']),2)
        self.assertEqual(updated_pss_user_json['event_roles_for_user'][0]['event_id'],event_json['event_id'])
        self.assertEqual(updated_pss_user_json['event_roles_for_user'][1]['event_id'],event_json_2['event_id'])
        

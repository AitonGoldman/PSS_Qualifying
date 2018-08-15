from tests.integration import static_setup
import unittest
import json 
import time


class PssIntegrationTestBase(unittest.TestCase):

    def create_user(self,event_creator=False):
        username = self.generate_unique_name('test_user')
        pss_user = self.app.table_proxy.pss_users.pss_users_model(username=username,
                                                                  first_name='first',
                                                                  last_name=self.generate_unique_name('last'),
                                                                  event_creator=event_creator)
        pss_user.crypt_password('test_user_password')
        self.app.table_proxy.sqlAlchemyHandle.session.add(pss_user)
        self.app.table_proxy.commit_changes()
        return pss_user
    
    def create_event(self):
        event_instance = self.app.table_proxy.events_proxy.event_model(event_name=self.generate_unique_name('test_event'))
        self.app.table_proxy.sqlAlchemyHandle.session.add(event_instance)
        self.app.table_proxy.commit_changes()                        
        return event_instance
    
    def login_user(self,pss_user):
        rv = self.app.test_client().put('/login_user',
                                        data=json.dumps({'username':pss_user.username,
                                                         'password':'test_user_password'}))
        return {'Cookie':'session=%s'% self.get_set_cookie_header(rv.headers)}
            
    def setUp(self):    
        self.app = static_setup()
        
    def generate_unique_name(self,name):
        millis = int(round(time.time() * 1000))
        return "%s_%s" %(name,millis)

    def get_set_cookie_header(self,headers):                
        cookie_header = headers.get('Set-Cookie',None)
        if cookie_header:
            return cookie_header.split(';')[0].split('=')[1]
        else:
            return None
        

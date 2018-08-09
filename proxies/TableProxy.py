from proxies.EventsProxy import EventsProxy
from proxies.EventRolesProxy import EventRolesProxy
from proxies.EventSettingsProxy import EventSettingsProxy
from proxies.PssUsersProxy import PssUsersProxy

from models.EventSettingsAssociation import generate_event_settings_association_model
from models.PssUsersEventRolesMappings import generate_pss_users_event_roles_mappings_model

from lib.serialization.PssUserSchema import gen_pss_users_schema
from lib.serialization.PssEventsSchema import gen_events_schema
from lib.serialization.PssEventRolesSchema import gen_event_roles_schema

class PssDeserializers():
    def __init__(self,app,table_proxy):
        self.app = app
        self.table_proxy = table_proxy
        
    def buildDeserializers(self):
        self.pss_user_schema = gen_pss_users_schema(self.app,self.table_proxy)
        self.events_schema = gen_events_schema(self.app,self.table_proxy)
        self.event_roles_schema = gen_event_roles_schema(self.app,self.table_proxy)
    
class TableProxy():
    def __init__(self, sqlAlchemyHandle, app):
        self.pssDeserializers = PssDeserializers(app,self)
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.events_proxy = EventsProxy(self.sqlAlchemyHandle)
        self.event_settings_proxy = EventSettingsProxy(self.sqlAlchemyHandle)
        self.event_roles =  EventRolesProxy(self.sqlAlchemyHandle)
        self.pss_users_event_roles = generate_pss_users_event_roles_mappings_model(self.sqlAlchemyHandle)
        self.pss_users = PssUsersProxy(self.sqlAlchemyHandle,self.pssDeserializers)                
        self.event_settings_association = generate_event_settings_association_model(self.sqlAlchemyHandle)                  
        self.pssDeserializers.buildDeserializers()
        
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        

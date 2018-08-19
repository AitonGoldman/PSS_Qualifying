from proxies.EventsProxy import EventsProxy
from proxies.EventSettingsProxy import EventSettingsProxy

from proxies.EventRolesProxy import EventRolesProxy
from proxies.PssUsersProxy import PssUsersProxy
from models.PssUsersEventRolesMappings import generate_pss_users_event_roles_mappings_model
from models.EventSettingsAssociation import generate_event_settings_association_model
from lib.PssSchema import PssSchemaBuilder
import sqlalchemy

class PssDeserializers():
    def __init__(self,app,table_proxy):
        self.app = app
        self.table_proxy = table_proxy        

    def buildDeserializers(self):        
        self.event_schema = PssSchemaBuilder(self.app,"Events",self.table_proxy.events_proxy.event_model).get_serializer()                
        self.pss_user_schema = PssSchemaBuilder(self.app,"PssUsers",self.table_proxy.pss_users.pss_users_model).get_serializer()                
        pass
    
class TableProxy():
    def __init__(self, sqlAlchemyHandle, app):
        self.sqlAlchemyHandle = sqlAlchemyHandle                
        self.pssDeserializers = PssDeserializers(app,self)
        self.event_settings_proxy = EventSettingsProxy(self.sqlAlchemyHandle)
        self.event_settings_association = generate_event_settings_association_model(self.sqlAlchemyHandle)                  
        self.events_proxy = EventsProxy(self.sqlAlchemyHandle,
                                        #self.event_settings_proxy,
                                        #self.event_settings_association,
                                        self,
                                        self.pssDeserializers)
        self.event_roles =  EventRolesProxy(self.sqlAlchemyHandle)
        self.pss_users_event_roles = generate_pss_users_event_roles_mappings_model(self.sqlAlchemyHandle)
        self.pss_users = PssUsersProxy(self.sqlAlchemyHandle,self.pssDeserializers)                
        self.pssDeserializers.buildDeserializers()
        
    def commit_changes(self):
        try:
            self.sqlAlchemyHandle.session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            return False

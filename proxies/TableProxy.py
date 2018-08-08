from proxies.EventsProxy import EventsProxy
from proxies.EventRolesProxy import EventRolesProxy
from proxies.EventSettingsProxy import EventSettingsProxy
from proxies.PssUsersProxy import PssUsersProxy

from models.EventSettingsAssociation import generate_event_settings_association_model
from models.PssUsersEventRolesMappings import generate_pss_users_event_roles_mappings_class

class TableProxy():
    def __init__(self,sqlAlchemyHandle):
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_settings_association = generate_event_settings_association_model(self.sqlAlchemyHandle)
        self.events = EventsProxy(self.sqlAlchemyHandle)                                        
        self.event_settings = EventSettingsProxy(self.sqlAlchemyHandle)
        self.event_roles = EventRolesProxy(self.sqlAlchemyHandle)
        self.pss_users = PssUsersProxy(self.sqlAlchemyHandle)
        self.pss_users_event_roles_mappings = generate_pss_users_event_roles_mappings_class(self.sqlAlchemyHandle)
        
    
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        

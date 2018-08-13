from proxies.EventsProxy import EventsProxy
from proxies.EventRolesProxy import EventRolesProxy
from proxies.PssUsersProxy import PssUsersProxy
from models.PssUsersEventRolesMappings import generate_pss_users_event_roles_mappings_model
                                     
class TableProxy():
    def __init__(self, sqlAlchemyHandle, app):
        self.sqlAlchemyHandle = sqlAlchemyHandle                
        self.events_proxy = EventsProxy(self.sqlAlchemyHandle)
        self.event_roles =  EventRolesProxy(self.sqlAlchemyHandle)
        self.pss_users_event_roles = generate_pss_users_event_roles_mappings_model(self.sqlAlchemyHandle)
        self.pss_users = PssUsersProxy(self.sqlAlchemyHandle)                
        
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        

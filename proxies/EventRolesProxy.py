from models.EventRoles import generate_event_roles_class

class EventRolesProxy():
    def __init__(self,sqlAlchemyHandle):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_roles = generate_event_roles_class(self.sqlAlchemyHandle)
        
    def get_event_roles(self):        
        pass        

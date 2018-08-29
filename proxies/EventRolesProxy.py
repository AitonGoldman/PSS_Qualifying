from models.EventRoles import generate_event_roles_model

class EventRolesProxy():
    def __init__(self,sqlAlchemyHandle):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_roles_model = generate_event_roles_model(self.sqlAlchemyHandle)
        
    def get_event_roles(self):        
        pass        

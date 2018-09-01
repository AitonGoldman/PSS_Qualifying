from models.EventRoles import generate_event_roles_model

class EventRolesProxy():
    def __init__(self,sqlAlchemyHandle):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_roles_model = generate_event_roles_model(self.sqlAlchemyHandle)
    
    def get_event_roles(self,serialized=True):        
        event_roles = self.event_roles_model.query.all()        
        if serialized:
            if len(event_roles)==0:
                return [],[]
            else:
                return event_roles,[event_role.to_dict() for event_role in event_roles]
        else:
            return event_roles 

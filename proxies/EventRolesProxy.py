from models.EventRoles import generate_event_roles_model

class EventRolesProxy():
    def __init__(self,sqlAlchemyHandle):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_roles_model = generate_event_roles_model(self.sqlAlchemyHandle)

    #TODO : need a create_event_role, but it only gets called up bootstrap/update script or tests
    def get_event_roles(self,serialized=True):        
        event_roles = self.event_roles_model.query.all()        
        if serialized:
            if len(event_roles)==0:
                return [],[]
            else:
                return event_roles,[event_role.to_dict() for event_role in event_roles]
        else:
            return event_roles 

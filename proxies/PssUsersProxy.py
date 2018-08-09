from models.PssUsers import generate_pss_users_class


class PssUsersProxy():
    def __init__(self,sqlAlchemyHandle,pssDeserializers=None):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.pssDeserializers=pssDeserializers
        self.pss_users = generate_pss_users_class(self.sqlAlchemyHandle)            
        
    def filter_event_roles_for_event(self, event_roles, event_id):
        return [event_role for event_role in event_roles if event_role.event_id == event_id]
    
    def get_pss_users(self):        
        pass
    
    def get_pss_user_for_event(self, event_id, pss_user_id=None, username=None):        
        if username:
            query = self.pss_users.query.filter_by(username=username)
        else:
            query = self.pss_users.query.filter_by(pss_user_id=pss_user_id)
        return self.pssDeserializers.pss_user_schema().dump(query.first()).data
        #return query.first()
    
    def get_global_pss_user(self):
        pass

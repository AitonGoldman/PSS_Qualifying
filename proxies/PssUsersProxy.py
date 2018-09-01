from models.PssUsers import generate_pss_users_model

class PssUsersProxy():
    SERIALIZE_FULL_PSS_USER=['-password_crypt']
    def __init__(self,
                 sqlAlchemyHandle,
                 table_proxy,
                 model=None):
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.table_proxy = table_proxy
        self.pssDeserializers = self.table_proxy.pssDeserializers
        self.pss_users_model = generate_pss_users_model(self.sqlAlchemyHandle) if model is None else model

    #TODO : implement tests
    def get_pss_users_for_event(self,event_id,serialized=True):        
        users_in_events = self.pss_users_model.query.filter(self.table_proxy.pss_users_event_roles.event_id==event_id).all()
        if serialized:
            if len(users_in_events)==0:
                return [],[]
            else:
                return users_in_events,[user.to_dict() for user in users_in_events]
        else:
            return users_in_events 
        
    #TODO : tests    
    def create_pss_user(self,pss_user_data,serialized=True):        
        new_pss_user = self.pssDeserializers.pss_user_schema.deserialize(pss_user_data)
        self.pssDeserializers.event_schema.check_deserialize_failures(new_pss_user)        

        if serialized:            
            return (new_pss_user.data, new_pss_user.data.to_dict()) if new_pss_user.data else (None,None)
        else:
            return new_pss_user.data

    #TODO : tests    
    def get_pss_user_template(self):
        pss_users_model_template = self.pss_users_model()        
        return pss_users_model_template.to_dict()
    
    def get_pss_user(self,
                     pss_user_id=None,
                     username=None,
                     serialized=True):
        if username:
            query = self.pss_users_model.query.filter_by(username=username)
        else:
            query = self.pss_users_model.query.filter_by(pss_user_id=pss_user_id)
        pss_user = query.first()
        if serialized:
            if pss_user is None:
                return None,None            
            dict_to_return = pss_user.to_dict(extend=self.SERIALIZE_FULL_PSS_USER)
            return pss_user,dict_to_return
        else:
            return pss_user if pss_user else None

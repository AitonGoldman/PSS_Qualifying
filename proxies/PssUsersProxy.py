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

    #TODO : implement
    def get_pss_users(self):
        pass

    #TODO : implement
    def register_pss_user_for_event(self):
        pass
    
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
            return pss_user

from models.PssUsers import generate_pss_users_model

class PssUsersProxy():
    def __init__(self,sqlAlchemyHandle,pssDeserializers,model=None):
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.pssDeserializers=pssDeserializers
        self.pss_users_model = generate_pss_users_model(self.sqlAlchemyHandle) if model is None else model

    def get_pss_users(self):
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
            dict_to_return = pss_user.to_dict()
            return pss_user,dict_to_return
        else:
            return pss_user

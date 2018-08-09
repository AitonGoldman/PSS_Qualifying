from models.PssUsers import generate_pss_users_model

class PssUsersProxy():
    def __init__(self,sqlAlchemyHandle,pssDeserializers=None):
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.pssDeserializers=pssDeserializers
        self.pss_users_model = generate_pss_users_model(self.sqlAlchemyHandle)

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
        if pss_user is None:
            return None
        if serialized:
            dict_to_return = self.pssDeserializers.pss_user_schema().dump(pss_user).data
            return pss_user,dict_to_return
        else:
            return pss_user

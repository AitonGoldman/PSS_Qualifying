from passlib.hash import sha512_crypt
from sqlalchemy_serializer import SerializerMixin

def generate_pss_users_model(db_handle):
    class PssUsers(db_handle.Model, SerializerMixin):
        pss_user_id = db_handle.Column(db_handle.Integer, primary_key=True)
        username = db_handle.Column(db_handle.String(80), unique=True, nullable=False)
        first_name = db_handle.Column(db_handle.String(80), nullable=False)
        last_name = db_handle.Column(db_handle.String(80), nullable=False)
        extra_title = db_handle.Column(db_handle.String(80))        
        password_crypt = db_handle.Column(db_handle.String(134))
        has_picture = db_handle.Column(db_handle.Boolean(),default=False)
        push_token=db_handle.Column(db_handle.String(500))
        event_creator=db_handle.Column(db_handle.Boolean)
        event_roles_for_user = db_handle.relationship('PssUsersEventRolesMappings',lazy="joined")

        def crypt_password(self, password):
            """Encrypt a plaintext password and store it"""
            self.password_crypt = sha512_crypt.encrypt(password)

        def verify_password(self, password):
            """Check to see if a plaintext password matches our crypt"""
            if self.password_crypt is None:
                return False
            else:
                return sha512_crypt.verify(password, self.password_crypt)

        def __repr__(self):            
            existing_user_name = self.first_name+" "+self.last_name
            if self.extra_title:
                existing_user_name = existing_user_name + " " + self.extra_title
            return existing_user_name

        @staticmethod
        def is_authenticated():
            """Users are always authenticated"""
            return True

        def is_active(self):
            # if self.event_user:
            #     return self.event_user.active
            # else:
            return True

        @staticmethod
        def is_anonymous():
            """No anon users"""
            return False

        def get_id(self):
            """Get the user's id"""
            return self.pss_user_id
    return PssUsers


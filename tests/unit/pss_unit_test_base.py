import unittest
from mock import MagicMock
from models.PssUsers import generate_pss_users_model
from models.Events import generate_event_model
from models.EventRoles import generate_event_roles_model
from models.PssUsersEventRolesMappings import generate_pss_users_event_roles_mappings_model
from models.EventSettings import generate_event_settings_model
from models.EventSettingsAssociation import generate_event_settings_association_model


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                                
        #FIXME : need constants for these strings                        
        self.fake_app = Flask('poop')
        self.fake_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
        self.db_handle = SQLAlchemy()
        self.fake_app.ma = Marshmallow(self.fake_app)

        self.fake_pss_users_model = generate_pss_users_model(self.db_handle)
        self.fake_pss_users_event_roles_model = generate_pss_users_event_roles_mappings_model(self.db_handle)        
        self.fake_event_roles_model = generate_event_roles_model(self.db_handle)
        self.fake_events_model = generate_event_model(self.db_handle)
        self.fake_event_settings_model=generate_event_settings_model(self.db_handle)
        self.fake_event_settings_association_model=generate_event_settings_association_model(self.db_handle)
            
    def create_mock_user(self,role_names,is_pss_admin_user=True):
        mock_user = MagicMock()        
        mock_user.admin_roles=[]
        mock_user.event_roles=[]
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)
            if is_pss_admin_user:
                mock_user.admin_roles.append(mock_role)
            else:
                mock_user.event_roles.append(mock_role)
                
        mock_user.verify_password.return_value=True            
        return mock_user
        
    def generate_mock_user_side_effect(self,side_effect_mock_user):
        def return_mock_user(*args,**kargs):            
            mock = MagicMock()
            if len(kargs) == 1:
                mock.first.return_value=None
            else:
                mock.first.return_value=side_effect_mock_user            
            return mock
        return return_mock_user
    # lib/customjsonencoder
    # lib/DbHelper
    # lib/DefaultJsonErrorHandler
    # lib DbHelper
    # 
    #

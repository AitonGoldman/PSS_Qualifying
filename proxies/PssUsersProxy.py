from models.PssUsers import generate_pss_users_model
from constants.serializers import SERIALIZE_FULL_PSS_USER
from proxies import TableProxyError

class PssUsersProxy():
    
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
    
    def create_event_creator(self,event_creator_dict,serialized=True):
        # TODO : check if existing event creator                
        new_event_creator = self.pssDeserializers.pss_user_schema.deserialize(event_creator_dict)
        self.pssDeserializers.event_schema.check_deserialize_failures(new_event_creator)                
        new_event_creator.data.event_creator=True        
        new_event_creator.data.crypt_password(event_creator_dict['password'])
        self.sqlAlchemyHandle.session.add(new_event_creator.data)

        if serialized:            
            return (new_event_creator.data, new_event_creator.data.to_dict()) if new_event_creator.data else (None,None)
        else:
            return new_event_creator.data 
       
    #TODO : tests    
    def update_pss_user(self,pss_user_dict,serialized=True):
        
        existing_user = self.get_pss_user(pss_user_id=pss_user_dict.get('pss_user_id',None),serialized=False)
        updated_user = self.pssDeserializers.pss_user_schema.deserialize(pss_user_dict,instance=existing_user)
        self.pssDeserializers.pss_user_schema.check_deserialize_failures(updated_user)
        
        if serialized:
            return (updated_user.data,updated_user.data.to_dict()) if updated_user.data else (None,None)
        else:
            return updated_user.data if updated_user.data else None
        
        
    def create_pss_user(self,pss_user_data,event_id=None,role_id=None,serialized=True):        
        #TODO : check for existing user before committing         
        pss_user_data.pop('event_roles_for_user',None)        
        event = self.table_proxy.events_proxy.get_event(event_id=event_id,serialized=False)
        if event is None:
            raise TableProxyError('No such event exists')
        event_role = next((event_role for event_role in self.table_proxy.event_roles.get_event_roles(serialized=False) if event_role.event_role_id==role_id),None)
        if event_role is None:
            raise TableProxyError("No such event role exists")
        new_pss_user = self.pssDeserializers.pss_user_schema.deserialize(pss_user_data)        
        self.pssDeserializers.event_schema.check_deserialize_failures(new_pss_user)
        new_pss_user.data.event_creator=False        
        if event_id:
            pss_users_event_roles_mapping = self.table_proxy.pss_users_event_roles()                        
            pss_users_event_roles_mapping.events=event
            pss_users_event_roles_mapping.event_roles=event_role
            new_pss_user.data.event_roles_for_user.append(pss_users_event_roles_mapping)
        new_pss_user.data.crypt_password(pss_user_data['password'])
        self.table_proxy.sqlAlchemyHandle.session.add(new_pss_user.data)
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
                     first_name=None,
                     last_name=None,
                     extra_title=None,
                     serialized=True):
        if username:
            query = self.pss_users_model.query.filter_by(username=username)
        if pss_user_id:
            query = self.pss_users_model.query.filter_by(pss_user_id=pss_user_id)
        if first_name:
            query = self.pss_users_model.query.filter_by(first_name=first_name,last_name=last_name)
            if extra_title:
                query = query.filter_by(extra_title=extra_title)
        pss_user = query.first()
        if serialized:
            if pss_user is None:
                return None,None            
            dict_to_return = pss_user.to_dict(extend=SERIALIZE_FULL_PSS_USER)
            return pss_user,dict_to_return
        else:
            return pss_user if pss_user else None

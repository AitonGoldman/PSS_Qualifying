from models.Events import generate_event_model
from proxies import TableProxyError
from constants.serializers import SERIALIZE_FULL_EVENT

class EventsProxy():

    def __init__(self,                 
                 sqlAlchemyHandle,
                 table_proxy,                 
                 event_model=None):                        
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.table_proxy = table_proxy
        self.pssDeserializers = table_proxy.pssDeserializers
        self.event_model=generate_event_model(self.sqlAlchemyHandle) if event_model is None else event_model
                
    def create_event(self,event_dict,serialized=True):                                    
        new_event = self.pssDeserializers.event_schema.deserialize(event_dict)        
        self.pssDeserializers.event_schema.check_deserialize_failures(new_event)
        self.sqlAlchemyHandle.session.add(new_event.data)

        if serialized:
            return (new_event.data, new_event.data.to_dict()) if new_event else (None, None)
        else:
            return new_event.data if new_event else None

    def update_event(self,event_dict,serialized=True):                                    
        existing_event = self.get_event(event_id=event_dict.get('event_id',None),serialized=False)
        if existing_event is None:
            return None        
        updated_event = self.pssDeserializers.event_schema.deserialize(event_dict,instance=existing_event)        
        
        if serialized:
            return (updated_event.data, updated_event.data.to_dict()) if existing_event else (None, None)
        else:
            return updated_event.data if update_event else None
        
    def get_event_setting(self,event_id,event_setting):
        event = self.get_event(event_id=event_id,serialized=False)
        if event is None:
            raise TableProxyError("Event does not exist")        
        event_setting_value = next((event_setting for event_setting in event.event_settings_values if event_setting.event_setting.event_setting_name == event_setting),None)        
        return event_setting_value.extra_data if event_setting_value else None       
    
    def get_event_template(self):
        event_model_template = self.event_model()        
        for event_setting in self.table_proxy.event_settings_proxy.get_event_settings(serialized=False):
            event_settings_association = self.table_proxy.event_settings_association()
            event_settings_association.event_setting=event_setting
            event_model_template.event_settings_values.append(event_settings_association)        
        return {key:value for key,value in event_model_template.to_dict().items() if "_id" not in key}
        
        
    #TODO : need unit test
    def get_events_created_by_user(self,pss_user_id,serialized=True):
        events = self.event_model.query.filter_by(event_creator_pss_user_id=pss_user_id).all()        
        if serialized:            
            if len(events)==0:
                return [],[]
            else:                
                return events,[event.to_dict() for event in events]
        else:
            return events 
        
    def get_event(self,event_id=None,serialized=True,event_name=None,serializer_type=None):
        if serializer_type is None:
            serializer_type = SERIALIZE_FULL_EVENT
        query = self.event_model.query
        if event_id:
            query = query.filter_by(event_id=event_id)
        else:
            query = query.filter_by(event_name=event_name)
        event = query.first()
        if serialized:
            if event:
                dict_to_return = event.to_dict(extend=serializer_type)                
                return event,dict_to_return
            else:
                return None,None
        else:
            return event  

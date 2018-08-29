from models.Events import generate_event_model
from lib.auth import permissions
import json

class EventsProxy():
    SERIALIZE_FULL_EVENT=[]
    SERIALIZE_EVENT_FOR_NON_EVENT_OWNER=[]    

    def __init__(self,                 
                 sqlAlchemyHandle,
                 table_proxy,
                 #event_settings_proxy,
                 #event_settings_associations_model,                 
                 pssDeserializers,
                 event_model=None):                        
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.table_proxy = table_proxy
        self.pssDeserializers = pssDeserializers
        self.event_model=generate_event_model(self.sqlAlchemyHandle) if event_model is None else event_model
                
    def create_event(self,event_dict,serialized=True):                                    
        new_event = self.pssDeserializers.event_schema.load(event_dict)        
        self.sqlAlchemyHandle.session.add(new_event.data)
        if serialized:
            return new_event.data, new_event.data.to_dict()
        else:
            return new_event.data

    def update_event(self,event_dict,serialized=True):                                    
        #TODO
        pass
    
    def get_event_setting(self,event_id,event_setting):
        event = self.get_event(event_id=event_id,serialized=False)
        if event is None:
            return None,None if serialized else None
        event_setting_value = next((event_setting for event_setting in event.event_settings_values if event_setting.event_setting.event_setting_name == event_setting),None)
        return event_setting_value.extra_data        
    
    def get_event_template(self):
        event_model_template = self.event_model()
        # FIXME : this should be a proxy        
        for event_setting in self.event_settings.get_event_settings(serialized=False):
            event_settings_association = self.table_proxy.event_settings_association()
            event_settings_association.event_setting=event_setting
            event_model_template.event_settings_values.append(event_settings_association)
        return event_model_template.to_dict()
    
    def get_event(self,event_id=None,serialized=True,event_name=None,serializer_type=None):
        if serializer_type=None:
            serializer_type = self.SERIALIZE_FULL_EVENT
        query = self.event_model.query
        if event_id:
            query = query.filter_by(event_id=event_id)
        else:
            query = query.filter_by(event_name=event_name)
        event = query.first()
        if serialized:
            if event is None:
                return None,None            
            dict_to_return = event.to_dict(extend=serializer_type)            
            return event,dict_to_return
        else:
            return event 

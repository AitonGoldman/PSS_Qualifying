from models.Events import generate_event_model

class EventsProxy():
    SERIALIZE_FULL_EVENT=[]
    SERIALIZE_EVENT_FOR_NON_EVENT_OWNER=[]    

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
        #TODO : check for errors on the new_event
        self.sqlAlchemyHandle.session.add(new_event.data)
        if serialized:
            return new_event.data, new_event.data.to_dict()
        else:
            return new_event.data

    def update_event(self,event_dict,serialized=True):                                    
        #TODO
        pass

    #TODO : change to get_event_setting_value()
    def get_event_setting(self,event_id,event_setting):
        event = self.get_event(event_id=event_id,serialized=False)
        if event is None:
            return None,None if serialized else None
        event_setting_value = next((event_setting for event_setting in event.event_settings_values if event_setting.event_setting.event_setting_name == event_setting),None)
        #TODO : check if event_setting_value is None 
        return event_setting_value.extra_data        
    
    def get_event_template(self):
        event_model_template = self.event_model()
        # FIXME : this should be a proxy        
        for event_setting in self.event_settings.get_event_settings(serialized=False):
            event_settings_association = self.table_proxy.event_settings_association()
            event_settings_association.event_setting=event_setting
            event_model_template.event_settings_values.append(event_settings_association)
        return event_model_template.to_dict()

    #TODO : need unit test
    def get_events_created_by_user(self,pss_user_id,serialized=True, serializer_type=None):
        if serializer_type is None:
            serializer_type = self.SERIALIZE_FULL_EVENT
        events = self.event_model.query.filter_by(event_creator_pss_user_id=pss_user_id).all()
        #TODO : check if events is actually none where there is no match
        if serialized:            
            if events is None:
                return [],[]
            else:                
                return [event.to_dict(extend=serializer_type) for event in events]
        else:
            return [event for event in events]
        
    def get_event(self,event_id=None,serialized=True,event_name=None,serializer_type=None):
        if serializer_type is None:
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

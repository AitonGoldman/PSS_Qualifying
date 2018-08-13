from models.Events import generate_event_model
from models.EventSettings import generate_event_settings_model
from models.EventSettingsAssociation import generate_event_settings_association_model

class EventsProxy():
    def __init__(self,                 
                 sqlAlchemyHandle,
                 event_settings_model,
                 event_settings_associations_model,                 
                 serializers,
                 event_model=None):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_model=generate_event_model(self.sqlAlchemyHandle) if event_model is None else event_model
        self.event_settings=event_settings_model,        
        self.event_settings_association=event_settings_associations_model,
        self.serializers = serializers
           
    def get_event(self,event_id,serialized=True):
        event = self.event_model.query.filter_by(event_id=event_id).first()
        if serialized:
            if event is None:
                return None,None            
            dict_to_return = event.to_dict()            
            return event,dict_to_return
        else:
            return event 

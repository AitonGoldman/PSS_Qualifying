from models.Events import generate_event_model
from lib.auth import permissions

class EventsProxy():
    SERIALIZE_FULL_EVENT=[]    
    def __init__(self,                 
                 sqlAlchemyHandle,
                 pssDeserializers,
                 event_model=None):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.pssDeserializers = pssDeserializers
        self.event_model=generate_event_model(self.sqlAlchemyHandle) if event_model is None else event_model

    def create_event(self,event_dict,serialized=True):                    
        new_event = self.pssDeserializers.event_schema.load(event_dict).data        
        self.sqlAlchemyHandle.session.add(new_event)
        if serialized:            
            return new_event,new_event.to_dict()
        else:
            return new_event
        
    def get_event_template(self):
        return self.event_model().to_dict()
    
    #FIXME : don't need the serialized option, since we always send back both
    def get_event(self,event_id=None,serialized=True,event_name=None):
        query = self.event_model.query
        if event_id:
            query = query.filter_by(event_id=event_id)
        else:
            query = query.filter_by(event_name=event_name)
        event = query.first()
        if serialized:
            if event is None:
                return None,None            
            dict_to_return = event.to_dict(extend=self.SERIALIZE_FULL_EVENT)            
            return event,dict_to_return
        else:
            return event 

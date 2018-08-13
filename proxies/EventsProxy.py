from models.Events import generate_event_model

class EventsProxy():
    def __init__(self,                 
                 sqlAlchemyHandle,
                 event_model=None):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_model=generate_event_model(self.sqlAlchemyHandle) if event_model is None else event_model
           
    def get_event(self,event_id,serialized=True):
        event = self.event_model.query.filter_by(event_id=event_id).first()
        if serialized:
            if event is None:
                return None,None            
            dict_to_return = event.to_dict()            
            return event,dict_to_return
        else:
            return event 

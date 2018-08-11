from models.Events import generate_event_model

class EventsProxy():
    def __init__(self,sqlAlchemyHandle):                
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_model=generate_event_model(self.sqlAlchemyHandle)
        
    def get_events(self):        
        pass

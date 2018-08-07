from models.Events import EventOperations
from models.EventSettings import EventSettingsOperations
from models.EventSettingsAssociation import generate_event_settings_association_model

class TableProxy():
    def __init__(self,sqlAlchemyHandle):
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_settings_association = generate_event_settings_association_model(self.sqlAlchemyHandle)
        self.events = EventOperations(sqlAlchemyHandle)                                        
        self.event_settings = EventSettingsOperations(sqlAlchemyHandle)
        
    
    def commit_changes(self):
        self.sqlAlchemyHandle.session.commit()
        

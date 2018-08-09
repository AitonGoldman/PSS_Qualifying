from models.EventSettings import generate_event_settings_model

class EventSettingsProxy():
    def __init__(self,sqlAlchemyHandle):        
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_settings_model=generate_event_settings_model(self.sqlAlchemyHandle)
        
    def get_event_settings(self):
        pass
        
    def add_event_setting(self,event_setting_name,commit=False):
        pass
    
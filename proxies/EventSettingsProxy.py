from models.EventSettings import generate_event_settings_model
from proxies import TableProxyError

class EventSettingsProxy():
    def __init__(self,sqlAlchemyHandle):        
        self.sqlAlchemyHandle = sqlAlchemyHandle
        self.event_settings_model=generate_event_settings_model(self.sqlAlchemyHandle)

    def get_event_settings(self,serialized=True):
        event_settings = self.event_settings_model.query.all()
        if serialized:
            if len(event_settings)==0:
                return [],[]
            return event_settings, [event_setting.to_dict() for event_setting in event_settings]
        else:
            return event_settings 
                    
    def create_event_setting(self,event_setting_name,event_setting_short_description,event_setting_long_description=None):
        event_setting_name_segments = event_setting_name.split("_")
        if len(event_setting_name_segments)==0:
            raise TableProxyError('Setting name does not have underscores')            
        if event_setting_name_segments[0] not in ['string','number','boolean']:
            raise TableProxyError('Setting type is not string, number, or boolean')            
        new_event_setting = self.event_settings_model(event_setting_name=event_setting_name,
                                                      event_setting_short_description=event_setting_short_description,
                                                      event_setting_long_description=event_setting_long_description)
        self.sqlAlchemyHandle.session.add(new_event_setting)                            
        return new_event_setting

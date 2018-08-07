class EventSettingsOperations():
    def __init__(self,sqlAlchemyHandle):
        self.event_settings_model=generate_event_settings_model(sqlAlchemyHandle)
        self.sqlAlchemyHandle = sqlAlchemyHandle
        
    def get_event_settings(self):
        return self.event_settings_model.query.all()
        
    def add_event_setting(self,event_setting_name,commit=False):
        new_event_setting = self.event_settings_model()
        new_event_setting.event_setting_name=event_setting_name
        self.sqlAlchemyHandle.session.add(new_event_setting)
        if commit:
            self.sqlAlchemyHandle.session.commit()
        return new_event_setting
    
def generate_event_settings_model(db):
    
    class EventSettings(db.Model):
        event_setting_id = db.Column(db.Integer, primary_key=True)
        event_setting_name = db.Column(db.String(80), unique=True, nullable=False)        

        def __repr__(self):
            return '<Event Setting %r>' % self.event_setting_name
    return EventSettings


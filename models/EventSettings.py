def generate_event_settings_model(db):    
    class EventSettings(db.Model):
        event_setting_id = db.Column(db.Integer, primary_key=True)
        event_setting_name = db.Column(db.String(80), unique=True, nullable=False)        

        def __repr__(self):
            return '<Event Setting %r>' % self.event_setting_name
    return EventSettings


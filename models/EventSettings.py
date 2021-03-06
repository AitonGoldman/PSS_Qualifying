from sqlalchemy_serializer import SerializerMixin

def generate_event_settings_model(db):    
    class EventSettings(db.Model, SerializerMixin):
        event_setting_id = db.Column(db.Integer, primary_key=True)
        event_setting_name = db.Column(db.String(80), unique=True, nullable=False)
        event_setting_short_description = db.Column(db.String(80), nullable=False)
        event_setting_long_description = db.Column(db.String(80))
 
        def __repr__(self):
            return '<Event Setting %r>' % self.event_setting_name
    return EventSettings


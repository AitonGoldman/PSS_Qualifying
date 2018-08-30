from sqlalchemy_serializer import SerializerMixin

def generate_event_settings_model(db):    
    class EventSettings(db.Model, SerializerMixin):
        event_setting_id = db.Column(db.Integer, primary_key=True)
        event_setting_name = db.Column(db.String(80), unique=True, nullable=False) 
        # TODO : add a short description and full description of setting
        def __repr__(self):
            return '<Event Setting %r>' % self.event_setting_name
    return EventSettings


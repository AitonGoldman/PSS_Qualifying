from sqlalchemy_serializer import SerializerMixin

def generate_event_settings_association_model(db):    
    class EventSettingsAssociation(db.Model,SerializerMixin):
        event_setting_id = db.Column(db.Integer, db.ForeignKey('event_settings.event_setting_id'), primary_key=True)        
        event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), primary_key=True)
        extra_data = db.Column(db.String(50))
        event_setting = db.relationship('EventSettings',lazy="joined")
        
    return EventSettingsAssociation


from sqlalchemy.orm import joinedload,subqueryload
from sqlalchemy_serializer import SerializerMixin

def generate_event_model(db):
    class Events(db.Model,SerializerMixin):
        event_id = db.Column(db.Integer, primary_key=True)
        event_name = db.Column(db.String(80), unique=True, nullable=False)        
        event_settings_values = db.relationship("EventSettingsAssociation",lazy="joined")
        
        def __repr__(self):
            return '<Event %r>' % self.event_name        
    return Events


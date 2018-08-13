def generate_event_model(db):
    class Events(db.Model):
        event_id = db.Column(db.Integer, primary_key=True)
        event_name = db.Column(db.String(80), unique=True, nullable=False)                
        
        def __repr__(self):
            return '<Event %r>' % self.event_name        
    return Events


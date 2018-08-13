def generate_event_owners_events_mappings_class(db_handle):    
    class EventOwnersEventsMappings(db_handle.Model):        
        pss_user_id=db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'),primary_key=True)        
    return EventOwnersEventsMappings
    


from sqlalchemy_serializer import SerializerMixin

def generate_event_roles_model(db_handle):
    class EventRoles(db_handle.Model, SerializerMixin):
        event_role_id=db_handle.Column(db_handle.Integer,primary_key=True)
        event_role_name=db_handle.Column(db_handle.String(80))
    return EventRoles

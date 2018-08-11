from lib.serialization.PssEventsSchema import gen_events_schema
from lib.serialization.PssEventRolesSchema import gen_event_roles_schema

def gen_pss_users_event_roles_schema(app,table_proxy,pss_model=None) :
    class PssUsersEventRolesSchema(app.ma.ModelSchema):
        event_roles = app.ma.Nested(gen_event_roles_schema(app,table_proxy,pss_model))
        events = app.ma.Nested(gen_events_schema(app,table_proxy,pss_model))
        class Meta:
            model = table_proxy.pss_users_event_roles_model if pss_model is None else pss_model
    return PssUsersEventRolesSchema()

def gen_pss_users_schema(app,table_proxy,pss_model=None):
    class PssUsersSchema(app.ma.ModelSchema):
        event_roles_for_user = app.ma.Nested(gen_pss_users_event_roles_schema(app,table_proxy,pss_model),many=True)
        class Meta:
            model = table_proxy.pss_users.pss_users_model if pss_model is None else pss_model
    return PssUsersSchema(exclude='password')

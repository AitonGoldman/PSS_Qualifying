def gen_event_roles_schema(app,table_proxy,pss_model=None) :
    class EventRolesSchema(app.ma.ModelSchema):
        class Meta:
            model = table_proxy.event_roles.event_roles_model if pss_model is None else pss_model
    return EventRolesSchema()

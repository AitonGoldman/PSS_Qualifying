def gen_event_roles_schema(app,table_proxy) :
    class EventRolesSchema(app.ma.ModelSchema):
        class Meta:
            model = table_proxy.event_roles.event_roles_model
    return EventRolesSchema

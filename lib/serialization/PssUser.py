from flask import current_app

class PssUserSchema(current_app.ma.ModelSchema):
    class Meta:
        model = current_app.table_proxy.pss_users.pss_users

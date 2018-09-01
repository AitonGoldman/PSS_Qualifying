from app import create_app
from flask import Flask
from lib.DbHelper import DbHelper,POSTGRES_TYPE
from lib.auth import roles_constants
from decouple import config
import os,sys

if len(sys.argv) > 1:
    pss_db_name=sys.argv[1]    
else:
    print("didn't specify db name...")
    sys.exit(1)

real_app = create_app()

pss_db_type = config('pss_db_type',default='postgres')
pss_db_username = config('db_username')
pss_db_password = config('db_password')

db_helper = DbHelper(pss_db_type,pss_db_username,pss_db_password,pss_db_name)
db_helper.create_db_and_tables(real_app)
#TODO : use the proper events_proxy function to create a new event and user
new_user = real_app.table_proxy.pss_users.pss_users_model(username="testuser",first_name="test",last_name="user",event_creator=True)
new_user.crypt_password('test')
real_app.table_proxy.sqlAlchemyHandle.session.add(new_user)
real_app.table_proxy.commit_changes()

new_event_setting = real_app.table_proxy.event_settings_proxy.event_settings_model(event_setting_name="string_test")
new_event = real_app.table_proxy.events_proxy.event_model(event_name='test_event')
new_event_settings_association = real_app.table_proxy.event_settings_association()
new_event_settings_association.event_setting=new_event_setting
new_event.event_settings_values.append(new_event_settings_association)
new_event.event_creator_pss_user_id=new_user.pss_user_id
#TODO : need to create a tableproxy function to create event roles
new_role = real_app.table_proxy.event_roles.event_roles_model(event_role_name=roles_constants.EVENT_CREATOR)
real_app.table_proxy.sqlAlchemyHandle.session.add(new_event_setting)
real_app.table_proxy.sqlAlchemyHandle.session.add(new_event)
real_app.table_proxy.sqlAlchemyHandle.session.add(new_role)
real_app.table_proxy.commit_changes()

# pss_config.get_db_info().create_db_and_tables(real_app,True)
# db_handle = pss_config.get_db_info().create_db_handle(real_app)
# table_proxy=TableProxy()
# table_proxy.initialize_tables(db_handle)
# #bootstrap.bootstrap_pss_admin_event(tables,'pss_admin')
# #bootstrap.bootstrap_roles(tables)
# table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR)
# table_proxy.create_role(roles_constants.SCOREKEEPER)
# table_proxy.create_role(roles_constants.DESKWORKER)

# table_proxy.create_user('test_user_admin',
#                         'test_first_name',
#                         'test_last_name',
#                         admin_password,
#                         event_creator=True,
#                         commit=True)

# pss_config.get_db_info().load_machines_from_json(real_app,test=False,table_proxy=table_proxy)


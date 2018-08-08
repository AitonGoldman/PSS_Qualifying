from collections import namedtuple
from functools import partial
from lib.auth import roles_constants

PssNeedWithArgument = namedtuple('pss_route_need', ['method', 'value'])
PssNeedWithoutArgument = namedtuple('pss_route_need', ['method'])

EventCreatorRoleNeed = partial(PssNeedWithoutArgument, roles_constants.EVENT_CREATOR)
EventEditNeed = partial(PssNeedWithArgument, roles_constants.EVENT_CREATOR)

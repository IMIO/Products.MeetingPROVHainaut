# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# College
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.id = 'meeting-config-zcollege'
collegeMeeting.shortName = 'ZCollege'

# Council
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.id = 'meeting-config-zcouncil'
councilMeeting.shortName = 'ZCouncil'

data.meetingConfigs = (collegeMeeting, councilMeeting)

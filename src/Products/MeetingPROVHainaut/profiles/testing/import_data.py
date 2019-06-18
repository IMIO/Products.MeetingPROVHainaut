# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_testing_import_data

data = deepcopy(mc_testing_import_data.data)

# College
collegeMeeting = deepcopy(mc_testing_import_data.collegeMeeting)
collegeMeeting.id = 'meeting-config-zcollege'
collegeMeeting.shortName = 'ZCollege'
collegeMeeting.workflowAdaptations += ['meetingadvicefinances_add_advicecreated_state',
                                       'meetingadvicefinances_controller_propose_to_manager']

# Council
councilMeeting = deepcopy(mc_testing_import_data.councilMeeting)
councilMeeting.id = 'meeting-config-zcouncil'
councilMeeting.shortName = 'ZCouncil'

data.meetingConfigs = (collegeMeeting, councilMeeting)

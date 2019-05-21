# -*- coding: utf-8 -*-

from Globals import InitializeClass
from Products.MeetingCommunes.adapters import CustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingPROVHainaut.utils import compta_group_uid
from Products.MeetingPROVHainaut.utils import finance_group_uid
from Products.PloneMeeting.utils import duplicate_workflow


class CustomPROVHainautMeetingConfig(CustomMeetingConfig):
    ''' '''
    def updateExtraPortalTypes(self):
        """Manage finances related advices :
           WF :
           ====
           - create 'patched_meetingadvicefinances_workflow' from 'meetingadvicefinances_workflow'
             on which we applied relevant workflowAdaptations;
           - create 'meetingadvicecompta_workflow' from 'meetingadvicefinances_workflow';
           - create 'patched_meetingadvicecompta_workflow' from 'meetingadvicecompta_workflow'
             on which we applied relevant workflowAdaptations."""
        if self.context.getId() == 'meeting-config-zcollege':
            # WFs
            # duplicate and associate
            # patched_meetingadvicefinances_workflow
            duplicate_workflow(
                'meetingadvicefinances_workflow',
                'patched_meetingadvicefinances_workflow',
                portalTypeNames=['meetingadvicefinances'])
            # meetingadvicecompta_workflow
            duplicate_workflow('meetingadvicefinances_workflow', 'meetingadvicecompta_workflow')
            # patched_meetingadvicecompta_workflow
            duplicate_workflow(
                'meetingadvicecompta_workflow',
                'patched_meetingadvicecompta_workflow',
                portalTypeNames=['meetingadvicecompta'])


class CustomPROVHainautMeetingItem(CustomMeetingItem):
    ''' '''

    def __init__(self, item):
        self.context = item

    def _advicePortalTypeForAdviser(self, groupId):
        """ """
        if groupId == finance_group_uid():
            return "meetingadvicefinances"
        elif groupId == compta_group_uid():
            return "meetingadvicecompta"
        else:
            return "meetingadvice"


InitializeClass(CustomPROVHainautMeetingConfig)
InitializeClass(CustomPROVHainautMeetingItem)

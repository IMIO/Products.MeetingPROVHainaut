# -*- coding: utf-8 -*-

from Globals import InitializeClass
from plone import api
from Products.MeetingCommunes.adapters import CustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingPROVHainaut.utils import finance_group_uid


class CustomPROVHainautMeetingConfig(CustomMeetingConfig):
    ''' '''

    def mayEvaluateCompleteness(self):
        '''Completeness can be evaluated by the finance precontroller.'''
        # user must be a finance precontroller
        item = self.getSelf()
        if item.isDefinedInTool():
            return
        member = api.user.get_current()
        # bypass for Managers
        if member.has_role('Manager'):
            return True

        # relevant state?
        if not item.queryState() == 'proposed__or__prevalidated_waiting_advices':
            return False

        # finances advice asked?
        finance_group = finance_group_uid()
        finance_asked = finance_group not in item.adviceIndex
        if not finance_asked:
            return False

        # current user is pre-controller for asked advice?
        tool = api.portal.get_tool('portal_plonemeeting')
        userGroups = tool.get_plone_groups_for_user()
        if '%s_financialcontrollers' % finance_group not in userGroups:
            return False

        return True


class CustomPROVHainautMeetingItem(CustomMeetingItem):
    ''' '''

    def __init__(self, item):
        self.context = item

    def _advicePortalTypeForAdviser(self, groupId):
        """ """
        if groupId == finance_group_uid():
            return "meetingadvicefinances"
        else:
            return "meetingadvice"


InitializeClass(CustomPROVHainautMeetingConfig)
InitializeClass(CustomPROVHainautMeetingItem)

# -*- coding: utf-8 -*-

from Globals import InitializeClass
from plone import api
from Products.MeetingCommunes.adapters import CustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingPROVHainaut.utils import compta_group_uid
from Products.MeetingPROVHainaut.utils import finance_group_uid


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
        # XXX not needed, kept for now, until...
        return

        # if self.context.getId() == 'meeting-config-zcollege':
        #     fin_wf = 'meetingadvicefinances_workflow'
        #     patched_fin_wf = 'patched_meetingadvicefinances_workflow'
        #     compta_wf = 'meetingadvicecompta_workflow'
        #     patched_compta_wf = 'patched_meetingadvicecompta_workflow'
        #     # WFs
        #     # duplicate and associate
        #     # patched_meetingadvicefinances_workflow
        #     duplicate_workflow(fin_wf, patched_fin_wf, portalTypeNames=['meetingadvicefinances'])
        #     # meetingadvicecompta_workflow
        #     duplicate_workflow(fin_wf, compta_wf)
        #     # patched_meetingadvicecompta_workflow
        #     duplicate_workflow(compta_wf, patched_compta_wf, portalTypeNames=['meetingadvicecompta'])
        #     # adapt WF, change initial_state (and leading trnsition)
        #     # and remove states proposed_to_financial_controller/proposed_to_financial_editor
        #     change_transition_new_state_id(wf_id=patched_compta_wf,
        #                                    transition_id='backToAdviceInitialState',
        #                                    new_state_id='proposed_to_financial_reviewer')
        #     removeState(wf_id=patched_compta_wf,
        #                 state_id='proposed_to_financial_controller',
        #                 remove_leading_transitions=True,
        #                 new_initial_state='proposed_to_financial_reviewer')
        #     removeState(wf_id=patched_compta_wf,
        #                 state_id='proposed_to_financial_editor',
        #                 remove_leading_transitions=True)

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

        # finance/compta advice asked?
        finance_group = finance_group_uid()
        finance_asked = finance_group not in item.adviceIndex
        compta_group = compta_group_uid()
        compta_asked = compta_group not in item.adviceIndex
        if not finance_asked and not compta_asked:
            return False

        # current user is pre-controller for asked advice?
        tool = api.portal.get_tool('portal_plonemeeting')
        userGroups = tool.get_plone_groups_for_user()
        if (finance_asked and '%s_financialcontrollers' % finance_group not in userGroups) or \
           (compta_asked and '%s_financialcontrollers' % compta_group not in userGroups):
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
        elif groupId == compta_group_uid():
            return "meetingadvicecompta"
        else:
            return "meetingadvice"


InitializeClass(CustomPROVHainautMeetingConfig)
InitializeClass(CustomPROVHainautMeetingItem)

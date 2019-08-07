# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from collective.contact.plonegroup.utils import get_organization
from Globals import InitializeClass
from plone import api
from Products.MeetingCommunes.adapters import CustomMeetingConfig as MCCustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem as MCCustomMeetingItem
from Products.MeetingCommunes.adapters import customwfAdaptations
from Products.MeetingCommunes.adapters import MeetingAdviceCommunesWorkflowConditions
from Products.MeetingCommunes.utils import finances_give_advice_states
from Products.MeetingPROVHainaut.interfaces import IMeetingAdvicePROVHainautWorkflowConditions
from Products.MeetingPROVHainaut.utils import finance_group_uid
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model import adaptations
from zope.i18n import translate
from zope.interface import implements


# add finances advice related wfAdaptations
customwfAdaptations.append('meetingadvicefinances_add_advicecreated_state')
customwfAdaptations.append('meetingadvicefinances_controller_propose_to_manager')
MeetingConfig.wfAdaptations = customwfAdaptations

adaptations.WAITING_ADVICES_FROM_STATES = (
    {'from_states': ('proposedToValidationLevel1',
                     'proposedToValidationLevel2',
                     'proposedToValidationLevel3',
                     'proposedToValidationLevel4',
                     'proposedToValidationLevel5'),
     'back_states': ('proposedToValidationLevel1',
                     'proposedToValidationLevel2',
                     'proposedToValidationLevel3',
                     'proposedToValidationLevel4',
                     'proposedToValidationLevel5',
                     'validated'),
     'perm_cloned_states': ('validated',),
     'remove_modify_access': True,
     'use_custom_icon': False,
     'use_custom_back_transition_title_for': ('validated'),
     'use_custom_state_title': False,
     },
)


class MeetingAdvicePROVHainautWorkflowConditions(MeetingAdviceCommunesWorkflowConditions):
    ''' '''

    implements(IMeetingAdvicePROVHainautWorkflowConditions)
    security = ClassSecurityInfo()

    security.declarePublic('mayProposeToFinancialEditor')

    def mayProposeToFinancialEditor(self):
        ''' '''
        res = super(MeetingAdvicePROVHainautWorkflowConditions, self).mayProposeToFinancialEditor()
        if res and \
           self.context.queryState() == 'proposed_to_financial_controller' and \
           self.context.advice_category == 'comptabilite':
            res = False
        return res

    security.declarePublic('mayProposeToFinancialManager')

    def mayProposeToFinancialManager(self):
        '''A financial manager may send the advice to the financial manager
           in any case (advice positive or negative) except if advice
           is still 'asked_again'.'''
        res = super(MeetingAdvicePROVHainautWorkflowConditions, self).mayProposeToFinancialManager()
        if res and \
           self.context.queryState() == 'proposed_to_financial_controller' and \
           self.context.advice_category != 'comptabilite':
            res = False
        return res


class CustomMeetingConfig(MCCustomMeetingConfig):
    ''' '''

    def _adviceConditionsInterfaceFor(self, advice_obj):
        '''See doc in interfaces.py.'''
        if advice_obj.portal_type == 'meetingadvicefinances':
            return IMeetingAdvicePROVHainautWorkflowConditions.__identifier__
        else:
            return super(CustomMeetingConfig, self)._adviceConditionsInterfaceFor(advice_obj)


class CustomMeetingItem(MCCustomMeetingItem):
    ''' '''

    def __init__(self, item):
        self.context = item

    def mayEvaluateCompleteness(self):
        '''Completeness can be evaluated by the finance precontroller.'''

        item = self.getSelf()
        if item.isDefinedInTool():
            return False

        # finances advice asked?
        finance_org_uid = finance_group_uid()
        if finance_org_uid not in item.adviceIndex:
            return False

        # bypass for Managers
        tool = api.portal.get_tool('portal_plonemeeting')
        if tool.isManager(item, realManagers=True):
            return True

        # relevant state?
        cfg = tool.getMeetingConfig(item)
        if item.queryState() not in finances_give_advice_states(cfg):
            return False

        # current user is pre-controller for asked advice?
        userGroups = tool.get_plone_groups_for_user()
        if '%s_financialprecontrollers' % finance_org_uid not in userGroups:
            return False

        return True

    def _advicePortalTypeForAdviser(self, groupId):
        """ """
        if groupId == finance_group_uid():
            return "meetingadvicefinances"
        else:
            return "meetingadvice"

    def _adviceIsAddableByCurrentUser(self, org_uid):
        """Only when item completeness is 'complete' or 'evaluation_not_required'."""
        if org_uid == finance_group_uid():
            return self._is_complete()
        return super(CustomMeetingItem, self)._adviceIsAddableByCurrentUser(org_uid)

    def _adviceIsAddable(self, org_uid):
        ''' '''
        return self.adapted()._adviceIsAddableByCurrentUser(org_uid)

    def _adviceIsEditableByCurrentUser(self, org_uid):
        """Only when item completeness is 'complete' or 'evaluation_not_required'."""
        if org_uid == finance_group_uid():
            return self._is_complete()
        return super(CustomMeetingItem, self)._adviceIsEditableByCurrentUser(org_uid)

    def _adviceDelayMayBeStarted(self, org_uid):
        """Delay is started when advice no more at controllers states."""
        res = True
        if org_uid == finance_group_uid():
            item = self.getSelf()
            adviceObj = item.getAdviceObj(org_uid)
            if not adviceObj or adviceObj.queryState() in ['advicecreated', 'proposed_to_financial_controller']:
                res = False
        if res:
            res = super(CustomMeetingItem, self)._adviceDelayMayBeStarted(org_uid)
        return res

    def getCustomAdviceMessageFor(self, advice):
        '''If we are on a finance advice that is still not giveable because
           the item is not 'complete', we display a clear message.'''
        item = self.getSelf()
        finance_org_uid = finance_group_uid()
        if advice['id'] == finance_org_uid and \
           advice['delay'] and \
           (not advice['delay_started_on'] or advice['type'] == 'asked_again'):
            finance_org = get_organization(finance_org_uid)
            tool = api.portal.get_tool('portal_plonemeeting')
            cfg = tool.getMeetingConfig(item)
            # item in state giveable but item not complete
            if item.queryState() in finance_org.get_item_advice_states(cfg):
                if not self._is_complete():
                    return {'displayDefaultComplementaryMessage': False,
                            'customAdviceMessage':
                            translate('finance_advice_not_giveable_because_item_not_complete',
                                      domain="PloneMeeting",
                                      context=item.REQUEST,
                                      default="Advice is still not giveable because item is not considered complete.")}
                # delay still not started when advice created/proposed_to_controller
                if not item.adapted()._adviceDelayMayBeStarted(advice['id']):
                    return {'displayDefaultComplementaryMessage': False,
                            'customAdviceMessage': translate(
                                'finance_advice_delay_still_not_started',
                                domain="PloneMeeting",
                                context=item.REQUEST,
                                default="Advice delay is still not started.")}
        return {'displayDefaultComplementaryMessage': True,
                'customAdviceMessage': None}


InitializeClass(CustomMeetingConfig)
InitializeClass(CustomMeetingItem)

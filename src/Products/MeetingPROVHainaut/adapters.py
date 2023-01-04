# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from collective.contact.plonegroup.utils import get_organization
from Globals import InitializeClass
from imio.helpers.cache import get_plone_groups_for_user
from plone import api
from Products.MeetingCommunes.adapters import CustomMeetingConfig as MCCustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem as MCCustomMeetingItem
from Products.MeetingCommunes.adapters import CustomToolPloneMeeting as MCCustomToolPloneMeeting
from Products.MeetingCommunes.adapters import MeetingAdviceCommunesWorkflowConditions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowConditions
from Products.MeetingCommunes.utils import finances_give_advice_states
from Products.MeetingPROVHainaut.interfaces import IMeetingAdvicePROVHainautWorkflowConditions
from Products.MeetingPROVHainaut.utils import finance_group_cec_uid
from Products.MeetingPROVHainaut.utils import finance_group_no_cec_uid
from Products.MeetingPROVHainaut.utils import finance_group_uid
from Products.MeetingPROVHainaut.utils import finance_group_uids
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model import adaptations
from zope.i18n import translate
from zope.interface import implements


# add finances advice related wfAdaptations
wfAdaptations = list(MeetingConfig.wfAdaptations)
wfAdaptations.append('meetingadvicefinances_add_advicecreated_state')
wfAdaptations.append('meetingadvicefinances_controller_propose_to_manager')
MeetingConfig.wfAdaptations = tuple(wfAdaptations)

adaptations.WAITING_ADVICES_USE_CUSTOM_ICON = False
adaptations.WAITING_ADVICES_USE_CUSTOM_BACK_TR_TITLE_FOR = ('validated', )
adaptations.WAITING_ADVICES_USE_CUSTOM_STATE_TITLE = False


class MeetingAdvicePROVHainautWorkflowConditions(MeetingAdviceCommunesWorkflowConditions):
    ''' '''

    implements(IMeetingAdvicePROVHainautWorkflowConditions)
    security = ClassSecurityInfo()


class MeetingItemPROVHainautWorkflowActions(MeetingItemCommunesWorkflowActions):
    """ """

    def _will_ask_completeness_eval_again(self):
        ''' '''
        res = False
        if finance_group_uid() in self.context.adviceIndex or \
           finance_group_cec_uid() in self.context.adviceIndex:
            res = super(MeetingItemPROVHainautWorkflowActions, self)._will_ask_completeness_eval_again()
        return res

    def _will_set_completeness_to_not_required(self):
        ''' '''
        finance_group_no_cec = finance_group_no_cec_uid()
        return finance_group_no_cec in self.context.adviceIndex


class MeetingItemPROVHainautWorkflowConditions(MeetingItemCommunesWorkflowConditions):
    """ """

    def _currentUserIsAdviserAbleToSendItemBackExtraCondition(self, org_uid, destinationState):
        '''Only financial managers may send item back to validated (aka validate the item)
           when advice is signed.'''
        res = True
        if destinationState == 'validated':
            advice_obj = self.context.getAdviceObj(org_uid)
            res = '%s_financialmanagers' % org_uid in get_plone_groups_for_user() and \
                (advice_obj and advice_obj.query_state() in
                 ['financial_advice_signed', 'advice_given'])
        return res

    def _get_waiting_advices_icon_advisers(self):
        '''To be overrided, return adviser ids for which the waiting_advices icon
           color must be computed.'''
        return finance_group_uids()

    def _adviceSendableBackOnlyWhenNoMoreEditable(self, org_uid):
        '''Advice is only sendable back when no more editable, aka end of advice WF.'''
        res = False
        if org_uid == finance_group_no_cec_uid():
            res = True
        return res


class CustomMeetingConfig(MCCustomMeetingConfig):
    ''' '''

    def _adviceConditionsInterfaceFor(self, advice_obj):
        '''See doc in interfaces.py.'''
        if advice_obj.portal_type.startswith('meetingadvicefinances'):
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
        finance_org_cec_uid = finance_group_cec_uid()
        if finance_org_uid not in item.adviceIndex and \
           finance_org_cec_uid not in item.adviceIndex:
            return False

        # bypass for Managers
        tool = api.portal.get_tool('portal_plonemeeting')
        if tool.isManager(realManagers=True):
            return True

        # relevant state?
        cfg = tool.getMeetingConfig(item)
        if item.query_state() not in finances_give_advice_states(cfg):
            return False

        # current user is pre-controller for asked advice?
        userGroups = get_plone_groups_for_user()
        if '%s_financialprecontrollers' % finance_org_uid not in userGroups and \
           '%s_financialprecontrollers' % finance_org_cec_uid not in userGroups:
            return False

        return True

    def _adviceIsAddableByCurrentUser(self, org_uid):
        """Only when item completeness is 'complete' or 'evaluation_not_required'."""
        # is_complete by default for "non finances" advices
        is_complete = True
        if org_uid in finance_group_uids():
            is_complete = self._is_complete()
        return is_complete and super(CustomMeetingItem, self)._adviceIsAddableByCurrentUser(org_uid)

    def _adviceIsAddable(self, org_uid):
        ''' '''
        return self._adviceIsAddableByCurrentUser(org_uid)

    def _adviceIsEditableByCurrentUser(self, org_uid):
        """Only when item completeness is 'complete' or 'evaluation_not_required'."""
        # is_complete by default for "non finances" advices
        is_complete = True
        if org_uid in finance_group_uids():
            is_complete = self._is_complete()
        return is_complete and super(CustomMeetingItem, self)._adviceIsEditableByCurrentUser(org_uid)

    def _adviceDelayMayBeStarted(self, org_uid):
        """Delay is started when advice no more at controllers states."""
        res = True
        if org_uid == finance_group_uid():
            item = self.getSelf()
            adviceObj = item.getAdviceObj(org_uid)
            if not adviceObj or adviceObj.query_state() in [
                    'advicecreated', 'proposed_to_financial_controller']:
                res = False
        if res:
            res = super(CustomMeetingItem, self)._adviceDelayMayBeStarted(org_uid)
        return res

    def getCustomAdviceMessageFor(self, advice):
        '''If we are on a finance advice that is still not giveable because
           the item is not 'complete', we display a clear message.'''
        item = self.getSelf()
        finance_org_uids = (finance_group_uid(), finance_group_cec_uid())
        if advice['id'] in finance_org_uids and \
           not advice['advice_addable']:
            finance_org = get_organization(advice['id'])
            tool = api.portal.get_tool('portal_plonemeeting')
            cfg = tool.getMeetingConfig(item)
            # item in state giveable but item not complete
            if item.query_state() in finance_org.get_item_advice_states(cfg):
                if not self._is_complete():
                    return {'displayDefaultComplementaryMessage': False,
                            'displayAdviceReviewState': True,
                            'customAdviceMessage':
                            translate('finance_advice_not_giveable_because_item_not_complete',
                                      domain="PloneMeeting",
                                      context=item.REQUEST,
                                      default="Advice is still not giveable because item is not considered complete.")}
                # delay still not started when advice created/proposed_to_controller
                if not item.adapted()._adviceDelayMayBeStarted(advice['id']):
                    return {'displayDefaultComplementaryMessage': False,
                            'displayAdviceReviewState': True,
                            'customAdviceMessage': translate(
                                'finance_advice_delay_still_not_started',
                                domain="PloneMeeting",
                                context=item.REQUEST,
                                default="Advice delay is still not started.")}
        return {'displayDefaultComplementaryMessage': True,
                'displayAdviceReviewState': True,
                'customAdviceMessage': None}

    def custom_validate_optionalAdvisers(self, values, storedOptionalAdvisers, removedAdvisers):
        '''Several finances advices may not be asked together.'''
        item = self.getSelf()
        if len(values) > 1:
            # double check to avoid failing tests
            fin_group_uids = finance_group_uids()
            value_org_uids = [value.split('_')[0] for value in values
                              if value is not None]
            if len(set(fin_group_uids).intersection(set(value_org_uids))) > 1:
                return translate('can_not_select_several_financial_advisers',
                                 domain='PloneMeeting',
                                 context=item.REQUEST)


class CustomToolPloneMeeting(MCCustomToolPloneMeeting):
    ''' '''

    def get_extra_adviser_infos(self):
        ''' '''
        infos = {}
        infos[finance_group_uid()] = {'portal_type': 'meetingadvicefinances',
                                      'base_wf': 'meetingadvicefinances_workflow',
                                      'wf_adaptations': ['add_advicecreated_state']}
        infos[finance_group_cec_uid()] = {'portal_type': 'meetingadvicefinancescec',
                                          'base_wf': 'meetingadvicefinancesmanager_workflow',
                                          'wf_adaptations': ['add_advicecreated_state']}
        infos[finance_group_no_cec_uid()] = {'portal_type': 'meetingadvicefinancesnocec',
                                             'base_wf': 'meetingadvicefinanceseditor_workflow',
                                             'wf_adaptations': []}
        return infos


InitializeClass(CustomMeetingConfig)
InitializeClass(CustomMeetingItem)
InitializeClass(CustomToolPloneMeeting)
InitializeClass(MeetingItemPROVHainautWorkflowActions)

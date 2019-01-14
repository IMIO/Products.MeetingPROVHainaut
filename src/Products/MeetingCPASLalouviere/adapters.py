# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
#
# Copyright (c) 2014 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------
from appy.gen import No
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from plone import api
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission

from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.model import adaptations
from Products.MeetingCommunes.adapters import MeetingCollegeWorkflowActions
from Products.MeetingCommunes.adapters import MeetingCollegeWorkflowConditions
from Products.MeetingCommunes.adapters import MeetingItemCollegeWorkflowActions
from Products.MeetingCommunes.adapters import MeetingItemCollegeWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingPBLalouviereWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingPBLalouviereWorkflowActions
from Products.MeetingCPASLalouviere.interfaces import IMeetingItemPBLalouviereWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingItemPBLalouviereWorkflowActions

from zope.interface import implements
from zope.i18n import translate

# Names of available workflow adaptations.
customWfAdaptations = ('return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations
# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {'meetingitembplalouviere_workflow':
    # view permissions
    {'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read budget infos':
    ('Manager', 'MeetingMember', 'Reader', 'MeetingManager', 'MeetingBudgetImpactEditor', 'MeetingBudgetImpactReviewer'),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'Review portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'Add portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write decision annex':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write budget infos':
    ('Manager', 'MeetingMember', 'MeetingBudgetImpactEditor', 'MeetingManager', 'MeetingBudgetImpactReviewer', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ['Manager', 'MeetingManager', ],
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingManager', ),
     }
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowActions(MeetingCollegeWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowConditions(MeetingCollegeWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowActions(MeetingItemCollegeWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingItemPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doRemove')

    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToN1')

    def doProposeToN1(self, stateChange):
        pass

    security.declarePrivate('doWaitAdvices')

    def doWaitAdvices(self, stateChange):
        pass

    security.declarePrivate('doProposeToSecretaire')

    def doProposeToSecretaire(self, stateChange):
        pass

    security.declarePrivate('doProposeToN2')

    def doProposeToN2(self, stateChange):
        pass

    security.declarePrivate('doProposeToPresident')

    def doProposeToPresident(self, stateChange):
        pass

    security.declarePrivate('doValidateByBudgetImpactReviewer')

    def doValidateByBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doProposeToBudgetImpactReviewer')

    def doProposeToBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doAsk_advices_by_itemcreator')

    def doAsk_advices_by_itemcreator(self, stateChange):
        pass


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowConditions(MeetingItemCollegeWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowConditions"""

    implements(IMeetingItemPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.useHardcodedTransitionsForPresentingAnItem = True
        self.transitionsForPresentingAnItem = ('proposeToN1',
                                               'proposeToN2',
                                               'proposeToSecretaire',
                                               'proposeToPresident',
                                               'validate',
                                               'present')

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        # first of all, the use must have the 'Review portal content permission'
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if the current item state is 'itemcreated', only the MeetingManager can validate
            if self.context.queryState() in ('itemcreated',) and \
                    not self.context.portal_plonemeeting.isManager(self.context):
                res = False
        return res

    security.declarePublic('mayWaitAdvices')

    def mayWaitAdvices(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToN1')

    def mayProposeToN1(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToN2')

    def mayProposeToN2(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToSecretaire')

    def mayProposeToSecretaire(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToPresident')

    def mayProposeToPresident(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if the current item state is 'itemcreated', only the MeetingManager can validate
            member = self.context.portal_membership.getAuthenticatedMember()
            if self.context.queryState() in ('proposed_to_n1',) and not \
               (member.has_role('MeetingReviewer') or member.has_role('Manager')):
                res = False
        return res

    security.declarePublic('mayRemove')

    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  For now, this is the same behaviour as 'mayDecide'
        """
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res

    security.declarePublic('mayValidateByBudgetImpactReviewer')

    def mayValidateByBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToBudgetImpactReviewer')

    def mayProposeToBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res


# ------------------------------------------------------------------------------
InitializeClass(MeetingPBLalouviereWorkflowActions)
InitializeClass(MeetingPBLalouviereWorkflowConditions)
InitializeClass(MeetingItemPBLalouviereWorkflowActions)
InitializeClass(MeetingItemPBLalouviereWorkflowConditions)
# ------------------------------------------------------------------------------


class MLItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MLItemPrettyLinkAdapter, self)._leadingIcons()

        item = self.context

        if item.isDefinedInTool():
            return icons

        itemState = item.queryState()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)

        # add some icons specific for dashboard if we are actually on the dashboard...
        if itemState in cfg.itemDecidedStates and \
                item.REQUEST.form.get('topicId', '') == 'searchitemsfollowupdashboard':
            itemFollowUp = item.getFollowUp()
            if itemFollowUp == 'follow_up_yes':
                icons.append(('follow_up_yes.png', 'icon_help_follow_up_needed'))
            elif itemFollowUp == 'follow_up_provided':
                icons.append(('follow_up_provided.png', 'icon_help_follow_up_provided'))

        # Add our icons for wf states
        if itemState == 'proposed_to_director':
            icons.append(('proposeToDirector.png',
                          translate('icon_help_proposed_to_director',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_divisionhead':
            icons.append(('proposeToDivisionHead.png',
                          translate('icon_help_proposed_to_divisionhead',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_officemanager':
            icons.append(('proposeToOfficeManager.png',
                          translate('icon_help_proposed_to_officemanager',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'item_in_council':
            icons.append(('item_in_council.png',
                          translate('icon_help_item_in_council',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_servicehead':
            icons.append(('proposeToServiceHead.png',
                          translate('icon_help_proposed_to_servicehead',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'item_in_committee':
            icons.append(('item_in_committee.png',
                          translate('icon_help_item_in_committee',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_budgetimpact_reviewer':
            icons.append(('proposed_to_budgetimpact_reviewer.png',
                          translate('icon_help_proposed_to_budgetimpact_reviewer',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'itemcreated_waiting_advices':
            icons.append(('itemcreated_waiting_advices.png',
                          translate('icon_help_itemcreated_waiting_advices  ',
                                    domain="PloneMeeting",
                                    context=self.request)))
        return icons

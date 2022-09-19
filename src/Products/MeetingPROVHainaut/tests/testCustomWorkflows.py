# -*- coding: utf-8 -*-

from imio.helpers.cache import get_cachekey_volatile
from Products.MeetingPROVHainaut.testing import MPH_FIN_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.MeetingPROVHainaut.utils import finance_group_cec_uid
from Products.MeetingPROVHainaut.utils import finance_group_no_cec_uid
from Products.MeetingPROVHainaut.utils import finance_group_uid


class testCustomWorkflows(MeetingPROVHainautTestCase):
    """Tests the default workflows implemented in MeetingPROVHainaut."""

    layer = MPH_FIN_TESTING_PROFILE_FUNCTIONAL

    def test_FinancesAdvicesWorkflow(self):
        """
           Test finances advices workflow.
        """
        def _check_date(item, modified_date, volatile_date):
            '''Check that item modified date was updated.'''
            new_modified_date = item.modified()
            self.assertNotEqual(modified_date, new_modified_date)
            new_volatile_date = get_cachekey_volatile('Products.PloneMeeting.MeetingItem.modified')
            self.assertNotEqual(volatile_date, new_volatile_date)
            return new_modified_date, new_volatile_date

        cfg = self.meetingConfig
        self.changeUser('dgen')
        gic1_uid = cfg.getOrderedGroupsInCharge()[0]
        item = self.create('MeetingItem', groupsInCharge=(gic1_uid, ))
        item_uid = item.UID()
        self.assertEqual(self.transitions(item), ['proposeToValidationLevel1'])
        # ask finances advice
        fin_group_uid = finance_group_uid()
        item.setOptionalAdvisers((fin_group_uid + '__rowid__unique_id_002', ))
        item._update_after_edit()
        # advice still not askable, askable as level2 or level3
        self.assertEqual(self.transitions(item),
                         ['proposeToValidationLevel1'])
        self.do(item, 'proposeToValidationLevel1')
        self.assertEqual(self.transitions(item),
                         ['backToItemCreated', 'proposeToValidationLevel2'])
        self.do(item, 'proposeToValidationLevel2')
        self.assertEqual(self.transitions(item),
                         ['backToProposedToValidationLevel1',
                          'proposeToValidationLevel3',
                          'wait_advices_from_proposedToValidationLevel2'])
        self.do(item, 'wait_advices_from_proposedToValidationLevel2')
        # a MeetingManager is able to send back but not a normal user
        self.assertEqual(
            self.transitions(item),
            ['backTo_proposedToValidationLevel2_from_waiting_advices',
             'backTo_proposedToValidationLevel3_from_waiting_advices',
             'backTo_validated_from_waiting_advices'])
        # but another user can not
        self._addPrincipalToGroup('bourgmestre', self.dirgen_creators)
        self._addPrincipalToGroup('bourgmestre', self.dirgen_level1reviewers)
        self._addPrincipalToGroup('bourgmestre', self.dirgen_level2reviewers)
        self._addPrincipalToGroup('bourgmestre', self.dirgen_level3reviewers)
        self.changeUser('bourgmestre')
        self.assertTrue(self.hasPermission("View", item))
        self.assertEqual(self.transitions(item), [])

        # give advice
        self.changeUser('dfin')
        self.assertEqual(self.transitions(item),
                         ['backTo_proposedToValidationLevel2_from_waiting_advices',
                          'backTo_proposedToValidationLevel3_from_waiting_advices'])
        # advice may be taken over
        self.assertTrue(item.adapted().mayTakeOver())
        # advice giveable when item complete
        self.assertFalse(item.adviceIndex[fin_group_uid]['advice_addable'])
        self.assertTrue(item.adapted().mayEvaluateCompleteness())
        # we will check that item modified date is invalidated when advice changed
        # this is responsible for updating collections counter in faceted portlet
        volatile_date = get_cachekey_volatile('Products.PloneMeeting.MeetingItem.modified')
        item_modified = item.modified()
        item.setCompleteness('completeness_complete')
        item._update_after_edit()
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        advice_portal_type = item._advicePortalTypeForAdviser(fin_group_uid)
        advice = self.addAdvice(item,
                                advice_group=fin_group_uid,
                                advice_type='positive_finance',
                                advice_portal_type=advice_portal_type)
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        self.assertTrue(advice.advice_hide_during_redaction)
        self.assertEqual(self.transitions(advice),
                         ['proposeToFinancialController'])
        # once advice given but hidden during redaction, item may no more be sent back
        self.assertEqual(self.transitions(item), [])
        # financial controller
        self.do(advice, 'proposeToFinancialController')
        self.assertEqual(self.transitions(item), [])
        self.assertEqual(self.transitions(advice),
                         ['backToAdviceCreated',
                          'proposeToFinancialEditor'])
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_proposed_to_financial_controller".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        # financial editor
        self.do(advice, 'proposeToFinancialEditor')
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'proposeToFinancialReviewer'])
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_proposed_to_financial_editor".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        # financial reviewer
        self.do(advice, 'proposeToFinancialReviewer')
        self.assertEqual(self.transitions(item), [])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'backToProposedToFinancialEditor',
                          'proposeToFinancialManager'])
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_proposed_to_financial_reviewer".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        # financial manager
        self.do(advice, 'proposeToFinancialManager')
        self.assertEqual(self.transitions(item), [])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'backToProposedToFinancialReviewer',
                          'signFinancialAdvice'])
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_proposed_to_financial_manager".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        # sign advice
        self.do(advice, 'signFinancialAdvice')
        self.assertEqual(self.transitions(item),
                         ['backTo_proposedToValidationLevel2_from_waiting_advices',
                          'backTo_proposedToValidationLevel3_from_waiting_advices',
                          'backTo_validated_from_waiting_advices'])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialManager'])
        self.assertFalse(advice.advice_hide_during_redaction)
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_financial_advice_signed".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)
        # validate item
        self.do(item, 'backTo_validated_from_waiting_advices')
        self.assertEqual(item.query_state(), 'validated')
        # indexAdvisers is correctly reindexed
        advice_index_value = "delay__{0}_advice_given".format(fin_group_uid)
        self.assertTrue(self.catalog(UID=item_uid, indexAdvisers=[advice_index_value]))
        # item modified date was updated
        item_modified, volatile_date = _check_date(item, item_modified, volatile_date)

    def test_ItemNotValidableWhenFinancesAdviceWFIncomplete(self):
        """
           Financial advice WF must have reached the "signed" step for the item to be
           validable, this avoid having a validated item when advice was sent back to
           proposing group before advice is signed.
           We need the advice to have been signed.
        """
        cfg = self.meetingConfig
        self._deactivate_wfas('waiting_advices_given_and_signed_advices_required_to_validate')
        self.changeUser('dgen')
        gic1_uid = cfg.getOrderedGroupsInCharge()[0]
        fin_no_cec_group_uid = finance_group_no_cec_uid()
        item = self.create(
            'MeetingItem',
            groupsInCharge=(gic1_uid, ),
            optionalAdvisers=(fin_no_cec_group_uid + '__rowid__unique_id_002', ))
        # ask finances advice
        # advice still not askable, askable as level2 or level3
        self.do(item, 'proposeToValidationLevel1')
        self.do(item, 'proposeToValidationLevel2')
        self.do(item, 'wait_advices_from_proposedToValidationLevel2')
        # give advice
        self.changeUser('dfin')
        advice_portal_type = item._advicePortalTypeForAdviser(fin_no_cec_group_uid)
        advice = self.addAdvice(item,
                                advice_group=fin_no_cec_group_uid,
                                advice_type='positive_finance',
                                advice_portal_type=advice_portal_type)
        # financial controller
        self.do(advice, 'proposeToFinancialReviewer')
        # advice must no more be hidden during redaction so item may be sent back
        changeView = advice.restrictedTraverse('@@change-advice-hidden-during-redaction')
        changeView()
        self.do(item, 'backTo_proposedToValidationLevel3_from_waiting_advices')
        # when not using the 'waiting_advices_given_advices_required_to_validate'
        # WFA, item could be validated
        self.assertFalse('waiting_advices_given_and_signed_advices_required_to_validate'
                         in cfg.getWorkflowAdaptations())
        self.changeUser('dgen')
        self.assertTrue('validate' in self.transitions(item))
        self._activate_wfas(
            'waiting_advices_given_and_signed_advices_required_to_validate',
            keep_existing=True)
        self.assertFalse('validate' in self.transitions(item))
        # if finance advice reached the "signed" state, then item may be validated
        self.do(item, 'wait_advices_from_proposedToValidationLevel3')
        self.changeUser('dfin')
        self.do(advice, 'proposeToFinancialReviewer')
        self.do(advice, 'proposeToFinancialManager')
        self.do(advice, 'signFinancialAdvice')
        self.do(item, 'backTo_proposedToValidationLevel3_from_waiting_advices')
        # as advice reached "signed", item may be validated
        self.changeUser('dgen')
        self.assertTrue('validate' in self.transitions(item))
        self.do(item, 'validate')
        self.assertEqual(item.query_state(), 'validated')

    def test_CompletenessEvaluationAskedAgain(self):
        """When item is sent for second+ time to the finances,
           completeness is automatically set to asked again except
           for finance_group_no_cec_uid."""
        cfg = self.meetingConfig
        gic1_uid = cfg.getOrderedGroupsInCharge()[0]
        self.changeUser('dgen')
        item_df1 = self.create(
            'MeetingItem',
            optionalAdvisers=((finance_group_uid() + '__rowid__unique_id_002', )),
            groupsInCharge=(gic1_uid, ))
        item_df2 = self.create(
            'MeetingItem',
            optionalAdvisers=((finance_group_cec_uid(), )),
            groupsInCharge=(gic1_uid, ))
        item_df3 = self.create(
            'MeetingItem',
            optionalAdvisers=((finance_group_no_cec_uid(), )),
            groupsInCharge=(gic1_uid, ))
        for tr in ['proposeToValidationLevel1',
                   'proposeToValidationLevel2',
                   'wait_advices_from_proposedToValidationLevel2']:
            self.do(item_df1, tr)
            self.do(item_df2, tr)
            self.do(item_df3, tr)
        self.assertEqual(item_df1.getCompleteness(), 'completeness_not_yet_evaluated')
        self.assertEqual(item_df2.getCompleteness(), 'completeness_not_yet_evaluated')
        self.assertEqual(item_df3.getCompleteness(), 'completeness_evaluation_not_required')
        # incomplete, return
        item_df1.setCompleteness('completeness_incomplete')
        item_df2.setCompleteness('completeness_incomplete')
        self.changeUser('dfin')
        self.do(item_df1, 'backTo_proposedToValidationLevel2_from_waiting_advices')
        self.do(item_df2, 'backTo_proposedToValidationLevel2_from_waiting_advices')
        self.do(item_df3, 'backTo_proposedToValidationLevel2_from_waiting_advices')
        # ask again
        self.changeUser('dgen')
        self.assertEqual(item_df1.getCompleteness(), 'completeness_incomplete')
        self.assertEqual(item_df2.getCompleteness(), 'completeness_incomplete')
        # manipulate completeness, like if we changed from DF3 to DF2
        item_df2.setCompleteness('completeness_evaluation_not_required')
        self.assertEqual(item_df3.getCompleteness(), 'completeness_evaluation_not_required')
        self.do(item_df1, 'wait_advices_from_proposedToValidationLevel2')
        self.do(item_df2, 'wait_advices_from_proposedToValidationLevel2')
        self.do(item_df3, 'wait_advices_from_proposedToValidationLevel2')
        self.assertEqual(item_df1.getCompleteness(), 'completeness_evaluation_asked_again')
        self.assertEqual(item_df2.getCompleteness(), 'completeness_evaluation_asked_again')
        self.assertEqual(item_df3.getCompleteness(), 'completeness_evaluation_not_required')

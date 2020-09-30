# -*- coding: utf-8 -*-

from Products.MeetingPROVHainaut.testing import MPH_FIN_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.MeetingPROVHainaut.utils import finance_group_uid


class testCustomWorkflows(MeetingPROVHainautTestCase):
    """Tests the default workflows implemented in MeetingPROVHainaut."""

    layer = MPH_FIN_TESTING_PROFILE_FUNCTIONAL

    def test_FinancesAdvicesWorkflow(self):
        """
           Test finances advices workflow.
        """
        cfg = self.meetingConfig

        self.changeUser('dgen')
        gic1_uid = cfg.getOrderedGroupsInCharge()[0]
        item = self.create('MeetingItem', groupsInCharge=(gic1_uid, ))
        self.assertEqual(self.transitions(item), ['proposeToValidationLevel1'])
        # ask finances advice
        fin_group_uid = finance_group_uid()
        item.setOptionalAdvisers((fin_group_uid + '__rowid__unique_id_002', ))
        item.at_post_edit_script()
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
        self.assertEqual(self.transitions(item), [])

        # give advice
        self.changeUser('dfin')
        self.assertEqual(self.transitions(item),
                         ['backTo_proposedToValidationLevel2_from_waiting_advices',
                          'backTo_proposedToValidationLevel3_from_waiting_advices'])
        # advice giveable when item complete
        self.assertFalse(item.adviceIndex[fin_group_uid]['advice_addable'])
        self.assertTrue(item.adapted().mayEvaluateCompleteness())
        item.setCompleteness('completeness_complete')
        item.at_post_edit_script()
        advice_portal_type = item._advicePortalTypeForAdviser(fin_group_uid)
        advice = self.addAdvice(item,
                                advice_group=fin_group_uid,
                                advice_type='positive_finance',
                                advice_portal_type=advice_portal_type)
        self.assertTrue(advice.advice_hide_during_redaction)
        self.assertEqual(self.transitions(advice),
                         ['proposeToFinancialController'])
        # once advice given but hidden during redaction, item may no more be sent back
        self.assertEqual(self.transitions(item), [])
        # financial controller
        self.do(advice, 'proposeToFinancialController')
        self.assertEqual(self.transitions(advice),
                         ['backToAdviceCreated',
                          'proposeToFinancialEditor'])
        self.assertEqual(self.transitions(item), [])
        # financial editor
        self.do(advice, 'proposeToFinancialEditor')
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'proposeToFinancialReviewer'])
        # financial reviewer
        self.do(advice, 'proposeToFinancialReviewer')
        self.assertEqual(self.transitions(item), [])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'backToProposedToFinancialEditor',
                          'proposeToFinancialManager'])
        # financial manager
        self.do(advice, 'proposeToFinancialManager')
        self.assertEqual(self.transitions(item), [])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialController',
                          'backToProposedToFinancialReviewer',
                          'signFinancialAdvice'])
        # sign advice
        self.do(advice, 'signFinancialAdvice')
        self.assertEqual(self.transitions(item),
                         ['backTo_proposedToValidationLevel2_from_waiting_advices',
                          'backTo_proposedToValidationLevel3_from_waiting_advices',
                          'backTo_validated_from_waiting_advices'])
        self.assertEqual(self.transitions(advice),
                         ['backToProposedToFinancialManager'])
        self.assertFalse(advice.advice_hide_during_redaction)
        # validate item
        self.do(item, 'backTo_validated_from_waiting_advices')
        self.assertEqual(item.queryState(), 'validated')

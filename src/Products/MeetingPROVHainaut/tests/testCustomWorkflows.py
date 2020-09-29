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
        import ipdb; ipdb.set_trace()
        self.assertEqual(self.transitions(item),
                         ['backTo_proposedToValidationLevel2_from_waiting_advices',
                          'backTo_proposedToValidationLevel3_from_waiting_advices'])
        # advice giveable when item complete
        self.assertFalse(item.adviceIndex[fin_group_uid]['advice_addable'])

# -*- coding: utf-8 -*-

from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.MeetingCommunes.tests.testWFAdaptations import testWFAdaptations as mctwfa


class testWFAdaptations(MeetingPROVHainautTestCase, mctwfa):
    '''Tests various aspects of votes management.'''

    def test_pm_WFA_availableWFAdaptations(self):
        '''Test what are the available wfAdaptations.'''
        self.assertEqual(
            sorted(self.meetingConfig.listWorkflowAdaptations().keys()),
            ['accepted_but_modified',
             'accepted_out_of_meeting',
             'accepted_out_of_meeting_and_duplicated',
             'accepted_out_of_meeting_emergency',
             'accepted_out_of_meeting_emergency_and_duplicated',
             'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
             'delayed',
             'hide_decisions_when_under_writing',
             'mark_not_applicable',
             'meetingadvicefinances_add_advicecreated_state',
             'meetingadvicefinances_controller_propose_to_manager',
             'meetingmanager_correct_closed_meeting',
             'no_publication',
             'only_creator_may_delete',
             'postpone_next_meeting',
             'pre_accepted',
             'presented_item_back_to_itemcreated',
             'presented_item_back_to_proposed',
             'refused',
             'removed',
             'removed_and_duplicated',
             'return_to_proposing_group',
             'return_to_proposing_group_with_all_validations',
             'return_to_proposing_group_with_last_validation',
             'reviewers_take_back_validated_item',
             'waiting_advices',
             'waiting_advices_adviser_may_validate',
             'waiting_advices_adviser_send_back',
             'waiting_advices_from_before_last_val_level',
             'waiting_advices_from_every_val_levels',
             'waiting_advices_from_last_val_level',
             'waiting_advices_given_advices_required_to_validate',
             'waiting_advices_proposing_group_send_back'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_pm_'))
    return suite

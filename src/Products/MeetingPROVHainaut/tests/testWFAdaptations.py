# -*- coding: utf-8 -*-

from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.MeetingCommunes.tests.testWFAdaptations import testWFAdaptations as mctwfa


class testWFAdaptations(MeetingPROVHainautTestCase, mctwfa):
    '''Tests various aspects of votes management.'''

    def test_pm_WFA_availableWFAdaptations(self):
        '''Test what are the available wfAdaptations.'''
        self.assertEquals(sorted(self.meetingConfig.listWorkflowAdaptations().keys()),
                          ['accepted_out_of_meeting',
                           'accepted_out_of_meeting_and_duplicated',
                           'accepted_out_of_meeting_emergency',
                           'accepted_out_of_meeting_emergency_and_duplicated',
                           'creator_edits_unless_closed',
                           'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
                           'everyone_reads_all',
                           'hide_decisions_when_under_writing',
                           'items_come_validated',
                           'mark_not_applicable',
                           'meetingadvicefinances_add_advicecreated_state',
                           'meetingadvicefinances_controller_propose_to_manager',
                           'no_global_observation',
                           'no_proposal',
                           'no_publication',
                           'only_creator_may_delete',
                           'postpone_next_meeting',
                           'pre_validation',
                           'pre_validation_keep_reviewer_permissions',
                           'presented_item_back_to_itemcreated',
                           'presented_item_back_to_prevalidated',
                           'presented_item_back_to_proposed',
                           'refused',
                           'removed',
                           'removed_and_duplicated',
                           'return_to_proposing_group',
                           'return_to_proposing_group_with_all_validations',
                           'return_to_proposing_group_with_last_validation',
                           'reviewers_take_back_validated_item',
                           'waiting_advices'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_pm_'))
    return suite

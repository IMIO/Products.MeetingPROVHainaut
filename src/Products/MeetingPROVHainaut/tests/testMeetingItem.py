# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase


class testMeetingItem(MeetingPROVHainautTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_pm_Completeness(self):
        """Already tested in testWorkflows."""
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_pm_'))
    return suite

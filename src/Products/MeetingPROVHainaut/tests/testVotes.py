# -*- coding: utf-8 -*-
#
# File: testVotes.py
#

from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.PloneMeeting.tests.testVotes import testVotes as pmtv


class testVotes(MeetingPROVHainautTestCase, pmtv):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testVotes, prefix='test_pm_'))
    return suite

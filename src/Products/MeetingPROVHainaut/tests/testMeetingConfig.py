# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.testMeetingConfig import testMeetingConfig as mctmc
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase


class testMeetingConfig(MeetingPROVHainautTestCase, mctmc):
    '''Call testMeetingConfig tests.'''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingConfig, prefix='test_pm_'))
    return suite

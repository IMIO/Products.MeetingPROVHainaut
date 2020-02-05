# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#

from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase
from Products.MeetingCommunes.tests.testWorkflows import testWorkflows as mctw


class testWorkflows(MeetingPROVHainautTestCase, mctw):
    """ """


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite

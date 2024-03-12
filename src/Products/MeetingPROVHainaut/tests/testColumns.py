# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testColumns import testColumns as mctc
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase


class testColumns(MeetingPROVHainautTestCase, mctc):
    ''' '''


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testColumns, prefix='test_pm_'))
    return suite

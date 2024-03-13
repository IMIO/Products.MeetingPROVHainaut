# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from collective.contact.plonegroup.utils import get_plone_group_id
from Products.MeetingCommunes.tests.testToolPloneMeeting import testToolPloneMeeting as mctt
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase


class testToolPloneMeeting(MeetingPROVHainautTestCase, mctt):
    '''Tests the ToolPloneMeeting class methods.'''

    def test_pm_FinancesAdvisersConfig(self):
        """ """
        self.changeUser('siteadmin')
        self._addPrincipalToGroup(
            'pmReviewer2',
            get_plone_group_id(self.vendors_uid, 'financialmanagers'))
        super(testToolPloneMeeting, self).test_pm_FinancesAdvisersConfig()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_pm_'))
    return suite

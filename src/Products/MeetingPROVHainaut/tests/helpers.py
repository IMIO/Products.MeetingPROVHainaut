# -*- coding: utf-8 -*-

from copy import deepcopy
from collective.contact.plonegroup.utils import select_org_for_function
from plone.memoize.forever import _memos
from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers
from Products.MeetingPROVHainaut.config import PROJECTNAME
from Products.MeetingPROVHainaut.profiles.zprovhainaut import import_data as provhainaut_import_data
from Products.MeetingPROVHainaut.utils import finance_group_uid
from Products.PloneMeeting.exportimport.content import ToolInitializer


class MeetingPROVHainautTestingHelpers(MeetingCommunesTestingHelpers):
    '''Override some values of MeetingCommunesTestingHelpers.'''

    def _configureFinancesAdvice(self, cfg):
        """ """
        # add finances group
        self._createFinancesGroup()
        # put users in finances group
        self._setupFinancesGroup()
        # configure customAdvisers for 'meeting-config-college'
        # turn FINANCE_GROUP_ID into relevant org UID
        customAdvisers = deepcopy(provhainaut_import_data.collegeMeeting.customAdvisers)
        for customAdviser in customAdvisers:
            customAdviser['org'] = finance_group_uid()
        cfg.setCustomAdvisers(customAdvisers)
        # configure usedAdviceTypes
        cfg.setUsedAdviceTypes(('asked_again',
                                'positive',
                                'positive_with_remarks',
                                'negative',
                                'nil',
                                'positive_finance',
                                'positive_with_remarks_finance',
                                'negative_finance',
                                'not_given_finance'))

    def _createFinancesGroup(self):
        """
           Create the finances group.
        """
        context = self.portal.portal_setup._getImportContext('Products.MeetingPROVHainaut:testing')
        initializer = ToolInitializer(context, PROJECTNAME)

        dirfin_grp = deepcopy(provhainaut_import_data.dirfincec)
        orgs, active_orgs, savedOrgsData = initializer.addOrgs([dirfin_grp])
        initializer.data = initializer.getProfileData()
        for org in orgs:
            org_uid = org.UID()
            self._select_organization(org_uid)
            select_org_for_function(org_uid, 'financialprecontrollers')
            select_org_for_function(org_uid, 'financialcontrollers')
            select_org_for_function(org_uid, 'financialeditors')
            select_org_for_function(org_uid, 'financialmanagers')
            select_org_for_function(org_uid, 'financialreviewers')
        # clean forever cache on utils finance_group_uid
        _memos.clear()

    def _setupFinancesGroup(self):
        '''Configure finances group.'''
        self._addPrincipalToGroup('pmAdviser2', '{0}_advisers'.format(finance_group_uid()))
        # respective _financesXXX groups
        self._addPrincipalToGroup('pmAdviser2', '{0}_financialprecontrollers'.format(finance_group_uid()))
        self._addPrincipalToGroup('pmAdviser2', '{0}_financialcontrollers'.format(finance_group_uid()))
        self._addPrincipalToGroup('pmAdviser2', '{0}_financialeditors'.format(finance_group_uid()))
        self._addPrincipalToGroup('pmAdviser2', '{0}_financialreviewers'.format(finance_group_uid()))
        self._addPrincipalToGroup('pmAdviser2', '{0}_financialmanagers'.format(finance_group_uid()))

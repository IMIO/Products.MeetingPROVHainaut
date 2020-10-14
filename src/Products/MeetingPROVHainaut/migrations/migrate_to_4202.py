# -*- coding: utf-8 -*-

from Products.PloneMeeting.migrations import Migrator

import logging


logger = logging.getLogger('MeetingPROVHainaut')


class Migrate_To_4202(Migrator):

    def _updateFinanceAdvicesAdviceType(self):
        """Use _finance like advice_type values for every finances advices.
           XXX this necessitate that upgradeLocalRoles are launched after!!!"""
        logger.info('Updating advice_type for every finances advices...')
        finances_portal_types = [
            portal_type for portal_type in self.tool.getAdvicePortalTypes(as_ids=True)
            if 'finances' in portal_type]
        brains = self.catalog(portal_type=finances_portal_types)
        for brain in brains:
            advice = brain.getObject()
            advice_type = advice.advice_type
            if not advice_type.endswith('_finance'):
                advice.advice_type = advice_type + '_finance'
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingPROVHainaut 4202...')
        self._updateFinanceAdvicesAdviceType()


def migrate(context):
    '''This migration will:
       1) Update advice_type of every finances advice to use _finance suffixed advice_type.
    '''
    migrator = Migrate_To_4202(context)
    migrator.run()
    migrator.finish()

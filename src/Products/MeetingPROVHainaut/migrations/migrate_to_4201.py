# -*- coding: utf-8 -*-

from plone import api
from Products.PloneMeeting.migrations import Migrator

import logging


logger = logging.getLogger('MeetingPROVHainaut')


class Migrate_To_4201(Migrator):

    def _migrateItemsMotivationToDecision(self):
        """Field MeetingItem.motivation is no more used,
           we use MeetingItem.description."""
        logger.info('Migrating MeetingItem.motivation to MeetingItem.description...')
        # make sure description field is enabled and motivation field is disabled
        logger.info('Substep >>> Fixing MeetingConfigs...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            usedItemAttrs = list(cfg.getUsedItemAttributes())
            if 'motivation' in usedItemAttrs:
                usedItemAttrs.remove('motivation')
                if 'description' not in usedItemAttrs:
                    usedItemAttrs.append('description')
                cfg.setUsedItemAttributes(usedItemAttrs)
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(meta_type=['MeetingItem'])
        # this will update every items, recurring/itemtemplate/real items
        logger.info('Substep >>> Migrating items...')
        for brain in brains:
            item = brain.getObject()
            if not item.fieldIsEmpty('motivation'):
                item.setDescription(item.getRawMotivation())
                item.setMotivation('<p></p>')
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingPROVHainaut 4201...')
        self._migrateItemsMotivationToDecision()


def migrate(context):
    '''This migration will:
       1) Migrate MeetingConfig/MeetingItem as MeetingItem.motivation is replaced by MeetingItem.description.
    '''
    migrator = Migrate_To_4201(context)
    migrator.run()
    migrator.finish()

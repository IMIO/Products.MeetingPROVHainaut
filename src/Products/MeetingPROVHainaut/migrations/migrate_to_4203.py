# -*- coding: utf-8 -*-

from imio.helpers.content import safe_delattr
from Products.PloneMeeting.migrations import Migrator
from Products.ZCatalog.ProgressHandler import ZLogHandler

import logging


logger = logging.getLogger('MeetingPROVHainaut')


class Migrate_To_4203(Migrator):

    def _removeMeetingItemGroupedItemsNumAttribute(self):
        """This field was supposed to be used but will not...
           Remove the MeetingItem.groupedItemsNum attribute on every existing items."""
        logger.info('Removing attribute "groupedItemsNum" from every items...')
        brains = self.catalog(meta_type="MeetingItem")
        pghandler = ZLogHandler(steps=1000)
        pghandler.init('Working', len(brains))
        i = 0
        for brain in brains:
            i += 1
            pghandler.report(i)
            item = brain.getObject()
            safe_delattr(item, "groupedItemsNum")
        pghandler.finish()
        logger.info('Done.')

    def _fixPODTemplatesInstructions(self):
        """Fix specific POD templates instructions."""
        # delete the filtered_groups_in_charge script in portal_skins/custom
        if "filtered_groups_in_charge" in self.portal.portal_skins.custom.objectIds():
            self.portal.portal_skins.custom.manage_delObjects(ids=["filtered_groups_in_charge"])
        # for every POD templates
        replacements = {
            'self.filtered_groups_in_charge':
            'self.get_representatives_in_charge',
        }
        self.updatePODTemplatesCode(replacements=replacements)

    def run(self):
        logger.info('Migrating to MeetingPROVHainaut 4203...')
        self._removeMeetingItemGroupedItemsNumAttribute()
        self._fixPODTemplatesInstructions()


def migrate(context):
    '''This migration will:
       1) Remove unused MeetingItem.groupedItemsNum attribute;
       2) Fix POD templates, custom script "filtered_groups_in_charge" was
          moved to "CustomMeetingItem.get_representatives_in_charge".
    '''
    migrator = Migrate_To_4203(context)
    migrator.run()
    migrator.finish()

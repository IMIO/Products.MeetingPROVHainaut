# -*- coding: utf-8 -*-

from copy import deepcopy
from imio.helpers.setup import load_type_from_package
from Products.PloneMeeting.migrations import Migrator
from Products.MeetingPROVHainaut.profiles.zprovhainaut import import_data as mph_import_data
from Products.MeetingPROVHainaut.utils import finance_group_uid
from Products.MeetingPROVHainaut.utils import finance_group_cec_uid
from Products.MeetingPROVHainaut.utils import finance_group_no_cec_uid
import logging


logger = logging.getLogger('MeetingPROVHainaut')


class Migrate_To_4204(Migrator):

    def _upgradeToAdvisersConfig(self):
        """Custom advisers are now configured in UI, we need to:
           - adapt MeetingConfig.usedAdviceTypes;
           - configure ToolPloneMeeting.customAdivsers;
           - update every finances advice wokflow_history as used WF id changed."""
        logger.info('Upgrading to customAdvisers UI...')
        # update every MeetingConfig.usedAdviceTypes to remove _finance values
        for cfg in self.tool.objectValues('MeetingConfig'):
            usedAdviceTypes = cfg.getUsedAdviceTypes()
            cfg.setUsedAdviceTypes([at for at in usedAdviceTypes
                                    if not at.endswith('_finance')])
        # configure ToolPloneMeeting.advisersConfig
        if not self.tool.getAdvisersConfig():
            data = deepcopy(mph_import_data.data.advisersConfig)
            data[0]['org_uids'] = [finance_group_uid()]
            data[1]['org_uids'] = [finance_group_cec_uid()]
            data[2]['org_uids'] = [finance_group_no_cec_uid()]
            self.tool.setAdvisersConfig(data)
            self.tool.configureAdvices()
        # reload meetingadvicefinances/meetingadvicefinancescec as model_source
        # was removed and we use IAdviceAccountingCommitmentBehavior behavior
        load_type_from_package('meetingadvicefinances', 'Products.MeetingPROVHainaut:default')
        load_type_from_package('meetingadvicefinancescec', 'Products.MeetingPROVHainaut:default')
        logger.info('Done.')

    def run(self,
            profile_name=u'profile-Products.MeetingLiege:default',
            extra_omitted=[]):

        # this will upgrade Products.PloneMeeting and dependencies
        self.upgradeAll(omit=[profile_name.replace('profile-', '')])

        self._upgradeToAdvisersConfig()


def migrate(context):
    '''This migration will:

       1) Upgrade to ToolPloneMeeting.advisersConfig.
    '''
    migrator = Migrate_To_4204(context)
    migrator.run()
    migrator.finish()

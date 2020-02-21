# -*- coding: utf-8 -*-

from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_REAPPLY
from Products.MeetingCommunes.migrations.migrate_to_4200 import Migrate_To_4200 as MCMigrate_To_4200
from Products.MeetingPROVHainaut.setuphandlers import _configureDexterityLocalRolesField

import logging


logger = logging.getLogger('MeetingPROVHainaut')


class Migrate_To_4200(MCMigrate_To_4200):

    def run(self):
        super(Migrate_To_4200, self).run(extra_omitted=['Products.MeetingPROVHainaut:default'])
        self.reinstall(profiles=[u'profile-Products.MeetingPROVHainaut:default'],
                       ignore_dependencies=False,
                       dependency_strategy=DEPENDENCY_STRATEGY_REAPPLY)
        _configureDexterityLocalRolesField()


def migrate(context):
    '''This migration will:
       1) Execute Products.MeetingPROVHainaut migration.
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()

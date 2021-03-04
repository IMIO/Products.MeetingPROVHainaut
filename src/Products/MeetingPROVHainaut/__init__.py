# -*- coding: utf-8 -*-

from Products.CMFCore import DirectoryView
from Products.MeetingPROVHainaut.config import product_globals

import adapters
import logging
import model.pm_updates  # noqa


logger = logging.getLogger('MeetingPROVHainaut')
logger.debug('Installing Product')


DirectoryView.registerDirectory('skins', product_globals)


def initialize(context):
    """initialize product (called by zope)"""

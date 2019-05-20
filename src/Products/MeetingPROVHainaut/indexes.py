# -*- coding: utf-8 -*-
#
# File: indexes.py
#
# Copyright (c) 2019 by Imio.be
#
# GNU General Public License (GPL)
#

from plone.indexer import indexer
from Products.PloneMeeting.interfaces import IMeetingItem

@indexer(IMeetingItem)
def groupedItemsNum(obj):
    """
    """
    return obj.groupedItemsNum()
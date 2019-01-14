# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
#
# Copyright (c) 2018 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from zope.interface import implements
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.PloneMeeting.interfaces import IMeetingItemCustom


class CustomCPASLiegeMeetingItem(CustomMeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom."""
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    security.declarePublic('getExtraFieldsToCopyWhenCloning')

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc):
        """
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        """
        res = ['decisionSuite']
        return res

# ------------------------------------------------------------------------------
InitializeClass(CustomMeetingItem)

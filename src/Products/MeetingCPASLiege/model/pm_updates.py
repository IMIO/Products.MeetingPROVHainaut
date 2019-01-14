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
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import TextField

from Products.PloneMeeting.config import registerClasses
from Products.PloneMeeting.MeetingItem import MeetingItem


def update_item_schema(baseSchema):

    specificSchema = Schema((
        TextField(
            name='decisionSuite',
            widget=RichWidget(
                rows=15,
                condition="python: here.attributeIsUsed('decisionSuite')",
                label='DecisionSuite',
                label_msgid='MeetingLiege_label_decisionSuite',
                description="Decision suite descr",
                description_msgid="item_decision_suite_descr",
                i18n_domain='PloneMeeting',
            ),
            read_permission="PloneMeeting: Read decision",
            searchable=True,
            allowable_content_types=('text/html',),
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            write_permission="PloneMeeting: Write decision",
            optional=True,
        ),
    ),)
    
    baseSchema['description'].widget.description_msgid = "MeetingCPASLiege_descr_motivation"

    completeItemSchema = baseSchema + specificSchema.copy()
    return completeItemSchema


MeetingItem.schema = update_item_schema(MeetingItem.schema)

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
registerClasses()

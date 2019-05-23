# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField
from Products.CMFCore.permissions import ManagePortal
from Products.PloneMeeting.config import registerClasses
from Products.PloneMeeting.MeetingItem import MeetingItem


def update_item_schema(baseSchema):

    specificSchema = Schema((
        StringField(
            name='groupedItemsNum',
            widget=StringField._properties['widget'](
                visible=True,
                label='GroupedItemsNum',
                label_msgid='MeetingPROVHainaut_label_groupedItemsNum',
                i18n_domain='PloneMeeting',
            ),
            optional=True,
            searchable=True,
            write_permission=ManagePortal,
        ),
    ),)

    completeItemSchema = baseSchema + specificSchema.copy()
    return completeItemSchema


MeetingItem.schema = update_item_schema(MeetingItem.schema)
registerClasses()

from Products.Archetypes.atapi import Schema
from Products.PloneMeeting.MeetingItem import MeetingItem


def update_item_schema(baseSchema):
    specificSchema = Schema((

    ),)

    completeItemSchema = baseSchema + specificSchema.copy()
    completeItemSchema['optionalAdvisers'].widget.size = 10
    completeItemSchema['optionalAdvisers'].widget.format = "select"
    completeItemSchema['optionalAdvisers'].widget.description_msgid = "optional_advisers_item_descr"
    return completeItemSchema
MeetingItem.schema = update_item_schema(MeetingItem.schema)

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()

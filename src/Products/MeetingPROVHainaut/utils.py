# -*- coding: utf-8 -*-


from plone.memoize import forever
from Products.MeetingPROVHainaut.config import COMPTA_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_CEC_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_NO_CEC_ID
from Products.PloneMeeting.utils import org_id_to_uid


@forever.memoize
def compta_group_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(COMPTA_GROUP_ID, raise_on_error=raise_on_error)


@forever.memoize
def finance_group_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(FINANCE_GROUP_ID, raise_on_error=raise_on_error)


@forever.memoize
def finance_group_cec_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(FINANCE_GROUP_CEC_ID, raise_on_error=raise_on_error)


@forever.memoize
def finance_group_no_cec_uid(raise_on_error=False):
    """ """
    return org_id_to_uid(FINANCE_GROUP_NO_CEC_ID, raise_on_error=raise_on_error)


@forever.memoize
def finance_group_uids(raise_on_error=False):
    """ """
    return (finance_group_uid(), finance_group_cec_uid(), finance_group_no_cec_uid())

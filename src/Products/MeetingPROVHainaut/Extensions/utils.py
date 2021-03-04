# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective.contact.plonegroup.utils import get_organizations
from plone import api
from Products.CMFCore.exceptions import BadRequest
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting.utils import org_id_to_uid

import csv
import unicodedata


def import_meetingsUsersAndRoles_from_csv(self, fname=None):
    """
      Import the users and attribute roles from the 'csv file' (fname received as parameter)
    """

    member = api.user.get_current()
    if not member.has_role('Manager'):
        raise Unauthorized('You must be a Manager to access this script !')

    if not fname:
        return "This script needs a 'fname' parameter"

    if not hasattr(self, 'portal_plonemeeting'):
        return "PloneMeeting must be installed to run this script !"

    try:
        file = open(fname, "rb")
        reader = csv.DictReader(file)
    except Exception, msg:
        file.close()
        return "Error with file : %s" % msg.value

    out = []

    acl = self.acl_users
    pms = api.portal.get_tool('portal_membership')
    pgr = api.portal.get_tool('portal_groups')
    registration = api.portal.get_tool('portal_registration')
    ORGANIZATIONS = get_organizations()

    for row in reader:
        row_id = normalizeString(row['username'], self)
        # add users if not exist
        if row_id not in [ud['userid'] for ud in acl.searchUsers()]:
            pms.addMember(row_id, row['password'], ('Member',), [])
            member = pms.getMemberById(row_id)
            properties = {'fullname': row['fullname'], 'email': row['email']}
            failMessage = registration.testPropertiesValidity(properties, member)
            if failMessage is not None:
                raise BadRequest(failMessage)
            member.setMemberProperties(properties)
            out.append("User '%s' is added" % row_id)
        else:
            out.append("User %s already exists" % row_id)
        # attribute roles

        group_title = safe_unicode(row['grouptitle'])
        org_id = normalizeString(group_title, self)
        for organization in ORGANIZATIONS:
            if normalized_org_titles_equals(organization.Title(), group_title):
                org_id = organization.id

        org_uid = org_id_to_uid(org_id)

        plone_groups = []
        if row['observers']:
            plone_groups.append(org_uid + '_observers')
        if row['creators']:
            plone_groups.append(org_uid + '_creators')
        if row['level1reviewers']:
            plone_groups.append(org_uid + '_level1reviewers')
        if row['level2reviewers']:
            plone_groups.append(org_uid + '_level2reviewers')
        if row['level3reviewers']:
            plone_groups.append(org_uid + '_level3reviewers')
        if row['level4reviewers']:
            plone_groups.append(org_uid + '_level4reviewers')
        if row['advisers']:
            plone_groups.append(org_uid + '_advisers')
        for plone_group_id in plone_groups:
            try:
                pgr.addPrincipalToGroup(row_id, plone_group_id)
                out.append("    -> Added in group '%s'" % plone_group_id)
            except KeyError:
                out.append("    -x-> Could not add in group '%s'" % plone_group_id)

    file.close()

    return '\n'.join(out)


def normalized_org_titles_equals(title1, title2):
    """
    Is title1 normalized equals title2 normalized ?
    :return: True if equals, False if not
    """
    normalized_title_1 = unicodedata.normalize('NFKD', safe_unicode(title1)).encode('ASCII', 'ignore')
    normalized_title_2 = unicodedata.normalize('NFKD', safe_unicode(title2)).encode('ASCII', 'ignore')
    return normalized_title_1 == normalized_title_2

# -*- coding: utf-8 -*-
#
# File: MeetingCPASLalouviere.py
#
# Copyright (c) 2015 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre Nuyens <andre@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from collections import OrderedDict


PROJECTNAME = "MeetingCPASLalouviere"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# the id of the collection querying finance advices
FINANCE_ADVICES_COLLECTION_ID = 'searchitemswithfinanceadvice'

from Products.PloneMeeting import config as PMconfig
CPASLALOUVIEREROLES = {}
CPASLALOUVIEREROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
CPASLALOUVIEREROLES['n1'] = 'MeetingN1'
CPASLALOUVIEREROLES['n2'] = 'MeetingN2'
CPASLALOUVIEREROLES['secretaire'] = 'MeetingSecretaire'
PMconfig.MEETINGROLES.update(CPASLALOUVIEREROLES)

PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()
#the president will use the default 'MeetingReviewer' role

STYLESHEETS = [{'id': 'meetingcpaslalouviere.css',
                'title': "MeetingCPASLalouvière CSS styles"}]

CPASLALOUVIEREMEETINGREVIEWERS = OrderedDict([('reviewers', 'proposed_to_president'),
                                            ('secretaire', 'proposed_to_secretaire'),
                                            ('n2', 'proposed_to_n2'),
                                            ('n1', 'proposed_to_n1'), ])
PMconfig.MEETINGREVIEWERS = CPASLALOUVIEREMEETINGREVIEWERS

# -*- coding: utf-8 -*-

from Products.PloneMeeting import config as PMconfig


product_globals = globals()

PROJECTNAME = "MeetingPROVHainaut"
FINANCE_GROUP_ID = 'dirfin'
FINANCE_GROUP_CEC_ID = 'dirfincec'
FINANCE_GROUP_NO_CEC_ID = 'dirfinnocec'

PMconfig.MEETING_GROUP_SUFFIXES = [
    {'fct_title': u'advisers',
     'fct_id': u'advisers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'creators',
     'fct_id': u'creators',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'observers',
     'fct_id': u'observers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'prereviewers',
     'fct_id': u'prereviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'reviewers',
     'fct_id': u'reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'level1reviewers',
     'fct_id': u'level1reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'level2reviewers',
     'fct_id': u'level2reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'level3reviewers',
     'fct_id': u'level3reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'level4reviewers',
     'fct_id': u'level4reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'level5reviewers',
     'fct_id': u'level5reviewers',
     'fct_orgs': [],
     'fct_management': False,
     'enabled': True},
]

PMconfig.EXTRA_GROUP_SUFFIXES = [
    {'fct_title': u'financialprecontrollers',
     'fct_id': u'financialprecontrollers',
     'fct_orgs': [FINANCE_GROUP_ID, FINANCE_GROUP_CEC_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialcontrollers',
     'fct_id': u'financialcontrollers',
     'fct_orgs': [FINANCE_GROUP_ID, FINANCE_GROUP_CEC_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialeditors',
     'fct_id': u'financialeditors',
     'fct_orgs': [FINANCE_GROUP_ID, FINANCE_GROUP_NO_CEC_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialreviewers',
     'fct_id': u'financialreviewers',
     'fct_orgs': [FINANCE_GROUP_ID, FINANCE_GROUP_CEC_ID, FINANCE_GROUP_NO_CEC_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialmanagers',
     'fct_id': u'financialmanagers',
     'fct_orgs': [FINANCE_GROUP_ID, FINANCE_GROUP_CEC_ID, FINANCE_GROUP_NO_CEC_ID],
     'fct_management': False,
     'enabled': True},
]

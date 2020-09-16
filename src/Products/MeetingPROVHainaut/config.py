# -*- coding: utf-8 -*-

from Products.PloneMeeting import config as PMconfig


product_globals = globals()

PROJECTNAME = "MeetingPROVHainaut"
COMPTA_GROUP_ID = 'comptabilite'
FINANCE_GROUP_ID = 'dirfin'
FINANCE_GROUP_CEC_ID = 'dirfincec'
FINANCE_GROUP_NO_CEC_ID = 'dirfinnocec'

ADVICE_CATEGORIES = (
    ('comptabilite', u'Passage à la CEC'),
    ('df', u'Directeur financier'),
)

ADVICE_STATES_ALIVE = ('advice_under_edit',
                       'proposed_to_financial_controller',
                       'proposed_to_financial_editor',
                       'proposed_to_financial_reviewer',
                       'proposed_to_financial_manager',
                       'financial_advice_signed', )


PMconfig.ADVICE_STATES_ALIVE = ADVICE_STATES_ALIVE

PMconfig.EXTRA_GROUP_SUFFIXES = [
    {'fct_title': u'financialprecontrollers',
     'fct_id': u'financialprecontrollers',
     'fct_orgs': [FINANCE_GROUP_ID, COMPTA_GROUP_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialcontrollers',
     'fct_id': u'financialcontrollers',
     'fct_orgs': [FINANCE_GROUP_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialeditors',
     'fct_id': u'financialeditors',
     'fct_orgs': [FINANCE_GROUP_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialreviewers',
     'fct_id': u'financialreviewers',
     'fct_orgs': [FINANCE_GROUP_ID, COMPTA_GROUP_ID],
     'fct_management': False,
     'enabled': True},
    {'fct_title': u'financialmanagers',
     'fct_id': u'financialmanagers',
     'fct_orgs': [FINANCE_GROUP_ID, COMPTA_GROUP_ID],
     'fct_management': False,
     'enabled': True},
]

# -*- coding: utf-8 -*-

from collective.contact.plonegroup.config import PLONEGROUP_ORG
from copy import deepcopy
from Products.MeetingCommunes.profiles.zones import import_data as zones_import_data
from Products.MeetingPROVHainaut.config import COMPTA_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_ID
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor


# File types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision', u'attach.png',
                                         relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis', u'attach.png',
                                 relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe', u'attach.png', relatedTo='meeting')

# Categories -------------------------------------------------------------------
categories = [
    CategoryDescriptor(u'assurances', u"Assurances"),
    CategoryDescriptor(u'autorites-provinciales', u"Autorités provinciales"),
    CategoryDescriptor(u'contentieux', u"Contentieux"),
    CategoryDescriptor(u'elections', u"Élections"),
    CategoryDescriptor(u'intercommunales', u"Intercommunales"),
    CategoryDescriptor(u'missions-et-deplacements', u"Missions et déplacements"),
]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('role', 'Rôle')
agendaTemplate.is_reusable = True
agendaTemplate.odt_file = 'role.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['Meeting']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'
agendaTemplate.style_template = ['styles1']

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.is_reusable = True
decisionsTemplate.odt_file = 'pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meeting']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'
decisionsTemplate.style_template = ['styles1']

noteTemplate = PodTemplateDescriptor('note', 'Note')
noteTemplate.is_reusable = True
noteTemplate.odt_file = 'note.odt'
noteTemplate.pod_formats = ['odt', 'pdf', ]
noteTemplate.pod_portal_types = ['MeetingItem']
noteTemplate.tal_condition = u'python:tool.isManager(here)'
noteTemplate.style_template = ['styles1']

templates = [agendaTemplate, decisionsTemplate, noteTemplate]

orgs = deepcopy(zones_import_data.data.orgs)
dirfin = [org for org in orgs if org.id == FINANCE_GROUP_ID][0]
dirfin.item_advice_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
dirfin.item_advice_edit_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
dirfin.item_advice_view_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
compta = [org for org in orgs if org.id == COMPTA_GROUP_ID][0]
compta.item_advice_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
compta.item_advice_edit_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
compta.item_advice_view_states = [
    u'cfg1__state__proposedToValidationLevel1__or__proposedToValidationLevel2__or__proposedToValidationLevel3_waiting_advices']
dirgen = [org for org in orgs if org.id == 'dirgen'][0]
dirgen.level1reviewers = deepcopy(dirgen.creators)
dirgen.level2reviewers = deepcopy(dirgen.creators)
dirgen.level3reviewers = deepcopy(dirgen.creators)

# create associated groups and groups in charge
ag1 = OrgDescriptor('ag1', 'Associated group 1', u'AG1', active=False)
ag2 = OrgDescriptor('ag2', 'Associated group 2', u'AG2', active=False)
ag3 = OrgDescriptor('ag3', 'Associated group 3', u'AG3', active=False)
ag4 = OrgDescriptor('ag4', 'Associated group 4', u'AG4', active=False)
ag5 = OrgDescriptor('ag5', 'Associated group 5', u'AG5', active=False)
gic1 = OrgDescriptor('dp-eric-massin', 'DP Éric Massin', u'DPEM')
gic2 = OrgDescriptor('dp-fabienne-capot', 'DP Fabienne Capot', u'DPFC')
gic3 = OrgDescriptor('dp-fabienne-devilers', 'DP Fabienne Devilers', u'DPFD')
gic4 = OrgDescriptor('dp-pascal-lafosse', 'DP Pascal Lafosse', u'DPPL')
gic5 = OrgDescriptor('dp-serge-hustache', 'DP Serge Hustache', u'DPSH')

orgs += [ag1, ag2, ag3, ag4, ag5, gic1, gic2, gic3, gic4, gic5]

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(zones_import_data.collegeMeeting)
collegeMeeting.podTemplates = templates
collegeMeeting.usedItemAttributes = collegeMeeting.usedItemAttributes + \
    ['completeness', 'associatedGroups', 'groupsInCharge']
collegeMeeting.workflowAdaptations = ('apply_item_validation_levels',
                                      'no_global_observation',
                                      'only_creator_may_delete',
                                      'no_publication',
                                      'no_proposal',
                                      'presented_item_back_to_itemcreated',
                                      'return_to_proposing_group',
                                      'waiting_advices_from_last_validation_level',
                                      'postpone_next_meeting',
                                      'refused',
                                      'meetingadvicefinances_add_advicecreated_state',
                                      'meetingadvicefinances_controller_propose_to_manager')
collegeMeeting.itemWFValidationLevels = (
    {'leading_transition': '',
     'state_title': 'itemcreated',
     'suffix': 'creators',
     'enabled': '1',
     'state': 'itemcreated',
     'back_transition_title': 'backToItemCreated',
     'back_transition': 'backToItemCreated',
     'leading_transition_title': '',
     'extra_suffixes': []},
    {'leading_transition': 'propose',
     'state_title': 'proposed',
     'suffix': 'reviewers',
     'enabled': '0',
     'state': 'proposed',
     'back_transition_title': 'backToProposed',
     'back_transition': 'backToProposed',
     'leading_transition_title': 'propose',
     'extra_suffixes': []},
    {'leading_transition': 'prevalidate',
     'state_title': 'prevalidated',
     'suffix': 'reviewers',
     'enabled': '0',
     'state': 'prevalidated',
     'back_transition_title': 'backToPrevalidated',
     'back_transition': 'backToPrevalidated',
     'leading_transition_title': 'prevalidate',
     'extra_suffixes': []},
    {'leading_transition': 'proposeToValidationLevel1',
     'state_title': 'proposedToValidationLevel1',
     'suffix': 'level1reviewers',
     'enabled': '1',
     'state': 'proposedToValidationLevel1',
     'back_transition_title': 'backToProposedToValidationLevel1',
     'back_transition': 'backToProposedToValidationLevel1',
     'leading_transition_title': 'proposeToValidationLevel1',
     'extra_suffixes': []},
    {'leading_transition': 'proposeToValidationLevel2',
     'state_title': 'proposedToValidationLevel2',
     'suffix': 'level2reviewers',
     'enabled': '1',
     'state': 'proposedToValidationLevel2',
     'back_transition_title': 'backToProposedToValidationLevel2',
     'back_transition': 'backToProposedToValidationLevel2',
     'leading_transition_title': 'proposeToValidationLevel2',
     'extra_suffixes': []},
    {'leading_transition': 'proposeToValidationLevel3',
     'state_title': 'proposedToValidationLevel3',
     'suffix': 'level3reviewers',
     'enabled': '1',
     'state': 'proposedToValidationLevel3',
     'back_transition_title': 'backToProposedToValidationLevel3',
     'back_transition': 'backToProposedToValidationLevel3',
     'leading_transition_title': 'proposeToValidationLevel3',
     'extra_suffixes': []},
    {'leading_transition': 'proposeToValidationLevel4',
     'state_title': 'proposedToValidationLevel4',
     'suffix': 'level4reviewers',
     'enabled': '0',
     'state': 'proposedToValidationLevel4',
     'back_transition_title': 'backToProposedToValidationLevel4',
     'back_transition': 'backToProposedToValidationLevel4',
     'leading_transition_title': 'proposeToValidationLevel4',
     'extra_suffixes': []},
    {'leading_transition': 'proposeToValidationLevel5',
     'state_title': 'proposedToValidationLevel5',
     'suffix': 'level5reviewers',
     'enabled': '0',
     'state': 'proposedToValidationLevel5',
     'back_transition_title': 'backToProposedToValidationLevel5',
     'back_transition': 'backToProposedToValidationLevel5',
     'leading_transition_title': 'proposeToValidationLevel5',
     'extra_suffixes': []},
)
collegeMeeting.transitionsForPresentingAnItem = ('proposeToValidationLevel1',
                                                 'proposeToValidationLevel2',
                                                 'proposeToValidationLevel3',
                                                 'validate',
                                                 'present')
collegeMeeting.transitionsToConfirm = []
collegeMeeting.usedAdviceTypes = collegeMeeting.usedAdviceTypes + [u'asked_again']
collegeMeeting.itemBudgetInfosStates = []
collegeMeeting.orderedContacts = []
collegeMeeting.orderedAssociatedOrganizations = [
    PLONEGROUP_ORG + '/ag1',
    PLONEGROUP_ORG + '/ag2',
    PLONEGROUP_ORG + '/ag3',
    PLONEGROUP_ORG + '/ag4',
    PLONEGROUP_ORG + '/ag5']
collegeMeeting.orderedGroupsInCharge = [
    PLONEGROUP_ORG + '/gic1',
    PLONEGROUP_ORG + '/gic2',
    PLONEGROUP_ORG + '/gic3',
    PLONEGROUP_ORG + '/gic4',
    PLONEGROUP_ORG + '/gic5']
collegeMeeting.categories = categories
collegeMeeting.useGroupsAsCategories = False
collegeMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_groups_in_charge', 'reverse': '0'},
    {'insertingMethod': 'on_categories', 'reverse': '0'},
    {'insertingMethod': 'on_all_associated_groups', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})

# Council
councilMeeting = deepcopy(zones_import_data.councilMeeting)
councilMeeting.podTemplates = []
councilMeeting.workflowAdaptations = ('apply_item_validation_levels',
                                      'no_global_observation',
                                      'only_creator_may_delete',
                                      'no_publication',
                                      'refused')
councilMeeting.transitionsToConfirm = []
councilMeeting.itemBudgetInfosStates = []
councilMeeting.orderedContacts = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=[collegeMeeting, councilMeeting],
    orgs=orgs)

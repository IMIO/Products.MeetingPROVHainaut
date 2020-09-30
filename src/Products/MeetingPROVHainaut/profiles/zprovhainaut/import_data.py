# -*- coding: utf-8 -*-

from collective.contact.plonegroup.config import PLONEGROUP_ORG
from copy import deepcopy
from Products.MeetingCommunes.profiles.examples_fr import import_data as examples_fr_import_data
from Products.MeetingCommunes.profiles.zones import import_data as zones_import_data
from Products.MeetingPROVHainaut.config import COMPTA_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_ID
from Products.PloneMeeting.MeetingConfig import defValues
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor


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
templates = []

delibTemplate = PodTemplateDescriptor('delib', 'Délibération')
delibTemplate.is_reusable = True
delibTemplate.odt_file = 'deliberation.odt'
delibTemplate.pod_formats = ['docx', 'pdf', ]
delibTemplate.pod_portal_types = ['MeetingItem']
templates.append(delibTemplate)

arreteTemplate = PodTemplateDescriptor('arrete', 'Arrêté')
arreteTemplate.is_reusable = True
arreteTemplate.odt_file = 'arrete.odt'
arreteTemplate.pod_formats = ['docx', 'pdf', ]
arreteTemplate.pod_portal_types = ['MeetingItem']
templates.append(arreteTemplate)

roleATemplate = PodTemplateDescriptor('role-a', 'Rôle A')
roleATemplate.is_reusable = True
roleATemplate.odt_file = 'role.odt'
roleATemplate.pod_formats = ['docx', 'pdf', ]
roleATemplate.pod_portal_types = ['Meeting']
roleATemplate.context_variables = [{'name': u'role', 'value': u'A'},
                                   {'name': u'toDiscuss', 'value': u'False'},
                                   {'name': u'listTypes', 'value': u'normal'}]
templates.append(roleATemplate)

roleBTemplate = PodTemplateDescriptor('role-b', 'Rôle B')
roleBTemplate.pod_template_to_use = {'cfg_id': 'meeting-config-zcollege', 'template_id': 'role-a'}
roleBTemplate.pod_formats = ['docx', 'pdf', ]
roleBTemplate.pod_portal_types = ['Meeting']
roleBTemplate.context_variables = [{'name': u'role', 'value': u'B'},
                                   {'name': u'toDiscuss', 'value': u'True'},
                                   {'name': u'listTypes', 'value': u'normal'}]
templates.append(roleBTemplate)

roleSTemplate = PodTemplateDescriptor('role-s', 'Rôle S')
roleSTemplate.pod_template_to_use = {'cfg_id': 'meeting-config-zcollege', 'template_id': 'role-a'}
roleSTemplate.pod_formats = ['docx', 'pdf', ]
roleSTemplate.pod_portal_types = ['Meeting']
roleSTemplate.context_variables = [{'name': u'role', 'value': u'S'},
                                   {'name': u'toDiscuss', 'value': u'True'},
                                   {'name': u'listTypes', 'value': u'late'}]
templates.append(roleSTemplate)

presencesTemplate = PodTemplateDescriptor('presences', 'Présences')
presencesTemplate.is_reusable = True
presencesTemplate.odt_file = 'presences.odt'
presencesTemplate.pod_formats = ['docx', 'pdf', ]
presencesTemplate.pod_portal_types = ['Meeting']
templates.append(presencesTemplate)

pvTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
pvTemplate.is_reusable = True
pvTemplate.odt_file = 'pv.odt'
pvTemplate.pod_formats = ['docx', 'pdf', ]
pvTemplate.pod_portal_types = ['Meeting']
templates.append(pvTemplate)

groupedItemsTemplate = PodTemplateDescriptor('grouped-items', 'Tous les bordereaux')
groupedItemsTemplate.odt_file = 'bordereaux.odt'
groupedItemsTemplate.pod_formats = ['docx', 'pdf', ]
groupedItemsTemplate.pod_portal_types = ['Meeting']
groupedItemsTemplate.merge_templates = [{'pod_context_name': u'delib',
                                         'do_rendering': False,
                                         'template': 'arrete'}]
templates.append(groupedItemsTemplate)

orgs = deepcopy(zones_import_data.data.orgs)
dirfin = [org for org in orgs if org.id == FINANCE_GROUP_ID][0]
dirfin.item_advice_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfin.item_advice_edit_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfin.item_advice_view_states = []
dfin = deepcopy(examples_fr_import_data.dfin)
dirfin.advisers.append(dfin)
dirfin.financialprecontrollers.append(dfin)
dirfin.financialcontrollers.append(dfin)
dirfin.financialeditors.append(dfin)
dirfin.financialreviewers.append(dfin)
dirfin.financialmanagers.append(dfin)

compta = [org for org in orgs if org.id == COMPTA_GROUP_ID][0]
compta.item_advice_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
compta.item_advice_edit_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
compta.item_advice_view_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']

# extra dirfin groups
# CEC
dirfincec = OrgDescriptor('dirfincec', 'Directeur Financier (CEC)', u'DFCEC')
dirfincec.item_advice_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfincec.item_advice_edit_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfincec.item_advice_view_states = []
# NO CEC
dirfinnocec = OrgDescriptor('dirfinnocec', 'Directeur Financier (NO CEC)', u'DFNOCEC')
dirfinnocec.item_advice_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfinnocec.item_advice_edit_states = [
    u'cfg1__state__itemcreated__or__proposedToValidationLevel1__or__proposedToValidationLevel2'
    u'__or__proposedToValidationLevel3__or__proposedToValidationLevel4_waiting_advices']
dirfinnocec.item_advice_view_states = []

# assign user 'dgen' to 'dirgen' and 'secretariat' extra validation levels
dirgen = [org for org in orgs if org.id == 'dirgen'][0]
dirgen.level1reviewers = deepcopy(dirgen.creators)
dirgen.level2reviewers = deepcopy(dirgen.creators)
dirgen.level3reviewers = deepcopy(dirgen.creators)
secr = [org for org in orgs if org.id == 'secretariat'][0]
secr.level1reviewers = deepcopy(secr.creators)
secr.level2reviewers = deepcopy(secr.creators)
secr.level3reviewers = deepcopy(secr.creators)

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

orgs += [dirfincec, dirfinnocec, ag1, ag2, ag3, ag4, ag5, gic1, gic2, gic3, gic4, gic5]

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(zones_import_data.collegeMeeting)
collegeMeeting.podTemplates = templates
collegeMeeting.usedItemAttributes = (
    u'budgetInfos', u'groupsInCharge', u'associatedGroups',
    u'motivation', u'toDiscuss', u'inAndOutMoves',
    u'notes', u'marginalNotes', u'observations',
    u'manuallyLinkedItems', u'otherMeetingConfigsClonableToPrivacy',
    u'completeness', u'groupedItemsNum')
collegeMeeting.usedMeetingAttributes = (
    u'startDate', u'endDate', u'attendees',
    u'excused', u'absents', u'signatories',
    u'place', u'extraordinarySession', u'inAndOutMoves',
    u'notes', u'observations')
collegeMeeting.workflowAdaptations = (
    'meetingadvicefinances_add_advicecreated_state',
    'meetingadvicefinances_controller_propose_to_manager',
    'accepted_but_modified',
    'refused',
    'delayed',
    'presented_item_back_to_itemcreated',
    'postpone_next_meeting',
    'no_publication',
    'only_creator_may_delete',
    'waiting_advices',
    'waiting_advices_given_advices_required_to_validate',
    'waiting_advices_from_before_last_val_level',
    'waiting_advices_from_last_val_level',
    'waiting_advices_adviser_send_back',
    'waiting_advices_adviser_may_validate')
collegeMeeting.dashboardItemsListingsFilters = (
    u'c4', u'c5', u'c6', u'c7', u'c8', u'c9',
    u'c10', u'c11', u'c13', u'c14', u'c15',
    u'c16', u'c18', u'c19', u'c23', u'c27')
collegeMeeting.dashboardMeetingAvailableItemsFilters = (
    u'c4', u'c5', u'c7', u'c8', u'c11', u'c16', u'c23', u'c27')
collegeMeeting.dashboardMeetingLinkedItemsFilters = (
    u'c4', u'c5', u'c6', u'c7', u'c8', u'c11', u'c12', u'c16', u'c19', u'c23')
collegeMeeting.itemColumns = (
    u'Creator', u'CreationDate', u'ModificationDate',
    u'review_state', u'getCategory', u'proposing_group_acronym',
    u'associated_groups_acronym', u'groups_in_charge_acronym',
    u'advices', u'toDiscuss', u'linkedMeetingDate', u'actions')
collegeMeeting.availableItemsListVisibleColumns = (
    u'Creator', u'getCategory', u'proposing_group_acronym',
    u'associated_groups_acronym', u'groups_in_charge_acronym',
    u'advices', u'toDiscuss', u'getPreferredMeetingDate', u'actions')
collegeMeeting.itemsListVisibleColumns = (
    u'static_item_reference', u'Creator', u'review_state',
    u'getCategory', u'proposing_group_acronym', u'associated_groups_acronym',
    u'groups_in_charge_acronym', u'advices', u'toDiscuss', u'actions')
collegeMeeting.itemActionsInterface = \
    'Products.MeetingPROVHainaut.interfaces.IMeetingItemPROVHainautWorkflowActions'
collegeMeeting.itemConditionsInterface = \
    'Products.MeetingPROVHainaut.interfaces.IMeetingItemPROVHainautWorkflowConditions'
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
     'enabled': '1',
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
collegeMeeting.transitionsForPresentingAnItem = (
    'proposeToValidationLevel1', 'proposeToValidationLevel2',
    'proposeToValidationLevel3', 'validate', 'present')
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
    PLONEGROUP_ORG + '/dp-eric-massin',
    PLONEGROUP_ORG + '/dp-fabienne-capot',
    PLONEGROUP_ORG + '/dp-fabienne-devilers',
    PLONEGROUP_ORG + '/dp-pascal-lafosse',
    PLONEGROUP_ORG + '/dp-serge-hustache']
collegeMeeting.categories = categories
collegeMeeting.useGroupsAsCategories = False
collegeMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_groups_in_charge', 'reverse': '0'},
    {'insertingMethod': 'on_categories', 'reverse': '0'},
    {'insertingMethod': 'on_all_associated_groups', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
# remove pre_accepted as not used
collegeMeeting.itemAdviceViewStates = ('validated',
                                       'presented',
                                       'itemfrozen',
                                       'accepted',
                                       'refused',
                                       'accepted_but_modified',
                                       'delayed')
collegeMeeting.defaultAdviceHiddenDuringRedaction = (
    'meetingadvicefinances',
    'meetingadvicefinancescec',
    'meetingadvicefinancesnocec')
collegeMeeting.powerObservers = defValues.powerObservers
collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approbation du procès-verbal de la séance du xx/xx/20xx',
        category='autorites-provinciales',
        proposingGroup='dirgen',
        decision='<p>Procès-verbal approuvé</p>'), ]
collegeMeeting.recurringItems[0].groupsInCharge = 'dirgen'

# Council
councilMeeting = deepcopy(zones_import_data.councilMeeting)
councilMeeting.podTemplates = []
councilMeeting.workflowAdaptations = ('only_creator_may_delete',
                                      'no_publication',
                                      'refused',
                                      'delayed',
                                      'accepted_but_modified',)
councilMeeting.transitionsToConfirm = []
councilMeeting.itemBudgetInfosStates = []
councilMeeting.orderedContacts = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=[collegeMeeting, councilMeeting],
    orgs=orgs)

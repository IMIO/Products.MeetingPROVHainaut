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
    CategoryDescriptor(u'category1', u"Catégorie1", categoryId='1'),
    CategoryDescriptor(u'category2', u"Catégorie2", categoryId='2'),
    CategoryDescriptor(u'category3', u"Catégorie3", categoryId='3'),
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
dirfin.item_advice_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
dirfin.item_advice_edit_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
dirfin.item_advice_view_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta = [org for org in orgs if org.id == COMPTA_GROUP_ID][0]
compta.item_advice_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta.item_advice_edit_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta.item_advice_view_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']

# create associated groups and groups in charge
ag1 = OrgDescriptor('ag1', 'Associated group 1', u'AG1', active=False)
ag2 = OrgDescriptor('ag2', 'Associated group 2', u'AG2', active=False)
ag3 = OrgDescriptor('ag3', 'Associated group 3', u'AG3', active=False)
ag4 = OrgDescriptor('ag4', 'Associated group 4', u'AG4', active=False)
ag5 = OrgDescriptor('ag5', 'Associated group 5', u'AG5', active=False)
gic1 = OrgDescriptor('gic1', 'Group in charge 1', u'GIC1')
gic2 = OrgDescriptor('gic2', 'Group in charge 2', u'GIC2')
gic3 = OrgDescriptor('gic3', 'Group in charge 3', u'GIC3')
gic4 = OrgDescriptor('gic4', 'Group in charge 4', u'GIC4')
gic5 = OrgDescriptor('gic5', 'Group in charge 5', u'GIC5')

orgs += [ag1, ag2, ag3, ag4, ag5, gic1, gic2, gic3, gic4, gic5]

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(zones_import_data.collegeMeeting)
collegeMeeting.podTemplates = templates
collegeMeeting.usedItemAttributes = collegeMeeting.usedItemAttributes + \
    ['completeness', 'associatedGroups', 'groupsInCharge']
collegeMeeting.workflowAdaptations = ('no_global_observation',
                                      'only_creator_may_delete',
                                      'pre_validation',
                                      'no_publication',
                                      'presented_item_back_to_itemcreated',
                                      'presented_item_back_to_proposed',
                                      'return_to_proposing_group',
                                      'waiting_advices',
                                      'refused',
                                      'meetingadvicefinances_add_advicecreated_state',
                                      'meetingadvicefinances_controller_propose_to_manager')
collegeMeeting.transitionsForPresentingAnItem = ('propose',
                                                 'prevalidate',
                                                 'validate',
                                                 'present')
collegeMeeting.usedAdviceTypes = collegeMeeting.usedAdviceTypes + [u'asked_again']
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

# Council
councilMeeting = deepcopy(zones_import_data.councilMeeting)
councilMeeting.podTemplates = []
councilMeeting.orderedContacts = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=[collegeMeeting, councilMeeting],
    orgs=orgs)

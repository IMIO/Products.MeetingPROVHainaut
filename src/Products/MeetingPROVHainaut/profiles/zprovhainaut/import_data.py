# -*- coding: utf-8 -*-

from copy import deepcopy

from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.MeetingCommunes.profiles.zones import import_data as zones_import_data
from Products.MeetingPROVHainaut.config import COMPTA_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_ID

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

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(zones_import_data.collegeMeeting)
collegeMeeting.podTemplates = templates
collegeMeeting.usedItemAttributes = collegeMeeting.usedItemAttributes + ['completeness']
collegeMeeting.workflowAdaptations = ('no_global_observation',
                                      'only_creator_may_delete',
                                      'pre_validation',
                                      'no_publication',
                                      'presented_item_back_to_itemcreated',
                                      'presented_item_back_to_proposed',
                                      'return_to_proposing_group',
                                      'waiting_advices',
                                      'refused')
collegeMeeting.transitionsForPresentingAnItem = ('propose',
                                                 'prevalidate',
                                                 'validate',
                                                 'present')
collegeMeeting.usedAdviceTypes = collegeMeeting.usedAdviceTypes + [u'asked_again']

# Council
councilMeeting = deepcopy(zones_import_data.councilMeeting)
councilMeeting.podTemplates = []

orgs = deepcopy(zones_import_data.data.orgs)
dirfin = [org for org in orgs if org.id == FINANCE_GROUP_ID][0]
dirfin.item_advice_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
dirfin.item_advice_edit_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
dirfin.item_advice_view_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta = [org for org in orgs if org.id == COMPTA_GROUP_ID][0]
compta.item_advice_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta.item_advice_edit_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']
compta.item_advice_view_states = [u'cfg1__state__proposed__or__prevalidated_waiting_advices']

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=[collegeMeeting, councilMeeting],
    orgs=zones_import_data.data.orgs)

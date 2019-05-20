# -*- coding: utf-8 -*-

from copy import deepcopy

from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.MeetingCommunes.profiles.zones import import_data as zones_import_data

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
collegeMeeting = deepcopy(zones_import_data.collegeMeeting)
collegeMeeting.podTemplates = templates

councilMeeting = deepcopy(zones_import_data.councilMeeting)
councilMeeting.podTemplates = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=[collegeMeeting, councilMeeting],
    orgs=zones_import_data.data.orgs)
data.configGroups = (
    {'row_id': 'bep', 'label': 'BEP'},
    {'row_id': 'expa', 'label': 'EXPA'},
    {'row_id': 'enviro', 'label': 'ENVIRO'},
    {'row_id': 'crema', 'label': 'CREMA'},
    {'row_id': 'idefin', 'label': 'IDEFIN'},
)

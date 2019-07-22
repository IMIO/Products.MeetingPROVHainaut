# -*- coding: utf-8 -*-

from collective.eeafaceted.dashboard.utils import addFacetedCriteria
from imio.helpers.catalog import addOrUpdateIndexes
from plone import api
from Products.CMFPlone.utils import _createObjectByType
from Products.MeetingCommunes.config import SAMPLE_TEXT
from Products.MeetingCommunes.setuphandlers import _showHomeTab
from Products.MeetingCommunes.setuphandlers import logStep
from Products.MeetingPROVHainaut.config import COMPTA_GROUP_ID
from Products.MeetingPROVHainaut.config import FINANCE_GROUP_ID
from Products.MeetingPROVHainaut.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.utils import org_id_to_uid
from DateTime import DateTime

import os


def isMeetingPROVHainautProfile(context):
    return context.readDataFile("MeetingPROVHainaut_marker.txt") or \
        context.readDataFile("MeetingPROVHainaut_zprovhainaut_marker.txt") or \
        context.readDataFile("MeetingPROVHainaut_testing_marker.txt")


def isMeetingPROVHainautConfigureProfile(context):
    return context.readDataFile("MeetingPROVHainaut_zprovhainaut_marker.txt") or \
        context.readDataFile("MeetingPROVHainaut_testing_marker.txt")


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if not isMeetingPROVHainautProfile(context):
        return

    logStep("postInstall", context)
    site = context.getSite()
    addOrUpdateIndexes(site, {'getGroupedItemsNum': ('FieldIndex', {})})
    _showHomeTab(context, site)
    logStep("reorderSkinsLayers", context)
    _reorderSkinsLayers(context, site)
    logStep("_addFacetedCriteria", context)
    _addFacetedCriteria()


def initializeTool(context):
    """Initialises the PloneMeeting tool based on information from the current profile."""
    if not isMeetingPROVHainautConfigureProfile(context):
        return

    logStep("initializeTool", context)
    return ToolInitializer(context, PROJECTNAME).run()


def _reorderSkinsLayers(context, site):
    """Re-apply MeetingPROVHainaut skins.xml step to be sure the order is correct."""
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.PloneMeeting:default', 'skins')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingPROVHainaut:default', 'skins')
    except KeyError:
        # if the plonemeetingskin or imioapps profile is not available
        # (not using plonemeetingskin, imioapps or in testing?) we pass...
        pass


def finalizeInstance(context):
    """Called at the very end of the installation process (after PloneMeeting)."""
    if not isMeetingPROVHainautProfile(context):
        return

    site = context.getSite()
    _reorderSkinsLayers(context, site)
    _reorderCss(context)
    _addDemoData(site)


def _reorderCss(context):
    """Make sure CSS are correctly reordered in portal_css so things work as expected..."""
    site = context.getSite()

    logStep("reorderCss", context)
    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'MeetingPROVHainaut.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)


def _addFacetedCriteria():
    """Add our own faceted criteria."""
    tool = api.portal.get_tool('portal_plonemeeting')
    for cfg in tool.objectValues('MeetingConfig'):
        # add new faceted filters for searches_items
        addFacetedCriteria(cfg.searches.searches_items, os.path.dirname(__file__) +
                           '/faceted_conf/meetingprovhainaut_dashboard_items_widgets.xml')


def _addDemoData(site,
                 # need 2
                 proposing_groups=[FINANCE_GROUP_ID, COMPTA_GROUP_ID],
                 # need 4
                 categories=[u'assurances', u'autorites-provinciales', u'contentieux', u'intercommunales'],
                 # need 4
                 associated_groups=['ag1', 'ag2', 'ag3', 'ag4', 'ag5'],
                 # need 5
                 groupsInCharge=['dp-eric-massin', 'dp-fabienne-capot',
                                 'dp-fabienne-devilers', 'dp-pascal-lafosse', 'dp-serge-hustache']
                 ):
    """ """
    items = (
        {'title': u'Exemple point 1',
         'proposingGroup': proposing_groups[0],
         'category': categories[0],
         'associatedGroups': [associated_groups[0]],
         'groupsInCharge': [],
         },
        {'title': u'Exemple point 2',
         'proposingGroup': proposing_groups[0],
         'category': categories[2],
         'associatedGroups': [associated_groups[1]],
         'groupsInCharge': [groupsInCharge[0]],
         },
        {'title': u'Exemple point 3',
         'proposingGroup': proposing_groups[0],
         'category': categories[1],
         'associatedGroups': [associated_groups[0], associated_groups[1]],
         'groupsInCharge': [groupsInCharge[1]],
         },
        {'title': u'Exemple point 4',
         'proposingGroup': proposing_groups[1],
         'category': categories[0],
         'associatedGroups': [associated_groups[1]],
         'groupsInCharge': [groupsInCharge[1]],
         },
        {'title': u'Exemple point 5',
         'proposingGroup': proposing_groups[0],
         'category': categories[2],
         'associatedGroups': [associated_groups[1]],
         'groupsInCharge': [groupsInCharge[2]],
         },
        {'title': u'Exemple point 6',
         'proposingGroup': proposing_groups[1],
         'category': categories[1],
         'associatedGroups': [associated_groups[3]],
         'groupsInCharge': [groupsInCharge[2]],
         },
        {'title': u'Exemple point 7',
         'proposingGroup': proposing_groups[1],
         'category': categories[1],
         'associatedGroups': [],
         'groupsInCharge': [groupsInCharge[0], groupsInCharge[2]],
         },
        {'title': u'Exemple point 8',
         'proposingGroup': proposing_groups[0],
         'category': categories[1],
         'associatedGroups': [associated_groups[2]],
         'groupsInCharge': [groupsInCharge[0]],
         },
        {'title': u'Exemple point 9',
         'proposingGroup': proposing_groups[1],
         'category': categories[3],
         'associatedGroups': [associated_groups[0], associated_groups[2]],
         'groupsInCharge': [groupsInCharge[3]],
         },
        {'title': u'Exemple point 10',
         'proposingGroup': proposing_groups[0],
         'category': categories[3],
         'associatedGroups': [associated_groups[0], associated_groups[2]],
         'groupsInCharge': [groupsInCharge[0], groupsInCharge[2], groupsInCharge[3]],
         },
        {'title': u'Exemple point 11',
         'proposingGroup': proposing_groups[1],
         'category': categories[0],
         'associatedGroups': [associated_groups[2]],
         'groupsInCharge': [groupsInCharge[0], groupsInCharge[4]],
         },
        {'title': u'Exemple point 12',
         'proposingGroup': proposing_groups[0],
         'category': categories[3],
         'associatedGroups': [associated_groups[3]],
         'groupsInCharge': [groupsInCharge[3]],
         },
    )
    # create a meeting and insert items
    # first we need to be sure that our IPoneMeetingLayer is set correctly
    # https://dev.plone.org/ticket/11673
    from zope.event import notify
    from zope.traversing.interfaces import BeforeTraverseEvent
    notify(BeforeTraverseEvent(site, site.REQUEST))
    # we will create elements for some users, make sure their personal
    # area is correctly configured
    # first make sure the 'Members' folder exists
    mTool = api.portal.get_tool('portal_membership')
    wfTool = api.portal.get_tool('portal_workflow')
    tool = api.portal.get_tool('portal_plonemeeting')
    members = mTool.getMembersFolder()
    if members is None:
        _createObjectByType('Folder', site, id='Members')
    mTool.createMemberArea('dgen')
    dgenFolder = tool.getPloneMeetingFolder('meeting-config-zcollege', 'dgen')
    date = DateTime() - 1
    meeting = api.content.create(container=dgenFolder,
                                 type='MeetingZCollege',
                                 id=date.strftime('%Y%m%d'),
                                 date=date)
    meeting.processForm()

    i = 1
    cfg = tool.getMeetingConfig(meeting)
    site.REQUEST['PUBLISHED'] = meeting
    for item in items:
        newItem = api.content.create(container=dgenFolder,
                                     type='MeetingItemZCollege',
                                     id=str(i),
                                     title=item['title'],
                                     proposingGroup=org_id_to_uid(item['proposingGroup']),
                                     category=item['category'],
                                     associatedGroups=[org_id_to_uid(associatedGroup)
                                                       for associatedGroup in item['associatedGroups']],
                                     groupsInCharge=[org_id_to_uid(groupInCharge)
                                                     for groupInCharge in item['groupsInCharge']],
                                     description=SAMPLE_TEXT,
                                     motivation=SAMPLE_TEXT,
                                     decision=SAMPLE_TEXT)
        for transition in cfg.getTransitionsForPresentingAnItem():
            wfTool.doActionFor(newItem, transition)
    return meeting

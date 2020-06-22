# -*- coding: utf-8 -*-

from collective.eeafaceted.dashboard.utils import addFacetedCriteria
from DateTime import DateTime
from dexterity.localroles.utils import add_fti_configuration
from imio.helpers.catalog import addOrUpdateIndexes
from plone import api
from Products.CMFPlone.utils import _createObjectByType
from Products.MeetingCommunes.config import SAMPLE_TEXT
from Products.MeetingCommunes.setuphandlers import _showHomeTab
from Products.MeetingCommunes.setuphandlers import logStep
from Products.MeetingPROVHainaut.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.utils import org_id_to_uid

import logging
import os

logger = logging.getLogger('MeetingPROVHainaut: setuphandlers')


def postInstall(context):
    """Called as at the end of the setup process. """
    if not hasattr(context, '_profile_path'):
        profile_id = 'profile-Products.MeetingPROVHainaut:default'
        context = context._getImportContext(profile_id)
    logStep("postInstall", context)
    site = context.getSite()
    addOrUpdateIndexes(site, {'getGroupedItemsNum': ('FieldIndex', {})})
    _showHomeTab(context, site)
    logStep("_reorderSkinsLayers", context)
    _reorderSkinsLayers(context, site)
    logStep("_reorderCss", context)
    _reorderCss(context)
    logStep("_addFacetedCriteria", context)
    _addFacetedCriteria()


def post_handler_zprovhainaut(context):
    """ """
    if not hasattr(context, '_profile_path'):
        profile_id = 'profile-Products.MeetingPROVHainaut:zprovhainaut'
        context = context._getImportContext(profile_id)

    initializeAppTool(context)
    logStep("_configureDexterityLocalRolesField", context)
    _configureDexterityLocalRolesField()
    finalizePROVHainautInstance(context)


def post_handler_testing(context):
    """ """
    if not hasattr(context, '_profile_path'):
        profile_id = 'profile-Products.MeetingPROVHainaut:testing'
        context = context._getImportContext(profile_id)

    initializeAppTool(context)


def initializeAppTool(context):
    """Initialises the PloneMeeting tool based on information from the current profile."""
    logStep("initializeAppTool", context)
    return ToolInitializer(context, PROJECTNAME).run()


def _reorderSkinsLayers(context, site):
    """Re-apply MeetingPROVHainaut skins.xml step to be sure the order is correct."""
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-Products.PloneMeeting:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingPROVHainaut:default', 'skins')


def _configureDexterityLocalRolesField():
    """Configure field meetingadvice.advice_group for meetingadvicefinances."""
    # meetingadvicefinances
    roles_config = {
        'advice_group': {
            'advice_given': {
                'advisers': {'roles': [], 'rel': ''}},
            'advicecreated': {
                u'financialprecontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_controller': {
                u'financialcontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_editor': {
                u'financialeditors': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_reviewer': {
                u'financialreviewers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_manager': {
                u'financialmanagers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'financial_advice_signed': {
                u'financialmanagers': {'roles': [u'Reviewer'], 'rel': ''}},
        }
    }
    msg = add_fti_configuration(portal_type='meetingadvicefinances',
                                configuration=roles_config['advice_group'],
                                keyname='advice_group',
                                force=True)

    # meetingadvicefinancesmanager
    roles_config = {
        'advice_group': {
            'advice_given': {
                'advisers': {'roles': [], 'rel': ''}},
            'advicecreated': {
                u'financialprecontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_controller': {
                u'financialcontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_reviewer': {
                u'financialreviewers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_manager': {
                u'financialmanagers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'financial_advice_signed': {
                u'financialmanagers': {'roles': [u'Reviewer'], 'rel': ''}},
        }
    }
    msg = add_fti_configuration(portal_type='meetingadvicefinancescec',
                                configuration=roles_config['advice_group'],
                                keyname='advice_group',
                                force=True)

    # meetingadvicefinanceseditor
    roles_config = {
        'advice_group': {
            'advice_given': {
                'advisers': {'roles': [], 'rel': ''}},
            'proposed_to_financial_editor': {
                u'financialeditors': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_reviewer': {
                u'financialreviewers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_manager': {
                u'financialmanagers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'financial_advice_signed': {
                u'financialmanagers': {'roles': [u'Reviewer'], 'rel': ''}},
        }
    }
    msg = add_fti_configuration(portal_type='meetingadvicefinancesnocec',
                                configuration=roles_config['advice_group'],
                                keyname='advice_group',
                                force=True)

    if msg:
        logger.warn(msg)


def finalizePROVHainautInstance(context):
    """ """
    site = context.getSite()
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
                 proposing_groups=['dirgen', 'secretariat'],
                 # need 4
                 categories=[u'assurances', u'autorites-provinciales', u'contentieux', u'intercommunales'],
                 # need 4
                 associated_groups=['ag1', 'ag2', 'ag3', 'ag4', 'ag5'],
                 # need 5
                 groupsInCharge=['dp-eric-massin', 'dp-fabienne-capot',
                                 'dp-fabienne-devilers', 'dp-pascal-lafosse', 'dp-serge-hustache'],
                 userId='dgen'
                 ):
    """ """
    items = (
        {'title': u'Exemple point 1',
         'proposingGroup': proposing_groups[0],
         'category': categories[0],
         'associatedGroups': [associated_groups[0]],
         'groupsInCharge': [groupsInCharge[0]],
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
    if not mTool.getMemberareaCreationFlag():
        mTool.setMemberareaCreationFlag()
    mTool.createMemberArea(userId)
    # in tests, the MeetingConfig id is generated
    cfg1 = tool.objectValues('MeetingConfig')[0]
    cfg1_id = cfg1.getId()
    userFolder = tool.getPloneMeetingFolder(cfg1_id, userId)
    date = DateTime() - 1
    with api.env.adopt_user(userId):
        meeting = api.content.create(container=userFolder,
                                     type='MeetingZCollege',
                                     id=date.strftime('%Y%m%d'),
                                     date=date)
        meeting.processForm()
        i = 1
        cfg = tool.getMeetingConfig(meeting)
        site.REQUEST['PUBLISHED'] = meeting
        for item in items:
            newItem = api.content.create(container=userFolder,
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

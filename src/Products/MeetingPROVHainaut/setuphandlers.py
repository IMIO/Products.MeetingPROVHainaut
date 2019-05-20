# -*- coding: utf-8 -*-

from Products.MeetingCommunes.setuphandlers import _installPloneMeeting
from Products.MeetingCommunes.setuphandlers import _showHomeTab
from Products.MeetingCommunes.setuphandlers import logStep
from Products.MeetingPROVHainaut.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.setuphandlers import addOrUpdateIndexes


def isMeetingPROVHainautProfile(context):
    return context.readDataFile("MeetingPROVHainaut_marker.txt") or \
        context.readDataFile("MeetingPROVHainaut_zprovhainaut_marker.txt") or \
        context.readDataFile("MeetingPROVHainaut_testing_marker.txt")


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if not isMeetingPROVHainautProfile(context):
        return

    logStep("postInstall", context)
    site = context.getSite()
    # Create or update indexes
    addOrUpdateIndexes(site, {'groupedItemsNum': ('FieldIndex', {})})
    # need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context, site)
    _showHomeTab(context, site)
    _reorderSkinsLayers(context, site)
    # Create or update indexes
    addOrUpdateIndexes(site, {'groupedItemsNum': ('FieldIndex', {})})


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingPROVHainautProfile(context):
        return

    site = context.getSite()
    logStep("initializeTool", context)
    _installPloneMeeting(context, site)
    return ToolInitializer(context, PROJECTNAME).run()


def _reorderSkinsLayers(context, site):
    """
       Re-apply MeetingPROVHainaut skins.xml step
       as the reinstallation of MeetingPROVHainaut and PloneMeeting changes the portal_skins layers order
    """
    logStep("reorderSkinsLayers", context)
    try:
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingPROVHainaut:default', 'skins')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the plonemeetingskin or imioapps profile is not available
        # (not using plonemeetingskin, imioapps or in testing?) we pass...
        pass


def finalizeInstance(context):
    """
      Called at the very end of the installation process (after PloneMeeting).
    """
    if not isMeetingPROVHainautProfile(context):
        return

    _reorderSkinsLayers(context, context.getSite())
    _reorderCss(context)


def _reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
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

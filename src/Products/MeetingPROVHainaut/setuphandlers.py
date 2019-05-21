# -*- coding: utf-8 -*-

from Products.MeetingCommunes.setuphandlers import _showHomeTab
from Products.MeetingCommunes.setuphandlers import logStep
from Products.MeetingPROVHainaut.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer


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
    _showHomeTab(context, site)
    _reorderSkinsLayers(context, site)


def initializeTool(context):
    """Initialises the PloneMeeting tool based on information from the current profile."""
    if not isMeetingPROVHainautProfile(context):
        return

    logStep("initializeTool", context)
    return ToolInitializer(context, PROJECTNAME).run()


def _reorderSkinsLayers(context, site):
    """Re-apply MeetingPROVHainaut skins.xml step to be sure the order is correct."""
    logStep("reorderSkinsLayers", context)
    try:
        site.portal_setup.runImportStepFromProfile(u'profile-Products.PloneMeeting:default', 'skins')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingPROVHainaut:default', 'skins')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the plonemeetingskin or imioapps profile is not available
        # (not using plonemeetingskin, imioapps or in testing?) we pass...
        pass


def finalizeInstance(context):
    """Called at the very end of the installation process (after PloneMeeting)."""
    if not isMeetingPROVHainautProfile(context):
        return

    _reorderSkinsLayers(context, context.getSite())
    _reorderCss(context)


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

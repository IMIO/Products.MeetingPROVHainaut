# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2015 by IMIO
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingCPASLalouviere: setuphandlers')
from Products.MeetingCPASLalouviere.config import PROJECTNAME
import os
from Products.CMFCore.utils import getToolByName
##code-section HEAD
from Products.PloneMeeting.exportimport.content import ToolInitializer
##/code-section HEAD


def isNotMeetingCPASLalouviereProfile(context):
    return context.readDataFile("MeetingCPASLalouviere_marker.txt") is None


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingCPASLalouviereProfile(context):
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingCPASLalouviereProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    #need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reorderSkinsLayers(context, site)


##code-section FOOT

def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCPASllConfigureProfile(context):
    return context.readDataFile("MeetingCPASll_examples_fr_marker.txt") or \
           context.readDataFile("MeetingCPASLL_tests_marker.txt")


def installMeetingCPASLalouviere(context):
    """ Run the default profile before bing able to run the CPAS lalouviere profile"""
    import ipdb; ipdb.set_trace()
    if not isMeetingCPASllConfigureProfile(context):
        return

    logStep("installMeetingCPASLalouviere", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingCPASLalouviere:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingCPASllConfigureProfile(context):
        return

    logStep("initializeTool", context)
    #PloneMeeting is no more a dependency to avoid
    #magic between quickinstaller and portal_setup
    #so install it manually
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingCPASLalouviereProfile(context):
        return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingCPASLalouviereProfile(context):
        return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reorderSkinsLayers(context, site):
    """
       Re-apply MeetingCPASLalouviere skins.xml step
       as the reinstallation of MeetingCPASLalouviere and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingCPASLalouviereProfile(context) and not isMeetingCPASllConfigureProfile(context):
        return

    logStep("reorderSkinsLayers", context)
    try:
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCPASLalouviere:default', 'skins')
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
    reorderSkinsLayers(context, context.getSite())
    reorderCss(context)


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingCPASLalouviereProfile(context) and not isMeetingCPASllConfigureProfile(context):
        return

    site = context.getSite()

    logStep("reorderCss", context)
    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'meetingCPASlalouviere.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)

##/code-section FOOT

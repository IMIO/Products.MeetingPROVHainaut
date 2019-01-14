# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingCPASLalouviere


MLL_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                           package=Products.MeetingCPASLalouviere,
                           name='MLL_ZCML')

MLL_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MLL_ZCML),
                               name='MLL_Z2')

MLL_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCPASLalouviere,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingCPASLalouviere',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingCPASLalouviere:testing',
    name="MLL_TESTING_PROFILE")

MLL_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MLL_TESTING_PROFILE,), name="MLL_TESTING_PROFILE_FUNCTIONAL")

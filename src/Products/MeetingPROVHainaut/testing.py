# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.testing import z2
from plone.testing import zca
from Products.MeetingCommunes.testing import MCLayer

import Products.MeetingPROVHainaut


MPH_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                           package=Products.MeetingPROVHainaut,
                           name='MPH_ZCML')

MPH_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MPH_ZCML),
                               name='MPH_Z2')

MPH_TESTING_PROFILE = MCLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingPROVHainaut,
    additional_z2_products=('imio.dashboard',
                            'Products.PloneMeeting',
                            'Products.MeetingCommunes',
                            'Products.MeetingPROVHainaut',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingPROVHainaut:testing',
    name="MPH_TESTING_PROFILE")

MPH_FIN_TESTING_PROFILE = MCLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingPROVHainaut,
    additional_z2_products=('imio.dashboard',
                            'Products.PloneMeeting',
                            'Products.MeetingCommunes',
                            'Products.MeetingPROVHainaut',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingPROVHainaut:zprovhainaut',
    name="MPH_FIN_TESTING_PROFILE")


MPH_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MPH_TESTING_PROFILE,), name="MPH_TESTING_PROFILE_FUNCTIONAL")

MPH_FIN_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MPH_FIN_TESTING_PROFILE,), name="MPH_FIN_TESTING_PROFILE_FUNCTIONAL")

# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingPROVHainaut


ML_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                           package=Products.MeetingPROVHainaut,
                           name='ML_ZCML')

ML_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, ML_ZCML),
                               name='ML_Z2')

ML_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingPROVHainaut,
    additional_z2_products=('imio.dashboard',
                            'Products.PloneMeeting',
                            'Products.MeetingCommunes',
                            'Products.MeetingPROVHainaut',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingPROVHainaut:testing',
    name="ML_TESTING_PROFILE")

ML_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(ML_TESTING_PROFILE,), name="ML_TESTING_PROFILE_FUNCTIONAL")

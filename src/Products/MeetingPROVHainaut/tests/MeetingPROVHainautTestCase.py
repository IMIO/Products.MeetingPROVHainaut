# -*- coding: utf-8 -*-

from Products.MeetingPROVHainaut.testing import MPH_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingPROVHainaut.tests.helpers import MeetingPROVHainautTestingHelpers
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class MeetingPROVHainautTestCase(MeetingCommunesTestCase, MeetingPROVHainautTestingHelpers):
    """Base class for defining MeetingPROVHainaut test cases."""

    layer = MPH_TESTING_PROFILE_FUNCTIONAL

    cfg1_id = 'meeting-config-zcollege'
    cfg2_id = 'meeting-config-zcouncil'

# -*- coding: utf-8 -*-
#
# File: MeetingCPASLiege.py
#
# Copyright (c) 2018 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from collections import OrderedDict


PROJECTNAME = "MeetingCPASLiege"

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# see doc in Products.PloneMeeting.config.py

STYLESHEETS = [{'id': 'meetingcpasliege.css',
                'title': "MeetingCPASLiege CSS styles"}]
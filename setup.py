# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = '4.2.0'

setup(name='Products.MeetingPROVHainaut',
      version=version,
      description="PloneMeeting profile for Province de Hainaut",
      long_description=open("README.rst").read() + "\n\n" + open("CHANGES.rst").read(),
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: Customer Service",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Other Scripting Engines",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP :: Site Management",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Office/Business",
      ],
      keywords='plone official meetings management egov communesplone imio plonegov hainaut',
      author='Gauthier Bastien',
      author_email='gauthier@imio.be',
      url='https://www.imio.be/nos-applications/ia-delib',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=['Products.PloneMeeting[test]']),
      install_requires=[
          'Products.MeetingCommunes'],
      entry_points={},
      )

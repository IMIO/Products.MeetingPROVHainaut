from setuptools import setup, find_packages
import os

version = '4.0-dev'

setup(name='Products.MeetingPROVHainaut',
      version=version,
      description="PloneMeeting profile for province of Hainaut",
      long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://www.imio.be/produits/gestion-des-deliberations',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
            test=['unittest2',
                  'zope.testing',
                  'plone.testing',
                  'plone.app.testing',
                  'plone.app.robotframework',
                  'Products.CMFPlacefulWorkflow',
                  'zope.testing',
                  'Products.PloneTestCase'],
              templates=['Genshi',
                         ]),
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'Pillow',
          'Products.PloneMeeting',
          'Products.MeetingCommunes'],
      entry_points={},
      )

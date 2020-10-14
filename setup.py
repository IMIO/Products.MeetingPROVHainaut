# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '4.2b3'

setup(name='Products.MeetingPROVHainaut',
      version=version,
      description="PloneMeeting profile for Province de Hainaut",
      long_description=open("README.rst").read() + "\n\n" + open("CHANGES.rst").read(),
      classifiers=["Programming Language :: Python"],
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
          test=['Products.PloneMeeting[test]']),
      install_requires=[
          'Products.MeetingCommunes'],
      entry_points={},
      )

from setuptools import setup, find_packages
import os

version = '0.1.dev0'

setup(name='adi.forumail',
      version=version,
      description="Webforum- and mailinglist-hybrid for Plone",
      long_description="",
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ida Ebkes',
      author_email='contact@ida-ebkes.eu',
      url='https://github.com/ida/adi.forumail',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'mailtoplone.base',
          'collective.contentrules.mailtogroup',
          'plone.api',
          'setuptools',
          'Products.ContentWellPortlets',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

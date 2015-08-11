import platform
import os
from Products.Five.utilities.marker import mark
from mailtoplone.base.interfaces import IBlogMailDropBoxMarker 
from plone import api
from plone.app.contentrules.api import assign_rule

def isInitialInstall(site, app_name):
    INI_INSTALL = False
    addons = site.portal_quickinstaller.listInstallableProducts(skipInstalled=False)
    for addon in addons:
        if (addon['id'] == app_name) and (addon['status'] == 'new'):
            INI_INSTALL = True
    return INI_INSTALL

def doOnInstall(site, app_name):

    site_domain = platform.uname()[1]

    if site_domain == 'localhost.localdomain':
        site_domain = 'example.org'

    forum_id = app_name.split('.')[1]
    forum_name = forum_id.title()

    user_id = 'forumailer'
    user_name = 'Forum Mailer'
    user_mail = user_id + '@' + site_domain

    group_id = 'Forumailers'
    group_name = group_id

    # Create forum:    
    forum = api.content.create(type='Folder', title=forum_name, container=site)
    # Assign interface for mail-dropping via mailtoplone.base:
    mark(forum, IBlogMailDropBoxMarker)

    # Set forum's view:
    forum.setLayout('folder_full_view')

    # Create group:
    api.group.create(groupname=group_id, title=group_name)
    
    # Assign group-permissions to forum:
    forum.manage_setLocalRoles(group_id, ['Contributor', 'Reader'])
    # Update perm-change in portal_catalog:
    forum.reindexObject()
    forum.reindexObjectSecurity()

    # Import contentrule of profile 'forumail':
    site.portal_setup.runAllImportStepsFromProfile('profile-' + app_name + ':' + app_name.split('.')[1], ignore_dependencies=True)
    # Assign contentrule to forum:
    assign_rule(forum, forum_id)

    # Add a collection, which sorts id alphabetically (1, 1-1, 1-2, 2, 2-1, 2-2, ...):
    collection = api.content.create(type='Topic', title='Threaded', container=forum)
    contenttype_criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    contenttype_criterion.setValue('News Item')
    collection.setSortCriterion('id', reversed=False)
    
    # Add user, we need at least one, so collective.contentrule.mailtogroup  will not complain:
#DEV    api.user.create(username=user_id, password=user_id, email=user_mail, properties=dict(fullname=user_name))
    # Assign user to group:
#    api.group.add_user(groupname=group_id, username=user_id)

    # Create forum-post, should trigger an email-noti:
#DEV    post = api.content.create(type='News Item', title='Welcome to the Forum of "%s"'%site.Title(), text='Express yourself, don\'t repress yourself!', container=forum)

def doOnReinstall(site):

    pass

def setupVarious(context):
    app_name = 'adi.forumail'
    site = api.portal.get()

    # Make sure, profile has been imported, otherwise will be executed also, when barely running buildout:
    if context.readDataFile(app_name + '.marker.txt') is None:
        return

    if isInitialInstall(site, app_name):
        doOnInstall(site, app_name)
    else:
        doOnReinstall(site)


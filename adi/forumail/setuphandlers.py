import os
from Products.Five.utilities.marker import mark
from mailtoplone.base.interfaces import IBlogMailDropBoxMarker 
from plone import api
from plone.app.contentrules.api import assign_rule
import platform

def isInitialInstall(site, app_name):
    INI_INSTALL = False
    addons = site.portal_quickinstaller.listInstallableProducts(skipInstalled=False)
    for addon in addons:
        if (addon['id'] == app_name) and (addon['status'] == 'new'):
            INI_INSTALL = True
    return INI_INSTALL

def doOnInstall(site, app_name):

    site_domain = platform.uname()[1]

    forum_id = app_name.split('.')[1]
    forum_name = forum_id.title()

    user_id = forum_id + 'er'
    user_name = user_id.title()
    user_mail = user_id + '@' + site_domain

    group_id = forum_id + 'ers'
    group_name = group_id.title()

    # Create forum:    
    forum = api.content.create(type='Folder', title=forum_name, container=site)
    # Set forum's view:
    forum.setLayout('folder_full_view')
    # Assign interface for mail-dropping:
    mark(forum, IBlogMailDropBoxMarker)

    # Create group:
    api.group.create(groupname=group_id, title=group_name)
    
    # Assign group-perms to forum:
    forum.manage_setLocalRoles(group_id, ['Contributor', 'Reader'])
    # Update perm-change:
    forum.reindexObjectSecurity()

    # Import contentrule of profile 'forumail':
    site.portal_setup.runAllImportStepsFromProfile('profile-' + app_name + ':' + app_name.split('.')[1], ignore_dependencies=True)
    # Assign contentrule to forum:
    assign_rule(forum, forum_id)

    # Add user:
    api.user.create(username=user_id, password=user_id, email=user_mail, properties=dict(fullname=user_name))

    # Assign user to group:
    api.group.add_user(groupname=group_id, username=user_id)

    # Create forum-post:
    post = api.content.create(type='News Item', title='Welcome to the Forum of "%s"'%site.Title(), text='Express yourself, don\'t repress yourself!', container=forum)
    
    # Update content-change:
    post.reindexObject()

def setupVarious(context):
    app_name = 'adi.forumail'
    site = api.portal.get()

    # Make sure, profile has been imported, otherwise will be executed also, when barely running buildout:
    if context.readDataFile(app_name + '.marker.txt') is None:
        return

    if isInitialInstall(site, app_name):
        doOnInstall(site, app_name)


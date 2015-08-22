import platform
import os
from Products.Five.utilities.marker import mark
from mailtoplone.base.interfaces import IBlogMailDropBoxMarker 
from plone import api
from plone.app.contentrules.api import assign_rule

def isInitialInstall(site, addon_name):
    INI_INSTALL = False
    addons = site.portal_quickinstaller.listInstallableProducts(skipInstalled=False)
    for addon in addons:
        if (addon['id'] == addon_name) and (addon['status'] == 'new'):
            INI_INSTALL = True
    return INI_INSTALL

def doOnInstall(site, addon_name):

    site_domain = platform.uname()[1]

    forum_id = 'forumail'
    forum_name = 'Forumail'

    user_id = 'forumailer'
    user_name = 'Foru Mailer'

    group_id = 'Forumailers'
    group_name = 'Forumailers'

    # Create forum:    
    forum = api.content.create(type='Folder', title=forum_name, container=site)
    # Assign interface for mail-dropping via mailtoplone.base:
    mark(forum, IBlogMailDropBoxMarker)
    # Set default-view of forum:
    forum.setLayout('forumail_view')
    # Create group:
    api.group.create(groupname=group_id, title=group_name)
    # Assign group-permissions to forum:
    forum.manage_setLocalRoles(group_id, ['Contributor', 'Reader'])
    # Update content- and permission-change in portal_catalog:
    forum.reindexObject()
    forum.reindexObjectSecurity()

 
    # Import contentrule of profile 'forumail' 
    # (! If this is done before content-creation and no user is assigned to group,
    # contentrule will righteously complain, that there's nobody to send the mail to.)
    # and complain, no recipients are designated:
    site.portal_setup.runAllImportStepsFromProfile('profile-' + addon_name + ':' + addon_name.split('.')[1], ignore_dependencies=True)
    # Assign contentrule to forum:
    assign_rule(forum, forum_id)

    if site_domain != 'localhost.localdomain':
        
        user_mail = user_id + '@' + site_domain

        # Add user, we need at least one, so collective.contentrule.mailtogroup  will not complain:
        api.user.create(username=user_id, password=user_id, email=user_mail, properties=dict(fullname=user_name))
        # Assign user to group:
        api.group.add_user(groupname=group_id, username=user_id)
        # Create forum-post, should trigger an email-noti:
        post = api.content.create(type='News Item', title='Welcome to the Forum of "%s"'%site.Title(), text='Express yourself, don\'t repress yourself!', container=forum)
    

def doOnReinstall(site):
    pass

def setupVarious(context):
    addon_name = 'adi.forumail'
    site = api.portal.get()

    # Make sure, profile has been imported, otherwise will be executed also, when barely running buildout:
    if context.readDataFile(addon_name + '.marker.txt') is None:
        return

    if isInitialInstall(site, addon_name):
        doOnInstall(site, addon_name)
    else:
        doOnReinstall(site)


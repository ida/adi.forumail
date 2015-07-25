from Products.Five.utilities.marker import mark
from mailtoplone.base.interfaces import IBlogMailDropBoxMarker 
from plone import api
from plone.app.contentrules.api import assign_rule

def doOnInstall(portal):

    app_name = 'adi.forumail' #__file__.split('/')[-3] # grandpa'-dir's name, should be egg's name, if two-dotted-namespace, here should be: 'adi.forummail'

    INI_INSTALL = False
    qi = portal.portal_quickinstaller
    addons = qi.listInstallableProducts(skipInstalled=False)

    for addon in addons:
        if (addon['id'] == app_name) and (addon['status'] == 'new'):
            INI_INSTALL = True

    if INI_INSTALL:
        forum_name = app_name.split('.')[-1]
        forum_title = forum_name.title()
        mail_from = portal.getProperty('email_from_address')
        mail_domain = mail_from.split('@')[1]
        setup_tool = portal.portal_setup
        user_name = forum_name + 'er'
        user_mail = user_name + '@' + mail_domain
        group_name = user_name + 's'
        group_mail = group_name + '@' + mail_domain
        mail_to = group_mail

        # Create forum-container:
        folder = api.content.create(type='Folder', title=forum_title, container=portal)
        # Set 'all_content' as default-view of container:
        folder.setLayout('folder_full_view')
        # Assign mailtoplone.base-interface to it:
        mark(folder, IBlogMailDropBoxMarker)
        # Create a group:
        api.group.create(groupname=group_name, title=group_name.title())
        # Set permissions for group on container:
        folder.manage_setLocalRoles(group_name, ['Contributor', 'Reader'])
        # After modifications, pdate changes in DB-index-cache, a.k.a portal_catalogue:
        folder.reindexObject()
        folder.reindexObjectSecurity()
        # Now, we have the group and container, load contentrules.xml of profile 'forumname',
        # to make our rule available and selectable in the Plone-site:
        setup_tool.runAllImportStepsFromProfile('profile-' + app_name + ':' + forum_name, ignore_dependencies=True)
        # Then, assign contentrule to container. Note: rule- and profile-name must equal forum_name!
        assign_rule(folder, forum_name)

        # Add a group-member (do this before creating first welcome-post, to check, if notimail works):
        api.user.create(username=user_name, password=user_name, email=user_mail, properties=dict(fullname=user_name))
        api.group.add_user(groupname=group_name, username=user_name)

        # Create a first welcome-post:
        post = api.content.create(type='News Item', title='Welcome to the Forum of "%s"!'%portal.Title(), text='Express yourself, don\'t repress yourself.', container=folder)
        post.reindexObject()

def setupVarious(context):
    portal = context.getSite()
    # Make sure, profile has been imported, otherwise will be executed also, when barely running buildout:
    if context.readDataFile('adi.forumail.marker.txt') is None:
        return
    doOnInstall(portal)

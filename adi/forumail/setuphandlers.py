from Products.CMFCore.utils import getToolByName
from Products.Five.utilities.marker import mark
from mailtoplone.base.interfaces import IBlogMailDropBoxMarker 
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.app.contentrules.rule import Rule
from plone.app.contentrules.api import assign_rule
from zope.component import getMultiAdapter

def doOnInstall(context):

    qi = getToolByName(context, 'portal_quickinstaller')
    prods = qi.listInstallableProducts(skipInstalled=False)
    for prod in prods: # Do this only on an initial install, not on re-installs:
        if (prod['id'] == 'adi.forumail') and (prod['status'] == 'uninstalled'):

            urltool = getToolByName(context, 'portal_url')
            portal = urltool.getPortalObject()
            typestool = getToolByName(context, 'portal_types')

            # Create dropbox:
            dropbox = typestool.constructContent(type_name="Folder", container=portal, id='dropbox', Title='Dropbox')
            # Assign interface:
            mark(portal.dropbox, IBlogMailDropBoxMarker)

            # Assign contentrule:
            assign_rule(portal.dropbox, 'rule-1')

            # Update dropbox in catalogue after changes:
            portal.dropbox.reindexObject()
                    

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.forumail.marker.txt') is None:
        return

    doOnInstall(portal)

from Acquisition import aq_inner, aq_parent

from mailtoplone.base.interfaces import IBlogMailDropBoxMarker

def setView(context, event):
    parent = aq_parent(context)
    if IBlogMailDropBoxMarker.providedBy(parent):
        context.setLayout('forumail_view')
        context.reindexObject()


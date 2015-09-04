# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    def getPostPortalType(self):
        return 'News Item'

    def getResultsTypes(self):
        return ['posts', 'threads']

    index = ViewPageTemplateFile("forum_main.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    forum_body = ViewPageTemplateFile("forum_body.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def renderForumHead(self):
        return self.forum_head()

    def renderForumBody(self):
        return self.forum_body()

    def getForumUrl(self):
        forum_url = self.request["ACTUAL_URL"]
        context = aq_inner(self.context)
        if context.Type() == self.getPostPortalType():
            forum_url = '/'.join(forum_url.split('/')[:-1])
        return forum_url

    def getForumPath(self):
        context = aq_inner(self.context)
        forum_path = self.request["ACTUAL_URL"]
        if context.Type() == self.getPostPortalType():
            forum_path = '/'.join(forum_path.split('/')[:-1])
        return forum_path

    def getAddUrl(self):
        add_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            add_url = forum_url + '/createObject?type_name=' + self.getPostPortalType()
        return add_url

    def getUrlParas(self):
        pairs = self.request.form.keys()
        return pairs

    def getUrlParaVal(self, para):
        val = self.request.form[para]
        return val

    def getResultsType(self, url_para='results_type'):
        para = 'results_type'
        results_type = self.getResultsTypes()[0] # default
        paras = self.getUrlParas()
        if para in paras:
            results_type = self.getUrlParaVal(para)
        return results_type

    def getPostsResults(self):
        """ Main function to return list of posts to view, depending on user's selection via URL-para."""
        results = None
        results_types = self.getResultsTypes()
        results_type = self.getResultsType()
        if results_type in results_types:
            if results_type == 'threads':
                results = self.getThreads()
            elif results_type == 'posts':
                results = self.getPosts()
        else:
            raise Exception, 'Resultss-type "' + results_type + '" is not available, choose of:: %s'%results_types
        return results

    def getPosts(self, sort_order='reverse', sort_on='created'):
        """
        Expects forum-container-folder or one of its first-children(=post).
        Returns all posts of forum, as a catalog-brain-dict, not as objects.
        """
        context = aq_inner(self.context)
        if context.Type() == self.getPostPortalType():
            context = aq_parent(context)
        elif context.Type() != 'Folder':
            raise Exception, context.Type() + " is not considered to be a forum's child, yet."
        posts = api.content.find(context=context,
                                 portal_type=self.getPostPortalType(),
                                 sort_on=sort_on,
                                 sort_order=sort_order)
        return posts

    def getThreads(self):
        context = aq_inner(self.context)
        posts = api.content.find(context=context,
                                 portal_type=self.getPostPortalType())
        posts = sorted(posts, key=lambda post: (post.created, post.id))
        return posts

    def getThreadId(self, post_id):
        thread_id = None
        nrs = ['0','1','2','3','4','5','6','7','8','9']
        i = len(post_id)-1
        if post_id[-1] in nrs:
            while i > 0 and post_id[i] in nrs or post_id[i] == '-':
                i -= 1
                if post_id[i] == '-' and not post_id[i-1] in nrs:
                    break
            thread_id = post_id[:i]
        else:
            thread_id = post_id
        return thread_id

    def isReply(self, post_id, thread_id):
        IS_REPLY = False
        nrs = ['1','2','3','4','5','6','7','8','9','0']
        if len(post_id) >= len(thread_id) + 1 \
        and post_id.startswith(thread_id + '-')\
        and post_id[len(thread_id) + 1] in nrs:
            IS_REPLY =  True
        return IS_REPLY

    def isIniPost(self, post_id):
        IS_INI_POST = False
        thread_id = self.getThreadId(post_id)
        IS_REPLY = self.isReply(post_id, thread_id)
        if not IS_REPLY: IS_INI_POST = True
        return IS_INI_POST

#EOF

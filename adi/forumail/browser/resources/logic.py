# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("thread.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def getThreadId(self, post_id):
        thread_id = ''
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

    def getForumPosts(self):
        """Returns brain."""
        post = aq_inner(self.context)
        forum = aq_parent(post)
        forum_posts = api.content.find(context=forum, portal_type='News Item', sort_on='id')
        return forum_posts

    def getThreadPosts(self, thread_id):
        """Returns objects."""
        thread_posts = []
        posts = self.getForumPosts()
        for post in posts:
            post_id = post.getObject().getId()
            if post_id.startswith(thread_id):
                thread_posts.append(post.getObject())
        return thread_posts

    def getThread(self):
        thread = []
        post = aq_inner(self.context)
        post_id = post.getId()
        thread_id = self.getThreadId(post_id)
        posts = self.getThreadPosts(thread_id)
        return posts


    def getAvatarUrl(self, user_id):
        member_tool = api.portal.get_tool('portal_membership')
        portrait = member_tool.getPersonalPortrait(user_id)
        portrait_url = portrait.absolute_url()
        if portrait_url.endswith('/defaultUser.png'):
            portrait_url = '/'.join(portrait_url.split('/')[:-1]) + '/logo.png'
        return portrait_url


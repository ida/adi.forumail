# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("posts.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def isNr(string):
        IS_NR = False
        nrs = ['0','1','2','3','4','5','6','7','8','9']
        i = len(string)-1
        while i < len(nrs)-1 and string[i] in nrs:
            i -= 1
        if i == 0: IS_NR = True
        return IS_NR


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

    def getPosts(self):
        """
        Expects forum-(Folder)- or post-(News Item)-object,
        returns post-objects.
        If self is a forum, returns all posts in forum,
        if self is a post, returns all posts of thread.
        """
        posts = []
        thread_id = None
        context = aq_inner(self.context)
        if context.Type() == 'News Item':
            post_id = context.getId()
            thread_id = self.getThreadId(post_id)
            context = aq_parent(context)
        posts_brain = api.content.find(context=context, portal_type='News Item', sort_on='created')
        for post in posts_brain:
            post = post.getObject()
            post_id = post.getId()
            if thread_id:
                if post.getId().startswith(thread_id):
                    posts.append(post)
            else:
                    posts.append(post)
        return posts

    def getPostIds(self):
        post_ids = []
        posts = self.getPosts()
        for post in posts:
            post_ids.append(post.getId())
        return post_ids

    def getNextId(self, post_id):
        """ Expects a post-obj and post-id, returns next reply-to-id."""
        next_id = ''
        next_nr = 0
        post_ids = self.getPostIds()
        if post_id != self.getThreadId(post_id):
            next_nr = int(post_id.split('-')[-1]) + 1
            next_id = '-'.join(post_id.split('-')[:-1]) + '-' + str(next_nr)
        else:
            next_id = post_id + '-1'
        # If id exists, increase:
        while next_id in post_ids:
            next_nr = next_nr + 1
            next_id = '-'.join(post_id.split('-')[:-1]) + '-' + str(next_nr)

        return next_id


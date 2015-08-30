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

    def getPosts(self):
        """
        Expects forum-(Folder)- or post-(News Item)-object,
        returns post-objects.
        If self is a forum, returns all posts in forum,
        if self is a post, returns all posts of thread.
        """
        sort_order = 'reverse'
        posts = []

        thread_id = None
        context = aq_inner(self.context)
        if context.Type() == 'News Item':
            post_id = context.getId()
            thread_id = self.getThreadId(post_id)
            context = aq_parent(context)
            sort_order = 'ascending'
        posts_brain = api.content.find(context=context, portal_type='News Item', sort_on='created', sort_order=sort_order)
        for post in posts_brain:
            post = post.getObject()
            post_id = post.getId()
            if thread_id:
                if post.getId().startswith(thread_id):
                    posts.append(post)
            else:
                    posts.append(post)
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

    def getPostsIds(self):
        post_ids = []
        posts = self.getPosts()
        for post in posts:
            post_id = post['id']
            post_ids.append(post_id)
        return post_ids

    def getThreadsIds(self):
        threads_ids = []
        posts_ids = self.getPostsIds()
        for post_id in posts_ids:
            thread_id = self.getThreadId(post_id)
            if thread_id not in threads_ids:
                threads_ids.append(thread_id)
        return threads_ids

    def isReply(self, post_id, thread_id):
        IS_REPLY = False
        nrs = ['1','2','3','4','5','6','7','8','9','0']
        if len(post_id) >= len(thread_id) + 1 \
        and post_id.startswith(thread_id + '-')\
        and post_id[len(thread_id) + 1] in nrs:
            IS_REPLY =  True
        return IS_REPLY 

    def getThreads(self):
        """
        Sorted by newest ini-post.
        """
        threads = []
        thread = None
        threads_ids = self.getThreadsIds()
        posts = self.getPosts()

        for thread_id in threads_ids:
            
            i = -1
            while i < len(posts)-1:
                i += 1
            
                post = posts[i]
                post_id = post['id']
                
                if post_id == thread_id:
                    threads.append(posts.pop(i))
            
                    i = -1
                    while i < len(posts)-1:
                        i += 1
            
                        post = posts[i]
                        post_id = post['id']
            
                        if post_id.startswith(thread_id):
                            threads.append(posts.pop(i))
        return threads


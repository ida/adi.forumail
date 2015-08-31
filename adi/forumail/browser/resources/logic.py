# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("forum.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    posts_template = ViewPageTemplateFile("posts.pt")

    def getPortalType(self):
        return 'News Item'

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def renderForumHead(self):
        return self.forum_head()

    def renderPosts(self):
        return self.posts_template()

    def getForumUrl(self):
        forum_url = self.request["ACTUAL_URL"]
        context = aq_inner(self.context)
        if context.Type() == self.getPortalType():
            forum_url = '/'.join(forum_url.split('/')[:-1])
        return forum_url

    def getForumPath(self):
        forum_path = self.request["ACTUAL_URL"]
        context = aq_inner(self.context)
        if context.Type() == self.getPortalType():
            forum_path = '/'.join(forum_path.split('/')[:-1])
        return forum_path

    def getAddUrl(self):
        add_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            add_url = forum_url + '/createObject?type_name=' + self.getPortalType()
        return add_url

    def getUrlParas(self):
        pairs = self.request.form.keys()
        return pairs

    def getUrlParaVal(self, para):
        val = self.request.form[para]
        return val

    def getResultsType(self):
        para = 'results_type'
        results_type = 'singles' # default
        paras = self.getUrlParas()
        if para in paras:
            results_type = self.getUrlParaVal(para)
        return results_type

    def getPostsResult(self):
        """ Main function to return list of posts to view."""
        results = None
        results_type = self.getResultsType()
        if results_type == 'singles':
            results = self.getPosts()
        elif results_type == 'threaded':
            results = self.getThreads()
        else:
            raise Exception, 'Results-type "' + results_type + '" is not available'
        return results

    def getPosts(self, sort_order='reverse', sort_on='created'):
        """
        Expects forum-(Folder)- or post-(News Item)-object,
        returns post-objects.
        If self is a forum, returns all posts in forum,
        if self is a post, returns all posts of thread.
        """
        posts = []
        context = aq_inner(self.context)
        if context.Type() == self.getPortalType():
            context = aq_parent(context)
        posts = api.content.find(context=context, portal_type=self.getPortalType(), sort_on=sort_on, sort_order=sort_order)
        posts_tuple = ()
        for post in posts:
            post_tuple = (post['id'], )
        return posts

    def getPostsIds(self):
        post_ids = []
        posts = self.getPosts()
        for post in posts:
            post_id = post['id']
            post_ids.append(post_id)
        return post_ids

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

    def getThreadsIds(self):
        threads_ids = []
        posts_ids = self.getPostsIds()
        for post_id in posts_ids:
            thread_id = self.getThreadId(post_id)
            if thread_id not in threads_ids:
                threads_ids.append(thread_id)
        return threads_ids

    def getThreads(self):
        """
        Sorted by newest ini-post.
        """
        threads_flat = []   # endresult
        threads_nested = [] # [ [threadposts], ]
        thread = None
        thread_ids = []
        threads_ids = self.getThreadsIds()
        posts = self.getPosts()

        for thread_id in threads_ids:
            
            i = -1
            while i < len(posts)-1:
                i += 1
            
                post = posts[i]
                post_id = post['id']
                

                if post_id == thread_id: # found threadstarter
                    thread = [posts[i]]

            
                    i = -1 # start searching from begin of list for replies
                    while i < len(posts)-1:
                        i += 1
            
                        post = posts[i]
                        post_id = post['id']
                        # TODO: make this sharper (endswith numbers sep by minus...):
                        if post_id.startswith(thread_id) and post_id != thread_id:
                            thread.append(posts[i]) # found reply
#                    print ', '.join([str(post['id']) for post in thread])
                    threads_nested.append(thread)
        # Sort a thread alphabetically by id: 
        for thread in threads_nested:
            thread_new = self.sortById(thread)
            for post in thread_new:
                threads_flat.append(post)
        return threads_flat

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

    def sortById(self, posts):
        new_posts = []
        posts_ids = [] #self.getPostsIds()
        for post in posts:
            posts_ids.append(post['id'])
        posts_ids.sort()
        for post_id in posts_ids:
            for i, post in enumerate(posts):
                if post['id'] == post_id:
                    new_posts.append(post)
        return new_posts

#EOF

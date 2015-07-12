Introduction
============

An experimental proof of concept for a mailinglist/forum-hybrid, realized with Plone.

For development-purposes only:

- Mail-account-password will be stored in plaintext two times. Changeable with:

    $ crontab -e

    $ vim ~/forumail/dev-addons/adi.forumail/adi/forumail/profiles/default/mailhost.xml


- Mail-inbox needs a filter, to check, whether a sender is a permitted forum's participant.


Requirements
=============

- Operating system is unixish.

- Min. sys-pckgs Plone needs, preinstalled. And git.

- You have at least two mail-accounts with the following usernames at the same domain:

    - 'forumail' -> 'From:'-address for mail-notificas, forum's inbox.

    - 'forumailers' -> 'To:'-address for mail-notificas, gets what groupmembers get.
                        Must differ to 'From:'-address, to not create an infinite loop.

- Optionally also:

    - 'forumailer' -> Example-user, belonging to the group 'forumailers'.
                      Should become a notification-mail with the initially
                      created welcome-post after install, if everything went well.


Dependencies
============

Development-versions of mailtoplone.base and collective.contentrules.mailtogroup,
will be installed of script automatically.



Installation
============

The installer-script creates a folder in your $HOME called 'forumail' and
installs Plone and this addon in it.


Download the installer script
-----------------------------

    $ wget https://raw.githubusercontent.com/ida/adi.forumail/master/buildout_forumail.sh



Set credentials in it
---------------------

Open the script with a text-editor and enter the needed mailaccount-credentials.



Make it executable
------------------

    $ chmod +x buildout_forumail.sh


Execute it
----------

    $ ./buildout_forumail.sh


After a while you should see "ZOPE ready to handle requests" at the prompt.


Usage
=====

Access forum
------------

In a browser open 'localhost:8080/Plone/forumail'.

Login with 'admin:'admin', or 'forumailer:forumailer', or any member of the group 'forumailers'.


Add post via Web-UI
-------------------

Click 'Add new...' -> 'Page', fill out form, save.


Reply to post via Web-UI
------------------------

TODO

Add post via mail
-----------------

As a groupmember (if usermail=fromaddress) send a mail to 'forumail@[YOURMAILDOMAIN]'.
Add tags (=categories) in body, like this: '[tag1,tag2,tag3]'.

Reply to post via mail
----------------------

Reply to the mail-notification of an added post, leave subject untouched.

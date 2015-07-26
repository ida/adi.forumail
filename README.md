Introduction
============

An experimental proof of concept for a mailinglist/forum-hybrid, realized with Plone.

For development-purposes only, will store inbox-password in plaintext two times,
change-/removable with:

    $ crontab -e

    $ vim ~/forumail/dev-addons/adi.forumail/adi/forumail/profiles/default/mailhost.xml

The installer-script creates a folder in your $HOME called 'forumail' and
install Plone and this addon in it.


Requirements
=============

- Operating system is unixish and the sys-pckgs Plone needs, are preinstalled.

- A Mail-inbox with IMAP-support and an SMTP-Server.


Dependencies
============

- mailtoplone.base
- collective.contentrules.mailtogroup

Currently dev-versions, will be fetched of installer-script.


Installation
============


Download the installer script
-----------------------------

    $ wget https://raw.githubusercontent.com/ida/adi.forumail/master/buildout_forumail.sh



Set credentials in it
---------------------

Open the script with a text-editor and enter the needed mailaccount-credentials.
Optionally set more params, like a shared eggs-directory, if you got one already.


Make sure, it's executable
--------------------------

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

Login with 'admin:'admin', or 'forumailer:forumailer',
or any member of the group 'forumailers'.


Add post via Web-UI
-------------------

Click 'Add new...' -> 'Page', fill out form, save.


Reply to post via Web-UI
------------------------

TODO

Add post via mail
-----------------

Send a mail to your inboxes address.
Add tags (=categories/keywords) in the last line, like this: '[tag1,tag2,tag3]'.


Reply to post via mail
----------------------

Reply to the mail-notification of an added post, leave subject and last line untouched.

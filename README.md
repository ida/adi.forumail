Introduction
============

An experimental proof of concept for a mailinglist/forum-hybrid, realized with Plone.

Currently ment for development-purposes only: Will store the mail-password(s)
on the filesystem in plaintext. See Installation-chapter below for details.


Requirements
=============

- Operating-system is unixish and the sys-pckgs Plone needs, are preinstalled.

- A mail-account with IMAP-support, for receiving mails and an SMTP-server for
sending mails. Can possibly be of same provider.


Dependencies
============

- mailtoplone.base

- collective.contentrules.mailtogroup

Currently dev-versions, see Installation-chapter below.


Installation
============

Preamble
--------

You can read the provided installer-script as a documentation and e.g., if you 
have Plone installed alread, skip these parts. If you excute it, it will:

- Create a folder in your home-directory, named 'forumail'. In it installs
ZOPE, Plone, this addon and its dependencies. The latter as development-versions.

- Add a cron-entry in your system-user's crontab, holding your IMAP-credentials,
to look up the inbox for new mails, every 10 seconds and push them as news-items
into the Plonesite. *Note:* You can remove this entry again, if you ever want this
to stop, by editing it with:

     `$ crontab -e`

- Add XML-configs into this addon, holding the SMTP-mail-credentials, to set them
during the Plonesite-installation. *Note* After the installation you can remove them,
if you want. The concerned files are:

    $ rm ~/forumail/dev-addons/adi.forumail/adi/forumail/profiles/default/mailhost.xml
    $ rm ~/forumail/dev-addons/adi.forumail/adi/forumail/profiles/default/properties.xml

- Add a sample Plonesite-user 'forumailer' with the mailddress 'forumailer@[YOUR-PLONESITE-SERVER-DOMAIN]'.
If you're running this locally, the domain will get the dummy 'example.org'. Assigns user to group 'forumailers'.

- Creates a first welcome-post, the user 'forumailer' should be notified of it
via mail then, if the set mail-address of 'forumailer' doesn't exist, say is 'forumailer@example.org',
you can change the mail-address after installation, via:
`http://localhost:8080/Plone/@@user-information?userid=forumailer'


Download the installer script
-----------------------------

    $ wget https://raw.githubusercontent.com/ida/adi.forumail/master/buildout_forumail.sh



Set credentials in it
---------------------

Open the script with a text-editor and enter the needed mailaccount-credentials.
Optionally set more params, like a shared eggs-directory, if you have one already.


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

TODO: Provide a button, which triggers a post-creation with the next increasing id
relative to the post answered to, e.g.: '1-1' -> '1-2', or '2-7-3' -> '2-7-4'.


Add post via mail
-----------------

Send a mail to your inboxes address.


Reply to post via mail
----------------------

Reply to the mail-notification of an added post, leave subject
and last line of mailbody untouched.


TODOS
=====

- Parse mail for tags in last-line, looking like `(tag1, tag2, tag3)`
and apply them to the pushed post.
Or: Look for hashtags (words starting with '#'), anywhere in the body.

- Lookup sender mail-address before pushing a mail to the Plone-site and grant
the user of the Plone-site with the same mailaddress the Creator-role on the post.

- On install, create collections with alphabetical and newest ordering.


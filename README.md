Introduction
============

For now, an experimental proof of concept for a mailinglist/forum-hybrid, realized with Plone.

Preparation
===========

You need a mail-account and -server for the mailinglist.
A filter must be set, to let only mails of permitted senders
(=Plonesite-users) come through to the inbox.

Dependencies
============

Development-versions of mailtoplone.base and collective.contentrules.mailtogroup,
will be installed of script automatically.

Installation
============

Download the installer script
-----------------------------

    $ wget https://raw.githubusercontent.com/ida/adi.forumail/master/buildout_forumail.sh

Open the script with a text-editor and enter the needed mailaccount-credentials.


Make the script executable
--------------------------

    $ chmod +x buildout_forumail.sh


Execute the installer script
----------------------------

    $ ./buildout_forumail.sh


- It creates a folder '~/.virtualenv' and installs buildout 
in it, isolation is a good idea, here.

- It creates a folder '~/.buildout/eggs', to store the 
needed sources.

- It will create a folder named 'instance' right where you 
are, to be the home of server and dev-addons,
do the installs and start server in foreground.

- It enters six crons, to achieve a period of ten seconds
  for triggering the mail-inbox-lookup and dropping them to Plone.
  In case, you want to remove them again, you can do this with:
  
    $ crontab -e


If everything went fine, after a while, 
you should see "ZOPE ready to handle requests" at the prompt.


Enter the Plonesite's mailsettings
----------------------------------

Open 'http://localhost:8080/Plone/mail-controlpanel in a browser, set credentials.



Create users and assign them to a group
---------------------------------------

Create user's via 'http://localhost:8080/Plone/usergroup-userprefs',
assign the wanted participants to the group 'Reviewers' (TODO: Create dedicated Group).

!!! Make sure, you don't have a user with the same email-adress as the inbox,
    that'll create an infinite circuit of dropping a mail to plone, 
    get notified via mail, drop that new mail...


Grant permissions on container (TODO: do programatically)
------------------------------
Go to 'http://localhost:8080/Plone/dropbox/sharing', 
grant 'Can add'-permission to group Reviewers.

If you don't want to publish the dropbox-folder, also add 'Can view'.


Give it a go
------------

- Mails landing in your specified inbox should be automatically be pushed to the dropbox-folder.

- Users of group Reviewers, can add (news-)items in the dropbox-folder, 
all Reviewers will be notified of the new post with a mail, containing all the bodytext.


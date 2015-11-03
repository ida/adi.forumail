Introduction
============

A mailinglist/forum-hybrid, realized with Plone.


Requirements
=============

- SMTP-server for sending mails.

- Mail-inbox with IMAP-support.


Dependencies
============

- mailtoplone.base

- collective.contentrules.mailtogroup


Installation
============


Add cron for fetching mails of inbox
------------------------------------

    crontab -e

Hit 'i' for insertion-mode, paste these lines into it, replace the vars in square-brackets and possibly also 'admin:admin':

    * * * * * [PATH_TO]/mailtoplone.base/mailtoplone/base/scripts/fetchemail -u http://admin:admin@[PLONESITE_URL]/forumail -i [IMAP_SERVER] -t [IMAP_PORT] -e [INBOX_USERNAME] -p [INBOX_PASSWORD];

This will look up your inbox for new mails every minute. You can increase the
interval, by repeating the command with a prepended delay via 'sleep', e.g. the
following line will look into the inbox every 30 seconds:

    * * * * * [PATH_TO]/mailtoplone.base/mailtoplone/base/scripts/fetchemail -u http://admin:admin@[PLONESITE_URL]/forumail -i [IMAP_SERVER] -t [IMAP_PORT] -e [INBOX_USERNAME] -p [INBOX_PASSWORD]; sleep 30 && [PATH_TO]/mailtoplone.base/mailtoplone/base/scripts/fetchemail -u http://admin:admin@[PLONESITE_URL]/forumail -i [IMAP_SERVER] -t [IMAP_PORT] -e [INBOX_USERNAME] -p [INBOX_PASSWORD];


Theoretically that'll allow to trigger the mailtoplone-script every second.
A good period can be every 10 seconds.

When done, hit Esc-key for leaving insertion-mode and type ':wq' to save and
close the file. The cron wil be active immediately.

In case needed, you can remove the entry again like this:
After opening with 'crontab -e', hit the 'd'-key as long,
 until nothing's left, then again do ':wq'.


Get addon and its dependencies
-------------------------------

    cd your-dev-eggs-dir
    git clone https://github.com/ida/adi.forumail
    git clone https://github.com/ida/collective.contentrules.mailtogroup --branch forumail
    git clone https://github.com/ida/mailtoplone.base --branch forumail


Add them to buildout
---------------------

Modify your buildout.cfg accordingly:

    [buildout]
    
    development =
        your-dev-eggs-dir/adi.forumail
        your-dev-eggs-dir/mailtoplone.base
        your-dev-eggs-dir/collective.contentrules.mailtogroup
    
    [instance]
    
        eggs =
            adi.forumail
            mailtoplone.base

        zcml =
            mailtoplone.base


Update build and raise server
-----------------------------

    cd your/instance
    ./bin/instance stop
    ./bin/buildout
    ./bin/instance fg


Set sender-mailaccount
----------------------

Navigate to http://example.org:8080/yourPloneSiteId/mail-controlpanel and enter your
SMTP-credentials, if not done already.


Install forumail
----------------

Navigate to http://example.org:8080/yourPloneSiteId/prefs_install_products_form,
check the box at 'adi.forumail', click 'Activate addon'.
You should now find a folder called 'forumail' on first level of your site.

Specify 'To'-address in contentrule for mail-notifica
-----------------------------------------------------

Navigate to 
http://example.org:8080/yourPloneSiteId/++rule++forumail/@@manage-elements,
scroll down to "Send email to groups and members", click "Edit".

You should now get a popup-form, in there, enter your inbox-address in the 
field "Email source", replace '[INBOX_MAIL_ADDRESS]' with your inbox-address,
scroll down, click "Save".

You'll land back on the contentrule-form. To be on the sure side, also there
click "Save", right below the "Enabled"-field.


Define allowed categories
-------------------------

Navigate to:

    http://localhost:8080/Plone/forumail/edit/#fieldsetlegend-categorization

Enter the categories you want to be available, where it's written "Create and
apply new tags", click save.

Categories are filtered of mails, whether the parent-folder holds the given
categories, too, or not.

Users adding posts via the web-UI can only choose of categories you defined on
the forum's folder.


Create users for forumail-group
-------------------------------

Before adding posts, please add at a least one user to the forumail-group,
otherwise the mail-notifica-contentrule will rightfully moan there's no
recipients available to send the notification to.

Alternatively disable the contentrule, if you only want to use the forum's
web-UI and don't need the mailing-functionality.

Create users via:

    http://localhost:8080/Plone/@@new-user

Enter at least the user-id, the user-mailaddress
and make sure, to check the box at the group 'Forumailers'.
Click save.


Usage
=====

Add post via Web-UI
-------------------

Click plus-symbol on top, fill out title- and text-field, apply tags, save.


Reply to post via Web-UI
------------------------

Click 'Reply', fill out text-field, save.


Add post via mail
-----------------

Send a mail to your inbox'es address.

Optionally add categories in the last line of your mail like this:

    [a category, another category, cat é gory]


Reply to post via mail
----------------------

Reply to the mail-notification of an added post, leave subject
and last line of mailbody untouched.


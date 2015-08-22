Introduction
============

An experimental proof of concept for a mailinglist/forum-hybrid, realized with Plone.

Currently ment for development-purposes only: Will store the inboxe's password
on the filesystem in plaintext. See installation-chapter below, for details.


Goal
====

Replace the currently used non-Plone-based forum of the Plone-community,
as it has flaws and because Plone can.


Preamble
========

If you have questions or suggestions or would like to contribute, don't
hesitate to open an issue, or, if you don't have/want a GitHub-account,
send a mail to <contact@ida-ebkes.eu>.

Plone-newbies and -wannabies, are very welcome to participate, basic skills
with CSS and/or JS and/or Python should help, but there's always non-programming
things to do, just ping.

If people get involved, the author (meh) will certainly love to move
this addon into the collective-namespace.

"Old-style"-techniques are used for the sake of holding everything configurable
via a site's UI, which is one of my attempts, when developing addons, in order to
empower the site-users and not be depending on hiring a Ploneirdo, or learn how to
plone for next two years, before being able, to become truly productive.

Nevertheless alternative suggestions will be happily considered and ideally,
sub-packages are created, to keep it modular and even have several possibilities
to choose of.


Requirements
=============

- Operating-system is unixish and the sys-pckgs Plone needs, are preinstalled.

- Two mailaccounts, residing at the same domain:
One with SMTP-support for sending mail, e.g. 'forumail@example.org',
and one with IMAP-support for receiving mail, e.g. 'forumailers@example.org'.


Dependencies
============

Will be installed by buildout along the way:

- mailtoplone.base (development-version)

- collective.contentrules.mailtogroup (development-version)

- collective.formcriteria


Installation
============

You can use the installer-script './build_forumail.sh', read its first lines,
to get further instructions, or, if you have a Plone-instance already, also do
the following steps manually.

Note: The usual prompt-prefix for commands is ommited, so one can copy'n'paste them.


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


Update build
------------

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


Specify 'To'-address in contentrule for mail-notifica
-----------------------------------------------------

Navigate to 
http://example.org:8080/yourPloneSiteId/++rule++forumail/@@manage-elements,
scroll down to "Send email to groups and members", click "Edit".

You should now get a popup-form, in there, enter your inbox-address in the 
field "Email source", replace '[INBOX_MAIL_ADDRESS]' with your inbox-address, scroll down, click "Save".

You'll land back on the contentrule-form. To be on the sure side, also there click "Save",
right below the "Enabled"-field.


Usage
=====

In a browser open 'example.org:8080/Plone/forumail'.

Login as admin, or as any member of the group 'Forumailers'.

Define allowed categories
-------------------------

Navigate to:

    http://localhost:8080/Plone/forumail/edit/#fieldsetlegend-categorization

Enter the categories you want to be available, where it's written "Create and apply new tags", and click save.

Categories are filtered of mails, whether the parent-folder holds the given
categories, too, or not.

Users adding posts via the web-UI can only choose of categories you defined on the
forum's folder.


Add post via Web-UI
-------------------

Click 'Add new post', fill out form, save.


Reply to post via Web-UI
------------------------

Click 'Reply', fill out form, save.


Add post via mail
-----------------

Send a mail to your inboxes address.

Optionally add categories in the last line of your mail like this:

    [a category, another category, cat é gory]


Reply to post via mail
----------------------

Reply to the mail-notification of an added post, leave subject
and last line of mailbody untouched.


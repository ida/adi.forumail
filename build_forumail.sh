# Leave these two untouched:
forum_name=forumail
site_domain=$HOSTNAME

# Set and check the following:
inbox_server=imap.gmail.com
inbox_port=993
inbox_user=asmith
inbox_password=aSuperSecretPassword
inbox_address=asmith@gmail.com

sender_server=localhost
sender_port=25
sender_user=$forum_name
sender_password=$sender_user
sender_address=$forum_name@$site_domain

# Optionally change:
forum_dir=$HOME/$forum_name
instance_dir=$forum_dir/server
eggs_dir=$forum_dir/apps
dev_eggs_dir=$forum_dir/dev-apps
plone_version='4.3.6'

################## Don't change anything after this line. #####################
mailtoplone_folder=http://admin:admin@localhost:8080/Plone/$forum_name
mailtoplone_script=$dev_eggs_dir/mailtoplone.base/mailtoplone/base/scripts/fetchemail
mailtoplone_command="${mailtoplone_script} -u ${mailtoplone_folder} -i ${inbox_server} -t ${inbox_port} -e ${inbox_address} -p ${inbox_password}"

###########  Create folders, install buildout with pip in a virtenv and get dev-eggs:
rm -rf $instance_dir; mkdir -p $instance_dir; cd $instance_dir;
virtualenv py-env; . pyenv/bin/activate
pip install setuptools -U; pip install zc.buildout
mkdir -p $eggs_dir ; mkdir -p $dev_eggs_dir; cd $dev_eggs_dir
git clone https://github.com/ida/adi.forumail
git clone https://github.com/ida/collective.contentrules.mailtogroup --branch forumail
git clone https://github.com/ida/mailtoplone.base  --branch forumail

###########  Pass this sever's domain to addon-install-setup-script (not available to script during runtime):
fil=$dev_eggs_dir/adi.forumail/adi/forumail/setuphandlers.py
printf "        site_domain = '$site_domain'
        if not INSTALLED_INITIALLY:
            doOnInstall(site, app_name, site_domain, INSTALLED_INITIALLY)
            INSTALLED_INITIALLY = True
" >> $fil
###########  Set plonesite-mail-credentials via profile/default-xml-files:
pro=$dev_eggs_dir/adi.forumail/adi/forumail/profiles/default
fil=$pro/mailhost.xml
rm $fil
printf "<?xml version=\"1.0\"?>
<object name=\"MailHost\"
    smtp_host=\"$sender_server\"
    smtp_port=\"$sender_port\"
    />
" >> $fil
    #smtp_pwd=\"$sender_password\"
    #smtp_uid=\"$sender_user\"
fil=$pro/properties.xml
rm $fil
printf "<?xml version=\"1.0\"?>
<site>
 <property name=\"email_from_address\"
    type=\"string\">$sender_address</property>
 <property name=\"email_from_name\"
    type=\"string\">$sender_address</property>
</site>
" >> $fil
########### Write buildout.cfg:
fil=$instance_dir/buildout.cfg
rm $fil
printf "[buildout]
parts =
    instance
    plonesite
    mailtoplone_cron
eggs-directory = $eggs_dir
extends = http://dist.plone.org/release/$plone_version/versions.cfg
#extends = $HOME/.buildout/versions.cfg # DEV
#offline = true                         # DEV
develop =
    $dev_eggs_dir/adi.forumail
    $dev_eggs_dir/mailtoplone.base
    $dev_eggs_dir/collective.contentrules.mailtogroup
[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
    Pillow
    Plone
    adi.forumail
    mailtoplone.base
    plone.reload

zcml =
    mailtoplone.base
    plone.reload

[plonesite]
recipe = collective.recipe.plonesite == 1.9.0
products = adi.forumail
[mailtoplone_cron]
# Fetch emails of an inbox and drop them to a plonesite-folder every ten seconds:
recipe = z3c.recipe.usercrontab
# Every minute ...
times = * * * * *
# ... execute 'mailtoplone_command' six times,
#     each time with an increasing delay of ten seconds via 'sleep':
command = $mailtoplone_command; sleep 10 && $mailtoplone_command; sleep 20 && $mailtoplone_command; sleep 30 && $mailtoplone_command; sleep 40 && $mailtoplone_command; sleep 50 && $mailtoplone_command
" >> $fil
####################### Build it out:
cd $instance_dir
buildout -U # U(pdate)-option ignores a possible existing '~/.buildout/default.cfg'.
####################### Start server:
./bin/instance fg # Run in foreground, for better debugging.

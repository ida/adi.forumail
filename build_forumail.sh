forum_name='forumail' # Do *not* change this one :-)

# Must haves, you gotta set at least these two:
mailbox_password=')§)DH"kdow3o330d"D\+'
mailbox_domain=gmail.com

# And doublecheck the following vars, based on good assumptions:
mailbox_username=$forum_name
mailbox_adress=$mailbox_username@$mailbox_domain
mailbox_name=$mailbox_adress
mailbox_server=$mailbox_domain
imap_server=imap.$mailbox_server
smtp_server=smtp.$mailbox_server
imap_port=993
smtp_port=25

# Change optionally:
instance_dir=$HOME/$forum_name
eggs_dir=$HOME/.buildout/eggs # $instance_dir/addons
dev_eggs_dir=$instance_dir/dev-addons
plone_version='4.3.5'

# Very well done, save, exit and make
# sure this script is executable:
# $ chmod +x buildout_forumail.sh
# Then execute it:
# $ ./buildout_forumail.sh
# Thanks! Oh look: A dragon...

# Hardies, do not change:
mailtoplone_folder=http://admin:admin@localhost:8080/Plone/$forum_name
mailtoplone_script=$dev_eggs_dir/mailtoplone.base/mailtoplone/base/scripts/fetchemail
mailtoplone_command="${mailtoplone_script} -u ${mailtoplone_folder} -i ${imap_server} -t ${imap_port} -e ${mailbox_name} -p ${mailbox_password}"

####  Create folders, install buildout with pip in a virtenv and get dev-eggs:
rm -rf $instance_dir; mkdir -p $instance_dir; cd $instance_dir;
virtualenv py-env; . pyenv/bin/activate
pip install setuptools -U; pip install zc.buildout
mkdir -p $eggs_dir ; mkdir -p $dev_eggs_dir; cd $dev_eggs_dir
git clone https://github.com/ida/adi.forumail
git clone https://github.com/ida/collective.contentrules.mailtogroup --branch $forum_name 
git clone https://github.com/ida/mailtoplone.base  --branch $forum_name

####  Set plonesite-mail-credentials via profile/default-xml-files:
pro=$dev_eggs_dir/adi.forumail/adi/forumail/profiles/default
fil=$pro/mailhost.xml
rm $fil
printf "<?xml version=\"1.0\"?>
<object name=\"MailHost\"
    smtp_host=\"$smtp_server\"
    smtp_port=\"$smtp_port\"
    smtp_pwd=\"$mailbox_password\"
    smtp_uid=\"$mailbox_name\"
    />
" >> $fil
fil=$pro/properties.xml
rm $fil
printf "<?xml version=\"1.0\"?>
<site>
 <property name=\"email_from_address\"
    type=\"string\">$mailbox_address</property>
 <property name=\"email_from_name\"
    type=\"string\">$mailbox_address</property>
</site>
" >> $fil
#################     Write buildout.cfg:    ##########################
fil=$instance_dir/buildout.cfg
rm $fil
printf "[buildout]
parts =
    instance
    plonesite
    mailtoplone_cron
eggs-directory = $eggs_dir
extends = http://dist.plone.org/release/$plone_version/versions.cfg
#DEV:extends = $HOME/.buildout/versions.cfg
#DEV:offline = true
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
#DEV:    plone.reload
zcml =
    mailtoplone.base
#DEV:    plone.reload
[plonesite]
recipe = collective.recipe.plonesite == 1.9.0
products = adi.forumail
[mailtoplone_cron]
# Fetch emails of an inbox and drop them to a plonesite-folderevery ten seconds:
recipe = z3c.recipe.usercrontab
# Every minute ...
times = * * * * *
# ... execute 'mailtoplone_command' six times,
#     each time with an increasing delay of ten seconds via 'sleep':
command = $mailtoplone_command; sleep 10 && $mailtoplone_command; sleep 20 && $mailtoplone_command; sleep 30 && $mailtoplone_command; sleep 40 && $mailtoplone_command; sleep 50 && $mailtoplone_command
" >> $fil
#################     Build it out:          ##########################
cd $instance_dir
buildout -U # we use U-option, to ignore a possible existing '~/.buildout/default.cfg'
#################     Start server:          ##########################
./bin/instance fg # in foreground, for better debugging

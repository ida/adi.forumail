#!/bin/bash
#
# This is an install-helper for the Plone-addon 'adi.forumail'.
#
# Requires to have Plone's needed sys-pckgs to be pre-installed.
#
# Creates a container-directory named 'forumail' in your $HOME,
# adds and installs the add-on and its dependencies in it, using
# a virtualenv, to not screw up your enviroment, nor be screwed up of it.
#
# Adds a cron in your user's crontab, for fetching mails of inbox. The inboxe's
# password will be stored in it in plaintext. You can edit/remove it with `crontab -e`, in case.
#
# Adds xml-files to the addon on the fly, holding mail-creds. Also there, the
# password is stored in plaintext, after install you can safely remove them,
# they are no longer longer needed. By default, you'll find them here:
#
# $HOME/forumail/dev-eggs/adi/forumail/profiles/default/mailhost.xml
# $HOME/forumail/dev-eggs/adi/forumail/profiles/default/mailhost.xml
#
# Set the following var's vals:

inbox_address=''    # forumailers@some-domain.net
inbox_password=''   # 'lkqqn392§$42pi'
inbox_user_id=''    # some-domain-0027

imap_host=''        # imap.provider.org
imap_port=993


sender_address=''   # forumail@some-domain.net
sender_password=''  # 'lk82$")!81jdDNWo++3'
sender_user_id=''   # some-domain-0042

smtp_host=''        # smtp.provider.org
smtp_port=25

# Optionally change:

project_dir=$HOME/forumail
eggs_dir=$project_dir/.addons # $HOME/.buildout/eggs
dev_eggs_dir=$project_dir/dev-addons
instance_dir=$project_dir/instance
plone_version='4.3.6'


# That's all needed, execute this script of the commandline, like this:
# ./build_forumail.sh
#
# In case it should complain about permissions, make it executable beforehand with:
# chmod +x build_forumail.sh
#
# Count in about 15 minutes for the install, if you're not using a shared eggs-dir.
#
# If everything went allright, you should see 'ZOPE ready for taking requests', the
# prompt, then open http://localhost:8080/Plone/forumail and login with 'admin:admin'.
#
#
##### Don't change anything after this line, unless you know, what you are doing. ####

mailtoplone_folder=http://admin:admin@localhost:8080/Plone/forumail
mailtoplone_script=$dev_eggs_dir/mailtoplone.base/mailtoplone/base/scripts/fetchemail
mailtoplone_command="${mailtoplone_script} -u ${mailtoplone_folder} -i ${imap_host} -t ${imap_port} -e ${inbox_user_id} -p ${inbox_password}"

dev_egg_profile=$dev_eggs_dir/adi.forumail/adi/forumail/profiles/default

this_script_name=`basename "$0"`
devinfo_prefix="INFO ${this_script_name}:"


createFolders() { 
    mkdir -p { $instance_dir, $eggs_dir, $dev_eggs_dir }
                    echo $devinfo_prefix Created project-containers $instance_dir, $eggs_dir, and $dev_eggs_dir.
}
createAndActivateVirtenv() {
    cd $project_dir
    virtualenv .virtenv
    . .virtenv/bin/activate
                    echo $devinfo_prefix Created and activated a virtual enviroment in $project_dir/.virtenv.
}
installBuildout() {
    createAndActivateVirtenv
    cd $project_dir
    pip install setuptools -U; # *The* dependency of any distributed Python-egg, as buildout is. Upgrade with -U, to avoid conflicts.
    pip install zc.buildout
                    echo $devinfo_prefix Installed buildout via pip of the currently activated virtenv.
}
getDevEggs() {   
    cd $dev_eggs_dir
    git clone https://github.com/ida/adi.forumail
    git clone https://github.com/ida/collective.contentrules.mailtogroup --branch forumail
    git clone https://github.com/ida/mailtoplone.base  --branch forumail
                    echo $devinfo_prefix Cloned dev-eggs into $dev_eggs_dir.
}
setMailCredsViaXML() {
    printf "<?xml version=\"1.0\"?>
<site>
 <property name=\"email_from_address\"
    type=\"string\">$sender_address</property>
 <property name=\"email_from_name\"
    type=\"string\">$sender_address</property>
</site>
    " > $dev_egg_profile/properties.xml
                    echo $devinfo_prefix Sender-address and -name in Plonesite set, via $fil
    fil=$dev_egg_profile/mailhost.xml
    rm $fil
    printf "<?xml version=\"1.0\"?>
<object name=\"MailHost\"
    smtp_host=\"$smtp_host\"
    smtp_port=\"$smtp_port\"
    " >> $fil
                    echo $devinfo_prefix SMPT-server and -port in Plonesite set, via $fil.
# If sender_password is not empty, (e.g. it would be empty, when using localhost) ...
    if [ -n $sender_password ]; then
# ... append creds:
        printf "smtp_pwd=\"$sender_password\"
smtp_uid=\"$sender_user_id\"" >> $fil
    fi
# And close tag:
    printf "
        />
    " >> $fil
                    echo $devinfo_prefix SMPT-server, -port and -password in Plonesite set via $fil.
}
writeBuildoutConfig() {
    fil=$instance_dir/buildout.cfg
    if test -f "$fil"; then rm $fil; fi;
    printf "[buildout]
parts =
    instance
    plonesite
    mailtoplone_cron
eggs-directory = $eggs_dir
extends = http://dist.plone.org/release/$plone_version/versions.cfg
#DEV: extends = $HOME/.buildout/versions.cfg
#DEV: offline = true
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

[mailtoplone_cron]
# Fetch emails of an inbox and drop them to a plonesite-folder every ten seconds:
recipe = z3c.recipe.usercrontab
# Every minute ...
times = * * * * *
# ... execute 'mailtoplone_command' six times,
#     each time with an increasing delay of ten seconds via 'sleep':
command = $mailtoplone_command; sleep 10 && $mailtoplone_command; sleep 20 && $mailtoplone_command; sleep 30 && $mailtoplone_command; sleep 40 && $mailtoplone_command; sleep 50 && $mailtoplone_command

[plonesite]
recipe = collective.recipe.plonesite == 1.9.0
products = adi.forumail
" >> $fil
                    echo $devinfo_prefix Buildout-config written.
}
buildOut() {
    cd $instance_dir
    buildout -U # U(pdate)-option ignores a possible existing '~/.buildout/default.cfg'.
                    echo $devinfo_prefix Buildout finished.
}
runInstance() {
    cd $instance_dir
    ./bin/instance fg;
                    echo $devinfo_prefix Starting instance in foreground, now.
}
devDestroyProjectDir() {
    rm -rf $project_dir
                    echo $devinfo_prefix Destroyed project-container.
}
devDestroyDeveggsDir() {
    rm -rf $dev_eggs_dir
                    echo $devinfo_prefix Destroyed deveggs-container.
}
devDestroyPlonesite() {
    buildout_entry_to_add='site-replace=true'
    buildout_config_path=$instance_dir/buildout.cfg
    buildout_config_text=$(<$buildout_config_path)
    printf "site-replace=true" >> $instance_dir/buildout.cfg
                    echo $devinfo_prefix Buildout-config set to destroy plonesite.
}
devCopyDeveggXMLToDevrepoXML() {
    dev_repo_profile=/home/ida/repos/adi.forumails/adi/forumail/profiles/default
    cp $dev_egg_profile/mailhost.xml $dev_repo_profile/mailhost.xml
    cp $dev_egg_profile/properties.xml $dev_repo_profile/properties.xml
                    echo $devinfo_prefix Copied dev-egg-xmls to dev-repo-xmls.
}
devSymlinkDeveggsToDevrepos() {
    cd $dev_eggs_dir; rm -rf adi.forumail; ln -s /home/ida/repos/adi.forumail
                    echo $devinfo_prefix Destroyed dev-egg and added symlink to dev-repo.
}
devReplaceDevEggsWithRepoEggs() {
    devCopyDeveggXMLToDevrepoXML
    devSymlinkDeveggsToDevrepos
}
main() {
#devDestroyProjectDir
#    createFolders
#    installBuildout
#    getDevEggs
#devReplaceDevEggsWithRepoEggs
    setMailCredsViaXML
    writeBuildoutConfig
#devDestroyPlonesite
    buildOut
    runInstance
}
main


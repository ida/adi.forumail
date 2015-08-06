project_name=forumail

# Set and check the following:

mail_server_domain=example.com
mail_address_domain=example.org

inbox_user_id=exampleorg-0001
inbox_password='superSecretPassword'
inbox_address=$project_name@$mail_address_domain
inbox_server=imap.$mail_server_domain
inbox_port=993

sender_user_id=$inbox_user_id
sender_password=$inbox_password
sender_address=$inbox_address
sender_server=smtp.$mail_server_domain
sender_port=25

# Optionally change:

project_dir=$HOME/$project_name
instance_dir=$project_dir/instance
eggs_dir=$project_dir/.addons # $HOME/.buildout/eggs
eggs_dir=$HOME/.buildout/eggs
dev_eggs_dir=$project_dir/dev-addons
plone_version='4.3.6'

##### Don't change anything after this line unless you know what you are doing. ####

mailtoplone_folder=http://admin:admin@localhost:8080/Plone/$project_name
mailtoplone_script=$dev_eggs_dir/mailtoplone.base/mailtoplone/base/scripts/fetchemail
mailtoplone_command="${mailtoplone_script} -u ${mailtoplone_folder} -i ${inbox_server} -t ${inbox_port} -e ${inbox_user_id} -p ${inbox_password}"

this_script_name=`basename "$0"`
devinfo_prefix=INFO_$this_script_name: 

createFolders() {
mkdir -p $instance_dir; mkdir -p $eggs_dir ; mkdir -p $dev_eggs_dir
}
installBuildout() {
    cd $project_dir
    virtualenv .virtenv
    . .virtenv/bin/activate
    pip install setuptools -U; pip install zc.buildout
}
getDevEggs() {   
    cd $dev_eggs_dir
    git clone https://github.com/ida/adi.forumail
    git clone https://github.com/ida/collective.contentrules.mailtogroup --branch forumail
    git clone https://github.com/ida/mailtoplone.base  --branch forumail
}
setMailCredsViaXML() {
    dev_egg_profile=$dev_eggs_dir/adi.forumail/adi/forumail/profiles/default
    fil=$dev_egg_profile/mailhost.xml
    rm $fil
    printf "<?xml version=\"1.0\"?>
<object name=\"MailHost\"
    smtp_host=\"$sender_server\"
    smtp_port=\"$sender_port\"
    " >> $fil
# If sender_password is not empty...
    if [ -n $sender_password ]; then
# ... append creds:
        printf "smtp_pwd=\"$sender_password\"
smtp_uid=\"$sender_user_id\"" >> $fil
    fi
# And close tag:
    printf "
        />
    " >> $fil

    fil=$dev_egg_profile/properties.xml
    rm $fil
    printf "<?xml version=\"1.0\"?>
<site>
 <property name=\"email_from_address\"
    type=\"string\">$sender_address</property>
 <property name=\"email_from_name\"
    type=\"string\">$sender_address</property>
</site>
    " >> $fil
} # EO setMailCreds()
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
} # EO writeBuildoutConfig()
buildOut() {
    cd $instance_dir
    buildout -U # U(pdate)-option ignores a possible existing '~/.buildout/default.cfg'.
}
runInstance() {
    cd $instance_dir
    ./bin/instance fg # In foreground, for better debugging.
}
devDestroyProjectDir() {
    rm -rf $project_dir; echo INFO $0: Destroyed project-container.
}
devDestroyDeveggsDir() {
    rm -rf $dev_eggs_dir; echo INFO $0: Destroyed deveggs-container.
}
devDestroyPlonesite() {
    printf "site-replace=true" >> $instance_dir/buildout.cfg
    echo $devinfo_prefix: Config set to destroy plonesite.
}
devCopyDeveggXMLToDevrepoXML() {
    dev_repo_profile=$HOME/repos/adi.forumail/adi/forumail/profiles/default
    cp $dev_egg_profile/mailhost.xml $dev_repo_profile/mailhost.xml
    cp $dev_egg_profile/properties.xml $dev_repo_profile/properties.xml
    echo $devinfo_prefix: Copied dev-egg-xmls to dev-repo-xmls.
}
devSymlinkDeveggsToDevrepos() {
    cd $dev_eggs_dir; rm -rf adi.forumail; ln -s /home/ida/repos/adi.forumail
    echo $devinfo_prefix: Symlinked dev-egg to dev-repo.
}
devReplaceDevEggsWithRepoEggs() {
    devCopyDeveggXMLToDevrepoXML
    devSymlinkDeveggsToDevrepos
}
main() {
#devDestroyProjectDir
    createFolders
    installBuildout
    getDevEggs
#devReplaceDevEggsWithRepoEggs
    setMailCredsViaXML
    writeBuildoutConfig
#devDestroyPlonesite
    buildOut
    runInstance
}
main


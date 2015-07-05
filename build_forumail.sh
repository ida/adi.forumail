# Set/change the following 4 vars!
account_name=yourMailAccountName[@yourMailProvider.com]
account_password=yourSuperSecretPassword
imap_server=imap.yourMailProvider.com
imap_port=993

############# Don't change the following, unless, you know. ###############

dropbox=http://admin:admin@localhost:8080/Plone/dropbox
skript=src/mailtoplone.base/mailtoplone/base/scripts/fetchemail

# Create a virtualenviroment for an isolated Python-env:
mkdir -p $HOME/.buildout/eggs
virtualenv $HOME/.virtenv

# Install buildout in the virtenv:
./$HOME/.virtenv/bin/pip install zc.buildout

# Create folder for instance and dev-eggs:
mkdir -p instance/src

# Locate into dev-eggs-folder:
cd instance/src

# Get dev-eggs:
git clone https://github.com/ida/collective.contentrules.mailtogroup --branch 1.3.1
git clone https://github.com/ida/mailtoplone.base
git clone https://github.com/ida/adi.forumail

# Locate back into ZOPE-instance's folder:
cd ..

#################################
# Create and write buildout.cfg #
#################################

# Add first static string to buildout.cfg:
printf "[buildout]
parts =
    instance
    plonesite
" >> buildout.cfg

# Add an entry for every cron:
for i in {0..5}
do
    printf "    mailtoplone0${i}of06\n" >> buildout.cfg
done

# Add next static string to buildout.cfg:
printf "eggs-directory = $HOME/.buildout/eggs
extends = http://dist.plone.org/release/4.3.5/versions.cfg
develop =
    src/adi.forumail
    src/collective.contentrules.mailtogroup
    src/mailtoplone.base

[instance] # Install ZOPE and define the eggs to be installable to it:
recipe = plone.recipe.zope2instance
user = admin:admin
eggs =
    Pillow # Optional: A library for images-magic, like creating several size-formats.
    Plone  # Well...
    adi.forumail # Our Plone-Addon

[plonesite] # Create a plonesite when running buildout and install a product in it:
recipe = collective.recipe.plonesite==1.9.0 # newer versions break layout
products = adi.forumail

[versions] # Work around possible version conflicts with preinstalled components:
setuptools =
zc.buildout =
" >> buildout.cfg

# Add a cron-entry for every ten seconds:
kommand="${skript} -u ${dropbox} -i ${imap_server} -t ${imap_port} -e ${account_name} -p ${account_password}"
for i in {0..5}
do
    printf "\n[mailtoplone0${i}of06]
# Fetch mails of inbox every minute on the ${i}0th second:
recipe = z3c.recipe.usercrontab
times = * * * * *
command = sleep ${i}0 ${kommand}
" >> buildout.cfg
done


########################
#        MAIN          #
########################
buildout # execute buildout
./bin/instance fg#start # start ZOPE-server
#firefox localhost:8080/Plone/dropbox # open browser and watch the plonesite

#!/bin/bash

# Define tests
#
tests="../test/test_packages.py \
       ../test/test_services.py \
       ../test/test_files.py \
       ../test/test_sockets.py \
       ../test/test_commands.py"

# Run tests using testinfra
#
SCRIPTNAME=$(basename $0)
DIRNAME=$(dirname $0)

# Setup for pip virtual environment
#
export WORKON_HOME=~/.pyenvironments
mkdir -p ${WORKON_HOME}

# Install pips for python virtual environment
#
pip install virtualenv virtualenvwrapper

# Source env wrapper
#
source /usr/local/bin/virtualenvwrapper.sh

# Make a virtual environment to install new pips
#
mkvirtualenv ocptest

# Upgrade pip and install pips
#
pip install --upgrade pip
pip install testinfra paramiko requests

# Bring up VM ready to run tests and save ssh key for testinfra
#
(cd ${DIRNAME}/../vagrant && vagrant up ocptest --provision && vagrant ssh-config ocptest > ocptest-sshkey)

# Run tests
#
(cd ${DIRNAME}/../vagrant && testinfra -v --sudo --sudo-user=root --hosts=ocptest --ssh-config=./ocptest-sshkey ${tests})

# Exit from the virtual environment and clean it up
#
deactivate
rmvirtualenv ocptest

exit 0

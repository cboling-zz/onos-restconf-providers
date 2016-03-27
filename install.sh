#!/usr/bin/env bash
#
# Script to install all RESTCONF modules.  Call with argument -run to also run it
#
cmd="install"
installFile=".installed"
# If no .install file available, create one in the past

if [ ! -f ${installFile} ]
then
    touch --date="2000-01-01 00:00:00" ${installFile}
fi

if [ $# -gt 1 ] && [ $1 == "-run" ]
then
  cmd="install!"
  echo "Installing and running the RESTCONF Provider and Applications"
else
  echo "Installing the RESTCONF Provider and Applications"
fi

find . -cnewer ${installFile} -name *.oar -print -exec onos-app $OC1 $cmd {} \;

touch ${installFile}

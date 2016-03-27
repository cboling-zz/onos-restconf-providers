#!/usr/bin/env bash
#
# Script to reinstall all RESTCONF modules.  Call with argument -run to also run it
#
installFile=".installed"
cmd="reinstall"

# If no .install file available, create one in the past

if [ ! -f ${installFile} ]
then
    touch --date="2000-01-01 00:00:00" ${installFile}
fi
if [ $# -gt 1 ] && [ $1 == "-run" ]
then
  cmd="reinstall!"
  echo "Re-installing and running the RESTCONF Provider and Applications"
else
  echo "Re-installing the RESTCONF Provider and Applications"
fi
# Re-install the file if it is newer than the last time we installed anything

find . -cnewer ${installFile} -name *.oar -print -exec onos-app $OC1 $cmd {} \;

if [ $? -eq 0 ]
then
    touch ${installFile}
fi
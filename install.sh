#!/usr/bin/env bash
#
# Script to install all RESTCONF modules.  Call with argument -run to also run it
#
cmd="install"

if [ $# -gt 1 && $1 == "-run" ]
then
  cmd="install!"
  echo "Installing and running the RESTCONF Provider and Applications"
else
  echo "Installing the RESTCONF Provider and Applications"
fi

find . -name *.oar -print -exec onos-app $OC1 $cmd {} \;


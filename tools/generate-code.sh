#!/usr/bin/env bash
#
# The next is primarily to support test compile of PYANGBIND test modules
#
PYBINDPLUGIN=`/usr/bin/env python -c \
    'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`

echo "pyangbind plugin located at ${PYBINDPLUGIN}"

RESTCONF_MODULE_BASEDIR=$(pwd)/../modules
RESTCONF_MODULE_OUTDIR=${RESTCONF_MODULE_BASEDIR}/generated-code
RESTCONF_MODULES="toaster.yang example-jukebox.yang"
#RESTCONF_MODULES="toaster.yang"

for module in ${RESTCONF_MODULES}
do
    inFile=${RESTCONF_MODULE_BASEDIR}/${module}
    outFile=${RESTCONF_MODULE_OUTDIR}/${module%%.*}.py

    # Remove any existing generated output
    rm -f ${outFile}

    # Generate the code now
    echo "Generating code for '${module}' to file '${module%%.*}.py'"

    pyang --plugindir ${PYBINDPLUGIN} -f pybind ${PYBIND_OPTS} -o ${outFile} ${inFile}
done

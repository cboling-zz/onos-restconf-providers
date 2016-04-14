#!/usr/bin/env bash
#
# The next is primarily to support test compile of PYANGBIND test modules
#
PYBINDPLUGIN=`/usr/bin/env python -c \
    'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`

# echo "pyangbind plugin located at ${PYBINDPLUGIN}"

RESTCONF_MODULE_BASEDIR=$(pwd)/../modules
RESTCONF_MODULE_OUTDIR=${RESTCONF_MODULE_BASEDIR}/generated-code
RESTCONF_MODULES="toaster.yang example-jukebox.yang"
#RESTCONF_MODULES="toaster.yang"
PYBIND_OPTS="--use-extmethods --build-rpcs"

for module in ${RESTCONF_MODULES}
do
    inFile=${RESTCONF_MODULE_BASEDIR}/${module}

    # PEP 8 says we need all lowercase names and no hyphens or spaces...

    pyFile="${module%%.*}.py"
    outFile=`echo "${pyFile}" | tr " " _ | tr - _ | tr '[:upper:]' '[:lower:]'`

    # echo "Output file is ${outFile}"

    outFilePath=${RESTCONF_MODULE_OUTDIR}/${outFile}

    # Remove any existing generated output
    rm -f ${outFile} >/dev/null 2>&1

    # Generate the code now
    echo "Generating code for '${module}' to file '${pyFile}'"
    cmd="pyang --plugindir ${PYBINDPLUGIN} -f pybind ${PYBIND_OPTS} -p ${RESTCONF_MODULE_BASEDIR} -o ${outFilePath} ${inFile}"
    echo ${cmd}
    ${cmd}
    echo "------------"
done

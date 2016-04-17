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
PYIN_OPTS="--format=yin --yin-canonical --yin-pretty-strings --trim-yin"

for module in ${RESTCONF_MODULES}
do
    inFile=${RESTCONF_MODULE_BASEDIR}/${module}

    # PEP 8 says we need all lowercase names and no hyphens or spaces...

    pyFile="${module%%.*}.py"
    xmlFile="${module%%.*}.xml"

    pyOutFile=`echo "${pyFile}" | tr " " _ | tr - _ | tr '[:upper:]' '[:lower:]'`
    xmlOutFile=`echo "${xmlFile}" | tr " " _ | tr - _ | tr '[:upper:]' '[:lower:]'`

    # echo "Output file is ${outFile}"

    pyOutFilePath=${RESTCONF_MODULE_OUTDIR}/${pyOutFile}
    xmlOutFilePath=${RESTCONF_MODULE_OUTDIR}/${xmlOutFile}

    # Remove any existing generated output
    rm -f ${pyOutFilePath} ${xmlOutFilePath} >/dev/null 2>&1

    # Generate the python code now via pyangbind
    echo "Generating code for '${module}' to file '${pyFile}'"
    cmd="pyang --plugindir ${PYBINDPLUGIN} -f pybind ${PYBIND_OPTS} -p ${RESTCONF_MODULE_BASEDIR} -o ${pyOutFilePath} ${inFile}"
    echo ${cmd}
    ${cmd}

    # Create a corresponding YIN document as well so we can get access to all fields/attributes
    cmd2="pyang ${PYIN_OPTS} -p ${RESTCONF_MODULE_BASEDIR} -o ${xmlOutFilePath} ${inFile}"
    echo ${cmd2}
    ${cmd2}

    echo "------------"
done

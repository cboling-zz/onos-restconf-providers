# RESTConf Southbound Provider for ONOS

**NOTE**: Currently this code is being restructured to fit the current device model
and directory structure of the ONOS master GIT tip (post-falcon ... early goldeneye release).

Once this conversion is complete and a clean build is available, this notice will be
removed and the documentation updated below accordingly.

-------------------------------------------

This project provides a southbound device provider via RESTConf for ONOS.

The planned design for this module is to leverage the work done by
HappiestMinds's NetConf provider so that the same YANG tools and hopefully
their Flow-Rule provider can be reused.

For information on Happiest Mind's netConf provider, please refer to:
https://wiki.onosproject.org/display/ONOS/Design+Document

Currently, only the skeleton of each portion of the RESTConf provider is
available, so please check back later for updates.

-----------------------------------------------------------------------------
The project currently is written to be built out-of-tree.  To build and
install, setup the appropriate cell file and execute.

    # Local virtualbox RESTConf test with mininet 

    export ONOS_NIC=192.168.2.*
    export OC1="192.168.1.136"
    export OCN="192.168.1.136"

    export ONOS_APPS="drivers,openflow,fwd"

##Build:

    $ cd <restconf-base-dir>
    $ mvn clean install            # or use 'mci' shortcut

##Install with onos-app:

use install! or reinstall! to install or re-install and activate with one command:

    $ onos-app $OC1 install app/target/onos-restconf-provider-1.6.0-SNAPSHOT.oar
    $ onos-app $OC1 activate onos-restconf-provider

-----------------------------------------------------------------------------
##Version Information

TODO:  Future
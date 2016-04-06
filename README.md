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
The project currently is written to be built out-of-tree but is structured in such
a way as to easily overlay (with a bit of work) into the main ONOS source tree.  To build and
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


# RESTCONF Device States

Each devices that supports the RESTCONF protocol will exist in a particular state according to the
connectivity status and YANG models that it supports.


## Initial

A RESTCONF device is in the initial state immediately after the RestconfDeviceProvider has been notified of
its existence from either a CLI command, from a NetworkConfig JSON event notification, or reloaded from persistent
storage after a controller or restconf provider/driver restart.  This state is temporary and will typically not be
observable from the outside world.

Once the RESTCONF device object is created, it is verified not to be a duplicate, it will be registered with
the DeviceService and will transition to the Discovery state.

If the device is a duplicate, it will transition to the Final state where cleanup of any allocated resources
is performed and deleted.

## Discovery

In the discovery state, the RESTCONF provider attempts to connect the device. HTTP/HTTPS REST GET
commands will be used to discover the Root Resource directory, following redirects as required. If a
root resource directory is not discoverable, or the device is not able to be contacted, the device
will be placed in the Failed State with a reason of 'RESTCONF Root Resource directory not found'.

Note that during Root Resource discovery, redirect (3xx) messages will be handled appropriately for
the 3xx status received.

If the device root resource can be discovered and the RESTCONF datastore 'yang-library-version' is
located, the device transitions to the LibraryPopulation state.  If the 'yang-library-version' cannot
be discovered, the device transitions to the Failed state with a reason of 'YANG Library not found'.

If restoring a device from persistent storage, the RESTCONF Root Resource will be rediscovered even if
any previously discovered locations may have been the result of a Permanent Redirect (302 status) message.

If new device information is received via NetworkConfig JSON while the device is in any other state, it
will transition back to the discovery state.

## LibraryPopulation
TODO: Lots of work needed here

## TODO: more to come

## Teardown

## Final
This state is entered when a RESTCONF device needs to be deleted and any allocated resources released. It
is typically not visible to the outside world. A variety

---------------------------------------------------------------------------------------------------------
# Testing

To assist in the development of this provider, I created a python *mockDevice* flask program to
implement a mock RESTCONF device.

## Dependencies

Currently, the *mockDevice* depends up both the **flask** and **xrd** python packages.

## Runtime options

When ran on the command line with no options (*$ ./mockDevice*), the mock RESTCONF device will present
a single device accessible on any local IP address over port 8080.  This mock device should provide
a valid XRD response to a http://<ip-add>/.well-known/host-meta GET request that provides the RESTCONF
Root Resource Directory.  The Root Resource Directory API provides both required entry points (data and
operations) as well as the optional yang-library-version entry point.

Currently, only the implementation of the example Jukebox Library is provided but as this project
matures, I hope to add and support a few other standard (and more useful) YANG modules.

### JSON Configuration during runtime

To simplify repeatedly running unit tests, a JSON interface is provided on the test device to
allow you to programatically set/clear error conditions and other runtime options for the
test device

--verbose / -v          Output verbose information, default = False

--root_resource / -r    RESTCONF Root Resource, default = 'top/restconf'

--http_port / -p        HTTP Port number, default = 8080

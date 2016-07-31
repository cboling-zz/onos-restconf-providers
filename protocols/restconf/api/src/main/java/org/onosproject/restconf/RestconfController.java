/*
 * Copyright 2015 - 2016 Boling Consulting Solutions, bcsw.net
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.onosproject.restconf;

import org.onosproject.net.DeviceId;

import java.util.Map;

/**
 * Abstraction of an RESTCONF controller.
 *
 * Used to obtain RestconfDevice and (un)register listeners on RESTCONF device events.
 */
public interface RestconfController {

    /**
     * Adds Device Event Listener.
     *
     * @param listener node listener
     */
    void addDeviceListener(RestconfDeviceListener listener);

    /**
     * Removes Device Listener.
     *
     * @param listener node listener
     */
    void removeDeviceListener(RestconfDeviceListener listener);

    /**
     * Tries to connect to a specific RESTCONF device, if the connection is successful
     * it creates and adds the device to the ONOS core as a RestconfDevice.
     *
     * @param deviceId deviceId of the device to connect
     *
     * @return NetconfDevice Netconf device
     *
     * @throws RestconfException when device is not available
     */
    RestconfDevice connectDevice(DeviceId deviceId) throws RestconfException;

    /**
     * Disconnects a RESTCONF device and removes it from the core.
     *
     * @param deviceId id of the device to remove
     * @param remove   true if device is to be removed from core
     */
    void disconnectDevice(DeviceId deviceId, boolean remove);

    /**
     * Removes a RESTCONF device from the core.
     *
     * @param deviceId id of the device to remove
     */
    void removeDevice(DeviceId deviceId);

    /**
     * Gets all the nodes information.
     *
     * @return map of devices
     */
    Map<DeviceId, RestconfDevice> getDevicesMap();

    /**
     * Returns all devices known to this RESTCONF controller.
     * @return Iterable of RESTCONF devices
     */
    Iterable<RestconfDevice> getDevices();

    /**
     * Get a specific RESTCONF device
     *
     * @param id device ID
     *
     * @return Requested device or NULL if not found
     */
    RestconfDevice getDevice(DeviceId id);

    // TODO: These are being moved to the RestconfDevice interface

    /**
     * Create a RESTCONF device object
     *
     * @param devInfo
     *
     * @return
     */
    RestconfDevice createDevice(RestconfDeviceInfo devInfo);


    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Device ID
     * @param msg Message to send       // TODO: Come up with a message object to encaps this
     */
    void write(DeviceId id, Byte[] msg);

    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Device ID
     * @param msg Message to send     // TODO: Come up with a message object to encaps this
     */
    void processPacket(DeviceId id, Byte[] msg);
}

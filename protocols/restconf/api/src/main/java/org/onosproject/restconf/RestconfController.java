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

/**
 * Abstraction of an RESTCONF controller.
 *
 * Used to obtain RestconfDevice and (un)register listeners on RESTCONF device events.
 */
public interface RestconfController {

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
    RestconfDevice getDevice(String id);

    // TODO: These are being moved to the RestconfDevice interface

    /**
     * Adds Device Event Listener.
     *
     * @param listener node listener
     */
    @Deprecated
    void addDeviceListener(RestconfDeviceListener listener);

    // TODO: These are being moved to the RestconfDevice interface
    /**
     * Removes Device Listener.
     *
     * @param listener node listener
     */
    @Deprecated
    void removeDeviceListener(RestconfDeviceListener listener);


    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Devide ID
     * @param msg Message to send       // TODO: Come up with a message object to encaps this
     */
    void write(String id, Byte[] msg);

    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Devide ID
     * @param msg Message to send     // TODO: Come up with a message object to encaps this
     */
    void processPacket(String id, Byte[] msg);
}

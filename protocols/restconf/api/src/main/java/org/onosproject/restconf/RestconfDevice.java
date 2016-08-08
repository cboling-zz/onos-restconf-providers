/*
 * Copyright 2015-present Boling Consulting Solutions, bcsw.net
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

/**
 * RESTCONF Device interface
 */
public interface RestconfDevice {
    /**
     * Get the device ID for this RESTCONF device
     *
     * @return device ID
     */
    @Deprecated
    // TODO: Move to the RestconfDeviceInfo interface
    DeviceId getDeviceId();

    /**
     * Start the device state machine to begin the discover process.
     * <p>
     * This transitions the device into the 'DISCOVERY' state regardless of current state
     * unless already in the 'DISCOVERY' state.
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    void start();

    /**
     * Set the Administrative state of the device to either UP or DOWN
     * <p>
     * The default state for a device is UP which allows it to participate with this
     * provider over the RESTCONF protocol. You can place a device in the DOWN state
     * to disable the RESTCONF protocol as needed (during shutdown, to maintain it in a
     * standby mode, perform maintenance, ...)
     *
     * @param setAdminUp If true, the administrative state of the device will be placed in the
     *                   UP state.  Down otherwise.
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    void setAdminState(boolean setAdminUp);

    /**
     * Get the ADMIN state for this device
     *
     * @return current ADMIN UP state.  true = UP, false = down
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    boolean getAdminStateUp();

    /**
     * Get the current state of the device
     *
     * @return Device State
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    int getState();

    /**
     * Get the base URL for this device
     *
     * @return http[s]://<ip-addr>:<port>/
     */
    @Deprecated
    // TODO: Move to the RestconfDeviceInfo interface
    String getBaseURL();

    /**
     * Do we have connectivity to the device
     *
     * @return true if we can connect to the device
     */
    boolean isReachable();

    /**
     * Get reason the device is in the FAILED or INACTIVE state
     *
     * @return Failure reason (blank if not in a failed or inactive state)
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    String getFailureReason();

    /**
     * Returns a NETCONF session context for this device.
     *
     * @return netconf session
     */
    RestconfSession getSession();

    /**
     * Ensures that all sessions are closed.
     * A device cannot be used after disconnect is called.
     */
    void disconnect();

    /**
     * Get the initial connection information fro a device
     *
     * @return device info
     */
    RestconfDeviceInfo getDeviceInfo();

    /**
     * Writes the message to the driver.
     * <p>
     * Note: Messages may be silently dropped/lost due to IOExceptions or
     * role. If this is a concern, then a caller should use barriers.
     * </p>
     *
     * @param msg the message to write
     */
    @Deprecated
    // TODO: Move to the RestconfSession interface
    void sendMsg(Byte[] msg);
}

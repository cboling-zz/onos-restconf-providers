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

/**
 * RESTCONF Device interface
 */
public interface RestconfDevice {
    /**
     * Start the device state machine to begin the discover process.
     * <p>
     * This transitions the device into the 'DISCOVERY' state regardless of current state
     * unless already in the 'DISCOVERY' state.
     */
    void start();

    /**
     * Get the current state of the device
     *
     * @return Device State
     */
    int getState();

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

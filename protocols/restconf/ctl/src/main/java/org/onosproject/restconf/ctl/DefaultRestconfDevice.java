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
package org.onosproject.restconf.ctl;

import org.onosproject.net.DeviceId;
import org.onosproject.restconf.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

import static com.google.common.base.MoreObjects.toStringHelper;

/**
 * RESTCONF Device Implementation
 */
public class DefaultRestconfDevice implements RestconfDevice {

    public static final Logger log = LoggerFactory.getLogger(DefaultRestconfDevice.class);

    private RestconfDeviceInfo deviceInfo;
    private final DeviceId deviceId;
    private RestconfDeviceStateMachine stateMachine;
    private boolean isAdminUp;
    private RestconfSession restconfSession;

    /**
     * Constructor for a RESTCONF device
     *
     * @param deviceInfo Initial device information
     */
    public DefaultRestconfDevice(RestconfDeviceInfo deviceInfo) {
        this.isAdminUp = true;
        this.deviceInfo = deviceInfo;
        this.deviceId = deviceInfo.getDeviceId();
        this.stateMachine = new RestconfDeviceStateMachine(this);
    }

    /**
     * Get the device ID for this RESTCONF device
     *
     * @return device ID
     */
    @Override
    public DeviceId getDeviceId() {
        return deviceId;
    }

    /**
     * Get the initial connection information fro a device
     *
     * @return device info
     */
    @Override
    public RestconfDeviceInfo getDeviceInfo() {
        return deviceInfo;
    }

    /**
     * Get the current state of the device
     *
     * @return Device State
     */
    @Override
    public int getState() {
        return stateMachine.getState();
    }

    /**
     * Start the device state machine to begin the discover process
     *
     * This transitions the device into the 'DISCOVERY' state regardless of current state
     * unless already in the 'DISCOVERY' state.
     */
    @Override
    public void start() {
        // Transition the state machine to the initial 'DISCOVERY' state

        try {
            stateMachine.connect();
        } catch (RestconfDeviceStateMachineException ex) {
            log.error("Illegal start/restart of device state. Device: {], Message: {}",
                    deviceId.toString(), ex.toString());
        }
    }

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
    public void setAdminState(boolean setAdminUp) {

        if (setAdminUp != isAdminUp) {
            // TODO: Implement this.

            isAdminUp = setAdminUp;
        }
    }

    /**
     * Get the ADMIN state for this device
     *
     * @return current ADMIN UP state.  true = UP, false = down
     */
    public boolean getAdminStateUp() {
        return isAdminUp;
    }

    /**
     * Get the base URL for this device
     *
     * @return http[s]://<ip-addr>:<port>/
     */
    @Override
    public String getBaseURL() {
        boolean isSSL = deviceInfo.getTLS(); // TODO: Support SSL sometime with fallback (or preference for) plain-old TCP
        String moniker = isSSL ? "https" : "http";
        int port = deviceInfo.getPort();

        return String.format("%s://%s:%d/", moniker, deviceInfo.getIpAddress(), port);
    }

    /**
     * Connectivity test to remote device
     *
     * @param port Port number to try
     *
     * @return True if a Socket can be established
     */
    private boolean testConnection(int port) {
        RestconfDeviceInfo info = getDeviceInfo();
        String address = info.getIpAddress().toString();
        Socket socket = null;
        int timeout = info.getSocketTimeout();

        try {
            socket = new Socket();
            socket.connect(new InetSocketAddress(address, port), timeout);
            return socket.isConnected() && !socket.isClosed();

        } catch (IOException e) {
            log.info("Device {} is not reachable on port {}: {}", getDeviceId(),
                    port, e.toString());
            return false;
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    log.debug("Test Socket failed {} on port {}: {}", getDeviceId(), port,
                            e.toString());
                }
            }
        }
    }

    /**
     * Do we have connectivity to the device
     *
     * @return true if we can connect to the device
     */
    @Override
    public boolean isReachable() {
        switch (getState()) {
            case RestconfDeviceStateMachine.IDLE:
                return testConnection(getDeviceInfo().getPort());

            case RestconfDeviceStateMachine.DISCOVERY:
            case RestconfDeviceStateMachine.POPULATE:
            case RestconfDeviceStateMachine.ACTIVE:
                return true;

            case RestconfDeviceStateMachine.INACTIVE:
            case RestconfDeviceStateMachine.ERROR:
                return false;
        }
        return false;
    }

    /**
     * Get reason the device is in the FAILED or INACTIVE state
     *
     * @return Failure reason (blank if not in a failed or inactive state)
     */
    @Override
    public String getFailureReason() {
        return stateMachine.getFailureReason();
    }

    /**
     * Returns a NETCONF session context for this device.
     *
     * @return netconf session
     */
    @Override
    public RestconfSession getSession() {
        return restconfSession;
    }

    /**
     * Writes the message to the driver.
     * <p>
     * Note: Messages may be silently dropped/lost due to IOExceptions or
     * role. If this is a concern, then a caller should use barriers.
     * </p>
     *
     * @param msg the message to write
     */
    @Override
    public void sendMsg(Byte[] msg) {
        //TODO: Need to implement
    }

    @Override
    public int hashCode() {
        return deviceId.hashCode();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof DefaultRestconfDevice) {
            DefaultRestconfDevice otherDev = (DefaultRestconfDevice) obj;

            return deviceId.equals(otherDev.deviceId);
        }
        return false;
    }

    @Override
    public String toString() {
        return toStringHelper(this)
                .add("DeviceId", deviceId)
                .add("State", stateMachine.getStateAsText())
                .add("AdminStatus", isAdminUp ? "UP" : "DOWN")
                .toString();
    }
}

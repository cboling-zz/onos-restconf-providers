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
package org.onosproject.restconf.ctl;

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
    private RestconfDeviceStateMachine stateMachine;
    private RestconfSession restconfSession;

    /**
     * Constructor for a RESTCONF device
     *
     * @param deviceInfo Initial device information
     */
    public DefaultRestconfDevice(RestconfDeviceInfo deviceInfo) {
        this.deviceInfo = deviceInfo;
        this.stateMachine = new RestconfDeviceStateMachine(this);
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
                    getDeviceInfo().getDeviceId().toString(), ex.toString());
        }
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
            log.info("Device {} is not reachable on port {}: {}", getDeviceInfo().getDeviceId(),
                    port, e.toString());
            return false;
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    log.debug("Test Socket failed {} on port {}: {}",
                            getDeviceInfo().getDeviceId(), port, e.toString());
                }
            }
        }
    }

    /**
     * Do we have connectivity to the device
     *
     * TODO: If we are running connectionless, may need another state and more logic here for that case
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
     * Ensures that all sessions are closed.
     * A device cannot be used after disconnect is called.
     */
    @Override
    public void disconnect() {
        // TODO: Implement this
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
        return getDeviceInfo().hashCode();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof DefaultRestconfDevice) {
            DefaultRestconfDevice otherDev = (DefaultRestconfDevice) obj;

            return getDeviceInfo().getDeviceId().equals(otherDev.getDeviceInfo().getDeviceId());
        }
        return false;
    }

    @Override
    public String toString() {
        return toStringHelper(this)
                .add("DeviceId", getDeviceInfo().getDeviceId())
                .add("State", stateMachine.getStateAsText())
                .add("AdminStatus", deviceInfo.getAdminStateUp() ? "UP" : "DOWN")
                .toString();
    }
}

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

import org.onlab.packet.IpAddress;
import org.onosproject.net.DeviceId;
import org.onosproject.restconf.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.URI;

/**
 * Created by cboling on 3/24/16.
 */
public class DefaultRestconfDevice implements RestconfDevice {

    public static final Logger log = LoggerFactory
            .getLogger(DefaultRestconfDevice.class);

    private RestconfDeviceInfo deviceInfo;
    private final RestId restId;
    private RestconfDeviceStateMachine stateMachine;

    public DefaultRestconfDevice(RestconfDeviceInfo deviceInfo) {
        this.deviceInfo = deviceInfo;
        this.restId = deviceInfo.getRestconfId();
        this.stateMachine = new RestconfDeviceStateMachine(DeviceId.deviceId(RestId.uri(restId)));
    }

    /**
     * Get the device ID for this RESTCONF device
     *
     * @return device ID
     */
    public DeviceId getDeviceId() {
        return DeviceId.deviceId(RestId.uri(restId));
    }

    /**
     * Get the RESTCONF ID for this device
     *
     * @return RESTCONF specific ID
     */
    public RestId getRestconfId() {
        return restId;
    }

    /**
     * Get the initial connection information fro a device
     *
     * @return device info
     */
    public RestconfDeviceInfo getDeviceInfo() {
        return deviceInfo;
    }

    /**
     * Get the current state of the device
     *
     * @return Device State
     */
    public int getState() {
        return stateMachine.getState();
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
                    return false;
                }
            }
        }
    }

    /**
     * Do we have connectivity to the device
     *
     * @return true if we can connect to the device
     */
    public boolean isReachable() {
        switch (getState()) {
            case RestconfDeviceStateMachine.IDLE:
                return testConnection(getDeviceInfo().getSslPort()) ||
                        testConnection(getDeviceInfo().getTcpPort());

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
    public String getFailureReason() {
        return stateMachine.getFailureReason();
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
    public void sendMsg(Byte[] msg) {
        //TODO: Need to implement
    }
}

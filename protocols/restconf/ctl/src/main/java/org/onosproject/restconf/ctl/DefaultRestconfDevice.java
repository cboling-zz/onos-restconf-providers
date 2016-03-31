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

import java.net.URI;

/**
 * Created by cboling on 3/24/16.
 */
public class DefaultRestconfDevice implements RestconfDevice {

    public static final Logger log = LoggerFactory
            .getLogger(DefaultRestconfDevice.class);

    private RestconfDeviceInfo deviceInfo;
    private final RestId restId;
    private State state = State.INITIAL;
    private String failureReason = "";

    public DefaultRestconfDevice(RestconfDeviceInfo deviceInfo) {
        this.deviceInfo = deviceInfo;
        this.restId = deviceInfo.getRestconfId();
    }
//
//    /**
//     * Registers a listener for RESTCONF events.
//     *
//     * @param listener the listener to notify
//     */
//    public void addEventListener(RestconfDeviceListener listener) {
//
//        //TODO: Need to implement
//    }
//
//    /**
//     * Unregisters a listener.
//     *
//     * @param listener the listener to unregister
//     */
//    public void removeEventListener(RestconfDeviceListener listener) {
//
//        //TODO: Need to implement
//    }

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
    public State getState() {
        return state;
    }

    /**
     * Transition the device to a new state
     *
     * @param newState new State
     *
     * @throws RestconfException
     */
    public void setState(State newState) throws RestconfException {
        // TODO: Code this as a state machine, but for now, use a nasty set of if/switches

        switch (state) {
            case INITIAL:
                // Only support transition to discovery

                if (newState != State.DISCOVERY) {
                    throw new RestconfException("Invalid state transistion");
                }
                throw new RestconfException("TODO: Not yet implemented");

            case DISCOVERY:
                throw new RestconfException("TODO: Not yet implemented");

            case LIBRARY_POPULATE:
                throw new RestconfException("TODO: Not yet implemented");

            case ACTIVE:
                throw new RestconfException("TODO: Not yet implemented");

            case INACTIVE:
                throw new RestconfException("TODO: Not yet implemented");

            case FAILED:
                throw new RestconfException("TODO: Not yet implemented");
        }
    }

    /**
     * Do we have connectivity to the device
     *
     * @return true if we can connect to the device
     */
    public boolean isReachable() {
        switch (state) {
            case INITIAL:
            case DISCOVERY:
            case INACTIVE:
            case FAILED:
                return false;
        }
        // TODO: Implement for the LIBRARY_POPULATE/ACTIVE States

        return false;
    }

    /**
     * Get reason the device is in the FAILED or INACTIVE state
     *
     * @return Failure reason (blank if not in a failed or inactive state)
     */
    public String getFailureReason() {
        return failureReason;
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

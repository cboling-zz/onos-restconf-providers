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
 * Created by cboling on 3/24/16.
 */
public interface RestconfDevice {

    /**
     * Representation of the RESTCONF device state
     */
    enum State {
        /**
         * Initial (temporary) state of the device that occurs just after the device
         * is created by CLI/NetConfig JSON or is being restored from persistent
         * storage after a Control or RESTCONF protocol driver reset.
         */
        INITIAL,

        /**
         *
         */
        DISCOVERY,

        /**
         *
         */
        LIBRARY_POPULATE,

        /**
         *
         */
        ACTIVE,

        /**
         *
         */
        INACTIVE,

        /**
         *
         */
        FAILED
    }
    /**
     * Registers a listener for RESTCONF events.
     *
     * @param listener the listener to notify
     */
    void addEventListener(RestconfDeviceListener listener);

    /**
     * Unregisters a listener.
     *
     * @param listener the listener to unregister
     */
    void removeEventListener(RestconfDeviceListener listener);

    /***
     * Get the current state of the device
     *
     * @return Device State
     */
    State getState();

    /**
     * Get reason the device is in the FAILED or INACTIVE state
     *
     * @return Failure reason (blank if not in a failed or inactive state)
     */
    String getFailureReason();


    /**
     * Writes the message to the driver.
     * <p>
     * Note: Messages may be silently dropped/lost due to IOExceptions or
     * role. If this is a concern, then a caller should use barriers.
     * </p>
     *
     * @param msg the message to write
     */
    void sendMsg(Byte[] msg);
}

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

import org.onosproject.event.AbstractEvent;

import java.util.Optional;

/**
 * Describes RESTCONF network configuration event.
 */
public class RestconfDeviceOutputEvent extends
        AbstractEvent<RestconfDeviceOutputEvent.Type, Object> {

    private final String messagePayload;
    private final Optional<Integer> messageID;
    private final RestconfDeviceInfo deviceInfo;

    /**
     * Type of network configuration events.
     */
    public enum Type {
        /**
         * Signifies that sent a reply to a request.
         */
        DEVICE_REPLY,

        /**
         * Signifies that the device sent a notification.
         */
        DEVICE_NOTIFICATION,

        /**
         * Signifies that the device is not reachable.
         */
        DEVICE_UNREGISTERED,

        /**
         * Signifies that the device has encountered an error.
         */
        DEVICE_ERROR,
    }

    /**
     * Creates an event of a given type and for the specified subject and the
     * current time.
     *
     * @param type       event type
     * @param subject    event subject
     * @param payload    message from the device
     * @param msgID      id of the message related to the event
     * @param deviceInfo device of event
     */
    public RestconfDeviceOutputEvent(Type type, Object subject, String payload,
                                     Optional<Integer> msgID,
                                     RestconfDeviceInfo deviceInfo) {
        super(type, subject);
        messagePayload = payload;
        this.messageID = msgID;
        this.deviceInfo = deviceInfo;
    }

    /**
     * Creates an event of a given type and for the specified subject and time.
     *
     * @param type       event type
     * @param subject    event subject
     * @param payload    message from the device
     * @param msgID      id of the message related to the event
     * @param deviceInfo device of event
     * @param time       occurrence time
     */
    public RestconfDeviceOutputEvent(Type type, Object subject, String payload,
                                     Optional<Integer> msgID,
                                     RestconfDeviceInfo deviceInfo,
                                     long time) {
        super(type, subject, time);
        messagePayload = payload;
        this.deviceInfo = deviceInfo;
        this.messageID = msgID;
    }

    /**
     * return the message payload of the reply form the device.
     *
     * @return reply
     */
    public String getMessagePayload() {
        return messagePayload;
    }

    /**
     * Event-related device information.
     *
     * @return information about the device
     */
    public RestconfDeviceInfo getDeviceInfo() {
        return deviceInfo;
    }

    /**
     * Reply messageId.
     *
     * @return messageId
     */
    public Optional<Integer> getMessageID() {
        return messageID;
    }
}

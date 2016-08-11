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

import com.google.common.annotations.Beta;
import org.onosproject.restconf.RestconfDeviceOutputEventListener;

import java.util.concurrent.CompletableFuture;

/**
 * Interface to represent an object that does all the I/O on a RESTCONF session
 * with the associated RESTConf device.
 *
 * TODO: Initially support one thread per session but plan for multisession support
 */
public interface RestconfStreamHandler {
    /**
     * Sends the request on the stream that is used to communicate to and from the device.
     * <p>
     * TODO: Modify this to better support Netty async HTTP client
     *
     * @param request request to send to the physical device
     *
     * @return a CompletableFuture of type String that will contain the response for the request.
     */
    CompletableFuture<String> sendMessage(String request);

    /**
     * Adds a listener for RESTConf events on the handled stream.
     *
     * @param listener RESTConf device event listener
     */
    void addDeviceEventListener(RestconfDeviceOutputEventListener listener);

    /**
     * Removes a listener for RESTConf events on the handled stream.
     *
     * @param listener RESTConf device event listener
     */
    void removeDeviceEventListener(RestconfDeviceOutputEventListener listener);

    // TODO: Notification support not in very first release/beta
//    @Beta
//    /**
//     * Sets instance variable that when true allows receipt of notifications.
//     *
//     * @param enableNotifications if true, allows action based off notifications
//     *                             else, stops action based off notifications
//     */
//    void setEnableNotifications(boolean enableNotifications);
}

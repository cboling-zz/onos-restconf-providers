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

import org.onosproject.restconf.RestconfDeviceOutputEventListener;

import java.util.concurrent.CompletableFuture;

/**
 * Thread that gets spawned each time a session is established and handles all the input
 * and output from the session's streams to and from the RESTCONF device the session is
 * established with.
 *
 * TODO: Initially support one thread per session but plan for multisession support
 * TODO: When multisession, have a max session limit per RestconfStreamThread
 */
public class RestconfStreamThread extends Thread implements RestconfStreamHandler {

    /**
     * Main thread entry point
     */
    public void run() {
        // TODO: Implement this

    }

    /**
     * Sends the request on the stream that is used to communicate to and from the device.
     * <p>
     * TODO: Modify this to better support Netty async HTTP client
     *
     * @param request request to send to the physical device
     *
     * @return a CompletableFuture of type String that will contain the response for the request.
     */
    @Override
    public CompletableFuture<String> sendMessage(String request) {

        // TODO: Implement this

        return null;
    }

    /**
     * Adds a listener for RESTConf events on the handled stream.
     *
     * @param listener RESTConf device event listener
     */
    @Override
    public void addDeviceEventListener(RestconfDeviceOutputEventListener listener) {

        // TODO: Implement this
    }

    /**
     * Removes a listener for RESTConf events on the handled stream.
     *
     * @param listener RESTConf device event listener
     */
    @Override
    public void removeDeviceEventListener(RestconfDeviceOutputEventListener listener) {

        // TODO: Implement this
    }
}

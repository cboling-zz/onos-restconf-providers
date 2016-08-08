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
import org.onosproject.restconf.RestconfException;
import org.onosproject.restconf.RestconfSession;

/**
 * RESTConf session object that allows RESTConf operations on top with the physical
 * device on top of an http or https connection.
 *
 *
 * TODO: This class is expected to change significantly once we get past discover
 *       and want to do real work.
 */
public class RestconfSessionImpl implements RestconfSession {

    public RestconfSessionImpl() {
        // TODO: Implement me
    }

    /**
     * Retrieves the requested data.
     *
     * @param request the XML or JSON containing the request to the server
     * @param headers Optional array of HTTP headers for the request
     * @param withDefaultsMode with-defaults mode
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String get(String request, String[] headers, String withDefaultsMode)
            throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Create the requested data or invoke an operation resource
     *
     * @param request the XML or JSON containing the request to the server
     * @param headers Optional array of HTTP headers for the request
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String post(String request, String[] headers) throws RestconfException {
        // TODO: Implement this
        return "";
    }

    /**
     * Create or replace the target data resource
     *
     * @param request the XML or JSON containing the request to the server
     * @param headers Optional array of HTTP headers for the request
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String put(String request, String[] headers) throws RestconfException {
        // TODO: Implement this
        return "";
    }

    /**
     * Replace portions of the target data resource
     *
     * @param request the XML or JSON containing the request to the server
     * @param headers Optional array of HTTP headers for the request
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String patch(String request, String[] headers) throws RestconfException {
        // TODO: Implement this
        return "";
    }

    /**
     * Delete the target data resource
     *
     * @param request the XML or JSON containing the request to the server
     * @param headers Optional array of HTTP headers for the request
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String delete(String request, String[] headers) throws RestconfException {
        // TODO: Implement this
        return "";
    }

    /**
     * Starts subscription to the device's notifications.
     *
     * @param request the XML or JSON containing the request to the server
     *
     * @throws RestconfException when there is a problem starting the subscription
     */
    @Override
    public void startSubscription(String request) throws RestconfException {
        // TODO: Implement this

    }

    /**
     * Ends a specific subscription to the device's notifications.
     *
     * @param request the XML or JSON containing the request to the server
     *
     * @throws RestconfException when there is a problem ending the subscription
     */
    @Override
    public void endSubscription(String request) throws RestconfException {
        // TODO: Implement this

    }

    /**
     * Ends all subscriptions to the device's notifications.
     *
     * @throws RestconfException when there is a problem ending the subscription
     */
    @Override
    public void endAllSubscriptions() throws RestconfException {
        // TODO: Implement this

    }

    /**
     * Closes the RESTCONF session with the device.
     * the first time it tries gracefully, then kills it forcefully
     *
     * @return true if closed
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public boolean close() throws RestconfException {
        // TODO: Implement this
        return false;
    }

    /**
     * Gets the session ID of the Netconf session.
     *
     * @return Session ID as a string.
     */
    @Override
    public String getSessionId() {
        // TODO: Implement this
        return "";
    }

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    @Override
    public void addDeviceOutputListener(RestconfDeviceOutputEventListener listener) {
        // TODO: Implement this
    }

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    @Override
    public void removeDeviceOutputListener(RestconfDeviceOutputEventListener listener) {
        // TODO: Implement this
    }
}

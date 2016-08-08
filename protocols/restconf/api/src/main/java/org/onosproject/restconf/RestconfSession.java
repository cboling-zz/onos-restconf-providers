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
import com.google.common.annotations.Beta;
import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * RESTConf session object that allows RESTConf operations on top with the physical
 * device on top of an http or https connection.
 *
 *
 * TODO: This class is expected to change significantly once we get past discover
 *       and want to do real work.
 */
public interface RestconfSession {

    // TODO: Only support synchronous operations in the GET/POST/PATCH of normal operations
    //       until working well enough to do it for other applications.  The State Machine
    //       and initial discover should be the first test of async operations.

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
    String get(String request, String[] headers, String withDefaultsMode)
            throws RestconfException;

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
    String post(String request, String[] headers) throws RestconfException;

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
    String put(String request, String[] headers) throws RestconfException;

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
    String patch(String request, String[] headers) throws RestconfException;

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
    String delete(String request, String[] headers) throws RestconfException;

    /**
     * Starts subscription to the device's notifications.
     *
     * @param request the XML or JSON containing the request to the server
     *
     * @throws RestconfException when there is a problem starting the subscription
     */
    void startSubscription(String request) throws RestconfException;

    /**
     * Ends a specific subscription to the device's notifications.
     *
     * @param request the XML or JSON containing the request to the server
     *
     * @throws RestconfException when there is a problem ending the subscription
     */
    void endSubscription(String request) throws RestconfException;

    /**
     * Ends all subscriptions to the device's notifications.
     *
     * @throws RestconfException when there is a problem ending the subscription
     */
    void endAllSubscriptions() throws RestconfException;

    /**
     * Closes the RESTCONF session with the device.
     * the first time it tries gracefully, then kills it forcefully
     *
     * @return true if closed
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    boolean close() throws RestconfException;

    /**
     * Gets the session ID of the Netconf session.
     *
     * @return Session ID as a string.
     */
    String getSessionId();

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    void addDeviceOutputListener(RestconfDeviceOutputEventListener listener);

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    void removeDeviceOutputListener(RestconfDeviceOutputEventListener listener);

}

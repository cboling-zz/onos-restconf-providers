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

import org.onosproject.restconf.RestconfDeviceOutputEventListener;
import org.onosproject.restconf.RestconfException;
import org.onosproject.restconf.RestconfSession;

/**
 * Created by cboling on 3/24/16.
 */
public class RestconfSessionImpl implements RestconfSession {

    public RestconfSessionImpl() {
        // TODO: Implement me
    }

    /**
     * Retrives the requested configuration, different from get-config.
     *
     * @param request the XML containing the request to the server.
     *
     * @return device running configuration
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String get(String request) throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Retrives the requested data.
     *
     * @param filterSchema     XML subtrees to include in the reply
     * @param withDefaultsMode with-defaults mode
     *
     * @return Server response
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String get(String filterSchema, String withDefaultsMode)
            throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Executes an synchronous RPC to the server.
     *
     * @param request the XML/JSON containing the RPC for the server.
     *
     * @return Server response or ERROR
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String requestSync(String request) throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Retrives the specified configuration.
     *
     * @return configuration.
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String getConfig() throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Retrieves part of the specivied configuration based on the filterSchema.
     *
     * @param configurationFilterSchema XML schema to filter the configuration
     *                                  elements we are interested in
     *
     * @return device running configuration.
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public String getConfig(String configurationFilterSchema)
            throws RestconfException {
        // TODO: Implement me
        return "";
    }

    /**
     * Retrieves part of the specified configuration based on the filterSchema.
     *
     * @param newConfiguration configuration to set
     *
     * @return true if the configuration was edited correctly
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public boolean editConfig(String newConfiguration) throws RestconfException {
        // TODO: Implement me
        return false;
    }

    /**
     * Retrives part of the specified configuration based on the filterSchema.
     *
     * @param mode             selected mode to change the configuration
     * @param newConfiguration configuration to set
     *
     * @return true if the configuration was edited correctly
     *
     * @throws RestconfException when there is a problem in the communication process on
     *                           the underlying connection
     */
    @Override
    public boolean editConfig(String mode, String newConfiguration)
            throws RestconfException {
        // TODO: Implement me

        return false;
    }

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    @Override
    public void addDeviceOutputListener(RestconfDeviceOutputEventListener listener) {
        // TODO: Implement me
    }

    /**
     * Remove a listener from the underlying stream handler implementation.
     *
     * @param listener event listener.
     */
    @Override
    public void removeDeviceOutputListener(RestconfDeviceOutputEventListener listener) {
        // TODO: Implement me
    }
}

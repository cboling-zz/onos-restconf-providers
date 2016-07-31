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
 */
public interface RestconfSession {


    /**
     * Retrives the requested configuration, different from get-config.
     *
     * @param request the XML containing the request to the server.
     * @return device running configuration
     * @throws RestconfException when there is a problem in the communication process on
     * the underlying connection
     */
    String get(String request) throws RestconfException;

    /**
     * Retrives the requested data.
     *
     * @param filterSchema XML subtrees to include in the reply
     * @param withDefaultsMode with-defaults mode
     * @return Server response
     * @throws RestconfException when there is a problem in the communication process on
     * the underlying connection
     */
    String get(String filterSchema, String withDefaultsMode)
            throws RestconfException;

    /**
     * Retrives the specified configuration.
     *
     * @return configuration.
     * @throws RestconfException when there is a problem in the communication process on
     * the underlying connection
     */
    String getConfig() throws RestconfException;

    /**
     * Retrives part of the specivied configuration based on the filterSchema.
     *
     * @param configurationFilterSchema XML schema to filter the configuration
     *                                  elements we are interested in
     * @return device running configuration.
     * @throws RestconfException when there is a problem in the communication process on
     * the underlying connection
     */
    String getConfig(String configurationFilterSchema)
            throws RestconfException;

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

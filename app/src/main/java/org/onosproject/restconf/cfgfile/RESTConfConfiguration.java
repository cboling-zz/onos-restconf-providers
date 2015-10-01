/*
 * Copyright 2015 Boling Consulting Solutions, bcsw.net
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
package org.onosproject.restconf.cfgfile;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * JSON RESTConfConfiguration file support
 */
public class RESTConfConfiguration {

    /////////////////////////////////////////////////////////////////////////
    // Constants / Defaults

    static final int DEFAULT_WORKER_THREADS = 1;
    static final int DEFAULT_EVENT_INTERVAL = 5;
    static final int DEFAULT_CONN_TIMEOUT = 45 * 1000;

    static final int DEFAULT_SSL_PORT = 443;
    static final int DEFAULT_TCP_PORT = 80;

    static final String DEFAULT_XML_MEDIA_TYPE = "xml";
    static final String DEFAULT_JSON_MEDIA_TYPE = "json";

    static final String DEFAULT_API_ROOT = "/restconf";

    /////////////////////////////////////////////////////////////////////////
    // Properites

    private final int numThreads;
    private final int connectionTimeout;
    private final int eventInterval;
    private final List<RESTConfDeviceEntry> devices;

    /**
     * Default constructor.
     */
    private RESTConfConfiguration() {
        eventInterval = DEFAULT_EVENT_INTERVAL;
        connectionTimeout = DEFAULT_CONN_TIMEOUT;
        numThreads = DEFAULT_WORKER_THREADS;
        devices = new ArrayList<>();
    }

    @JsonCreator
    public RESTConfConfiguration(@JsonProperty("eventInterval")
                                 Integer interval,
                                 @JsonProperty("connectionTimeout")
                                 Integer timeout,
                                 @JsonProperty("numThreads")
                                 Integer workers,
                                 @JsonProperty("devices")
                                 List<RESTConfDeviceEntry> devs) {
        eventInterval = interval;
        connectionTimeout = timeout;
        numThreads = workers;
        devices = devs;
    }

    /**
     * Get the number of worker threads to use for background processing
     *
     * @return Number of threads
     */
    public int getNumThreads() {
        return numThreads;
    }

    /**
     * Get the interval between network queries
     *
     * @return Interval in milliseconds
     */
    public int getEventInterval() {
        return connectionTimeout;
    }

    /**
     * Get the timeout for network requests to RESTConf devices
     *
     * @return timeout in milliseconds
     */
    public int getConnectionTimeout() {
        return eventInterval;
    }

    /**
     * Get a list of RESTConf devices
     *
     * @return a list of RESTConf devices
     */
    public List<RESTConfDeviceEntry> getDevices() {
        return Collections.unmodifiableList(devices);
    }
}

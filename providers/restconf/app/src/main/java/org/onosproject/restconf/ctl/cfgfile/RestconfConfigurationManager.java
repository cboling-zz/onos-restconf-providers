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
package org.onosproject.restconf.ctl.cfgfile;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Provides for configuration restoration from JSON configuration file
 */
@Component(immediate = true)
@Service
public class RestconfConfigurationManager implements RestconfConfigurationService {
    private static final String CONFIG_DIR = "../config";

    //////////////////////////////////////////////////////////////////////
    // Constants
    private static final String DEFAULT_CONFIG_FILE = "restconf.json";
    private final Logger log = LoggerFactory.getLogger(getClass());
    private String configFileName = DEFAULT_CONFIG_FILE;

    //////////////////////////////////////////////////////////////////////
    // Class data

    private Integer numThreads = RestconfConfiguration.DEFAULT_WORKER_THREADS;
    private Integer eventInterval = RestconfConfiguration.DEFAULT_EVENT_INTERVAL;
    private Integer connectionTimeout = RestconfConfiguration.DEFAULT_CONN_TIMEOUT;

    /**
     * Collection of RESTConf Devide entries
     */
    private List<RestconfDeviceEntry> deviceEntries = new CopyOnWriteArrayList<>();

    //////////////////////////////////////////////////////////////////////

    @Activate
    protected void activate() {
        readConfiguration();
        log.info("Started");
    }

    @Deactivate
    protected void deactivate() {
        log.info("Stopped");
    }

    /**
     * Instructs the configuration reader to read the configuration from the
     * file.
     */
    public void readConfiguration() {
        readConfiguration(configFileName);
    }

    /**
     * Reads RESTConf devices and settings contained in configuration file.
     *
     * @param configFilename the name of the configuration file
     */
    private void readConfiguration(String configFilename) {
        File configFile = new File(CONFIG_DIR, configFilename);
        ObjectMapper mapper = new ObjectMapper();

        try {
            log.info("Loading config: {}", configFile.getAbsolutePath());
            RestconfConfiguration config = mapper.readValue(configFile, RestconfConfiguration.class);

            numThreads = config.getNumThreads();
            eventInterval = config.getEventInterval();
            connectionTimeout = config.getConnectionTimeout();
            deviceEntries = config.getDevices();

        } catch (FileNotFoundException e) {
            log.warn("RestconfConfiguration file not found: {}", configFileName);
        } catch (IOException e) {
            log.error("Error loading configuration", e);
        }
        // TODO: Add validation code here.
    }

    /**
     * Get the number of worker threads to use for background processing
     *
     * @return Number of threads
     */
    @Override
    public Integer getNumberOfWorkerThreads() {
        return numThreads;
    }

    /**
     * Get the interval between network queries
     *
     * @return Interval in milliseconds
     */
    @Override
    public Integer getEventInterval() {
        return eventInterval;
    }

    /**
     * Get the timeout for network requests to RESTConf devices
     *
     * @return timeout in milliseconds
     */
    @Override
    public Integer getConnectionTimeout() {
        return connectionTimeout;
    }

    /**
     * Get a list of RESTConf devices
     *
     * @return a list of RESTConf devices
     */
    @Override
    public List<RestconfDeviceEntry> getDevices() {
        return deviceEntries;
    }
}

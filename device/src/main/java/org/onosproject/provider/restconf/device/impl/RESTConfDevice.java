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
package org.onosproject.provider.restconf.device.impl;

import org.slf4j.Logger;

import java.util.Date;

import static com.google.common.base.Preconditions.checkNotNull;
import static org.slf4j.LoggerFactory.getLogger;

/**
 * This is a logical representation of actual RESTConf device, carrying all the
 * necessary information to connect and execute RESTConf operations.
 */
public class RESTConfDevice {
    // TODO: Store these in distributed store (eventually consistent) and provide ability to change
    //       via CLI, REST, and JSON Configuration File
    // TODO: Move defaults to 'app.configuration'

    private static final int DEFAULT_URL_UPDATE_TIMEOUT = (24 * 3600 * 1000); // One Day
    private static final int DEFAULT_DEVICE_UPDATE_TIMEOUT = (15 * 60 * 1000);   // Fifteen minutes
    private static final int DEFAULT_TIME_SKEW_PERCENT = 5;                  // 5% skew
    private final Logger log = getLogger(RESTConfDevice.class);
    // Connection information to device
    private String url;                 // Encoded URL
    private String servicesUrl;
    private String username;
    private String password;

    private Date lastUrlUpdate;         // (UTC) last time URL location was discovered
    private Date lastDeviceUpdate;      // (UTC) last time device was contacted

    // (mS) time between URL discoveries (<= 0 == never)
    private int urlUpdateTimeout = DEFAULT_URL_UPDATE_TIMEOUT;
    // (mS) time between updates (<= 0 == never)
    private int deviceUpdateTimeout = DEFAULT_DEVICE_UPDATE_TIMEOUT;

    protected RESTConfDevice(String deviceUrl, String user, String password) {
        this.url = checkNotNull(deviceUrl, "RESTConf Device URL Cannot be null");
        this.username = user;
        this.password = password;
    }
}
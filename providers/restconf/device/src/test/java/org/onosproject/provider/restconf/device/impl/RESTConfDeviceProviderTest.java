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

import org.junit.After;
import org.junit.Before;
import org.slf4j.Logger;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Test Case to Validate RESTCONF Device Provider.
 */
public class RESTConfDeviceProviderTest {
    private final Logger log = getLogger(RESTConfDeviceProviderTest.class);

    @Before
    public void setUp() {
        log.info("setup");
    }

    @After
    public void tearDown() {
        log.info("tear down");
    }
}

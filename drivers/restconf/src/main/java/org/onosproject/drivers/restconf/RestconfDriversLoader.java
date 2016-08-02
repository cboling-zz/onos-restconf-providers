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

package org.onosproject.drivers.restconf;

import org.apache.felix.scr.annotations.Component;
import org.onosproject.net.driver.AbstractDriverLoader;
import org.slf4j.Logger;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Loader for RESTconf device drivers.
 */
@Component(immediate = true)
public class RestconfDriversLoader extends AbstractDriverLoader {
    private final Logger log = getLogger(RestconfControllerConfig.class);

    private static String DRIVER_DEFINITION_RESOURCE_PATH = "/restconf-drivers.xml";

    public RestconfDriversLoader() {
        super(DRIVER_DEFINITION_RESOURCE_PATH);

        log.debug("RestconfDriversLoader has been created. Resource Path: {}",
                DRIVER_DEFINITION_RESOURCE_PATH);
    }
}

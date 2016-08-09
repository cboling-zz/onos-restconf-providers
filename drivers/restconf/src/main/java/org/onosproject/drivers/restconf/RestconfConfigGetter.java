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

import com.google.common.base.Preconditions;
import org.onosproject.net.DeviceId;
import org.onosproject.net.behaviour.ConfigGetter;
import org.onosproject.net.driver.AbstractHandlerBehaviour;
import org.onosproject.net.driver.DriverHandler;
import org.onosproject.restconf.RestconfController;
import org.slf4j.Logger;

import java.io.IOException;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Gets the configuration of the specified type from the specified device. If a
 * failure occurs it returns the error string found in UNABLE_TO_READ_CONFIG.
 * This is a temporary development tool for use until YANG integration is complete.
 * This is not a properly specified behavior implementation. DO NOT USE AS AN EXAMPLE.
 */
//FIXME this should eventually be removed.

public class RestconfConfigGetter extends AbstractHandlerBehaviour
        implements ConfigGetter {

    private final Logger log = getLogger(getClass());

    //FIXME the error string should be universal for all implementations of
    // ConfigGetter
    public static final String UNABLE_TO_READ_CONFIG = "config retrieval error";

    /**
     * Behaviour that gets the configuration of the specified type from the device
     *
     * @param unused Not currently used.  Needed to keep interface happy
     *
     * @return Returns the string representation of a device configuration, returns a
     * failure string if the configuration cannot be retrieved.
     */
    @Override
    public String getConfiguration(String unused) {
        DriverHandler handler = handler();
        RestconfController controller = handler.get(RestconfController.class);
        DeviceId ofDeviceId = handler.data().deviceId();
        Preconditions.checkNotNull(controller, "RESTconf controller is null");

        log.debug("getControllers: entry");

//        try {
        return "";      // TODO: Implement this
//            return controller.getDevicesMap().
//                    get(ofDeviceId).
//                    getSession().
//                    getConfig();
//        } catch (IOException e) {
//            log.error("Configuration could not be retrieved {}",
//                    e.getMessage());
//        }
//        return UNABLE_TO_READ_CONFIG;
    }

}

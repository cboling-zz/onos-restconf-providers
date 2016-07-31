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
import org.onosproject.drivers.utilities.XmlConfigParser;
import org.onosproject.mastership.MastershipService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.behaviour.ControllerConfig;
import org.onosproject.net.behaviour.ControllerInfo;
import org.onosproject.net.driver.AbstractHandlerBehaviour;
import org.onosproject.net.driver.DriverHandler;
import org.onosproject.restconf.RestconfController;
import org.onosproject.restconf.RestconfDevice;
import org.slf4j.Logger;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Implementation of controller config which allows to get and set controllers
 * through the Netconf protocol.
 */
public class RestconfControllerConfig extends AbstractHandlerBehaviour
        implements ControllerConfig {

    private final Logger log = getLogger(RestconfControllerConfig.class);


    @Override
    public List<ControllerInfo> getControllers() {
        DriverHandler handler = handler();
        RestconfController controller = handler.get(RestconfController.class);
        MastershipService mastershipService = handler.get(MastershipService.class);
        DeviceId deviceId = handler.data().deviceId();
        Preconditions.checkNotNull(controller, "RESTconf controller is null");
        List<ControllerInfo> controllers = new ArrayList<>();
        if (mastershipService.isLocalMaster(deviceId)) {
//            try {
//                // TODO: Need to implement this
//                String reply = controller.getDevice(restId).getSession().
//                        getConfig("running");
//                log.debug("Reply XML {}", reply);
//                controllers.addAll(XmlConfigParser.parseStreamControllers(XmlConfigParser.
//                        loadXml(new ByteArrayInputStream(reply.getBytes(StandardCharsets.UTF_8)))));
//            } catch (IOException e) {
//                log.error("Cannot communicate with device {} ", deviceId, e);
//            }
        } else {
            log.warn("I'm not master for {} please use master, {} to execute command",
                    deviceId,
                    mastershipService.getMasterFor(deviceId));
        }
        return controllers;
    }

    @Override
    public void setControllers(List<ControllerInfo> controllers) {
        DriverHandler handler = handler();
        RestconfController controller = handler.get(RestconfController.class);
        DeviceId deviceId = handler.data().deviceId();
        Preconditions.checkNotNull(controller, "RESTconf controller is null");
        MastershipService mastershipService = handler.get(MastershipService.class);
        if (mastershipService.isLocalMaster(deviceId)) {
            try {
                RestconfDevice device = controller.getDevice(deviceId);
                String config = null;

//                try {
//                    //TODO Need to implement this
//                    String reply = device.getSession().getConfig("running");
//                    log.info("reply XML {}", reply);
//                    config = XmlConfigParser.createControllersConfig(
//                            XmlConfigParser.loadXml(getClass().getResourceAsStream("controllers.xml")),
//                            XmlConfigParser.loadXml(
//                                    new ByteArrayInputStream(reply.getBytes(StandardCharsets.UTF_8))),
//                            "running", "merge", "create", controllers
//                    );
//                } catch (IOException e) {
//                    log.error("Cannot communicate to device {} , exception {}", deviceId, e.getMessage());
//                }
//                // TODO IMplement this
//                device.getSession().editConfig(config.substring(config.indexOf("-->") + 3));
            } catch (NullPointerException e) {
                log.warn("No RESTCONF device with requested parameters " + e);
                throw new NullPointerException("No RESTCONF device with requested parameters " + e);
//            } catch (IOException e) {
//                log.error("Cannot communicate to device {} , exception {}", deviceId, e.getMessage());
            }
        } else {
            log.warn("I'm not master for {} please use master, {} to execute command",
                    deviceId,
                    mastershipService.getMasterFor(deviceId));
        }
    }

    //TODO maybe put method getRestconfClientService like in ovsdb if we need it

}



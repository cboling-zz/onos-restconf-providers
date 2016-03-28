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

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Service;
import org.onosproject.net.DeviceId;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.onosproject.restconf.RestconfController;
import org.onosproject.restconf.RestconfDevice;
import org.onosproject.restconf.RestconfDeviceFactory;
import org.onosproject.restconf.RestconfDeviceInfo;
import org.onosproject.restconf.RestconfDeviceListener;
import org.onosproject.restconf.RestconfDeviceOutputEvent;
import org.onosproject.restconf.RestconfDeviceOutputEventListener;
import org.onosproject.restconf.RestconfException;
import org.osgi.service.component.ComponentContext;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArraySet;

/**
 * RestconfController implementation
 */
@Component(immediate = true)
@Service
public class RestconfControllerImpl implements RestconfController {

    public static final Logger log = LoggerFactory
            .getLogger(RestconfControllerImpl.class);

    private Map<DeviceId, RestconfDevice> restconfDeviceMap = new ConcurrentHashMap<>();

    //private final RestconfDeviceOutputEventListener downListener = new DeviceDownEventListener();

    protected Set<RestconfDeviceListener> restconfDeviceListeners = new CopyOnWriteArraySet<>();
    //protected RestconfDeviceFactory deviceFactory = new DefaultRestconfDeviceFactory();


    @Activate
    public void activate(ComponentContext context) {
        log.info("Started");
    }

    @Deactivate
    public void deactivate() {
        restconfDeviceMap.clear();
        log.info("Stopped");
    }

    @Override
    public Iterable<RestconfDevice> getDevices() {
        return restconfDeviceMap.values();
    }

    @Override
    public void addDeviceListener(RestconfDeviceListener listener) {
        if (!restconfDeviceListeners.contains(listener)) {
            restconfDeviceListeners.add(listener);
        }
    }

    @Override
    public void removeDeviceListener(RestconfDeviceListener listener) {
        restconfDeviceListeners.remove(listener);
    }
}

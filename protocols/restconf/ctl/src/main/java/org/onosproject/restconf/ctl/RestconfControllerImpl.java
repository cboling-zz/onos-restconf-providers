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
package org.onosproject.restconf.ctl;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Service;
import org.onlab.packet.IpAddress;
import org.onosproject.net.DeviceId;
import org.onosproject.restconf.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.osgi.service.component.ComponentContext;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArraySet;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.onlab.util.Tools.groupedThreads;

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
    protected RestconfDeviceFactory deviceFactory = new DefaultRestconfDeviceFactory();

    private int workerThreads = 5;  // TODO: Make this a configuration varioable

    protected ExecutorService executorRxMsgs =
            Executors.newFixedThreadPool(workerThreads, groupedThreads("onos/netconf", "rx-%d",
                    log));
    @Activate
    public void activate(ComponentContext context) {
        log.info("Started");
    }

    @Deactivate
    public void deactivate() {
        restconfDeviceMap.clear();
        log.info("Stopped");
    }

    /**
     * Returns all devices known to this RESTCONF controller.
     *
     * @return Iterable of RESTCONF devices
     */
    @Override
    public Iterable<RestconfDevice> getDevices() {
        return restconfDeviceMap.values();
    }

    /**
     * Get a specific RESTCONF device
     *
     * @param id device ID
     *
     * @return Requested device or NULL if not found
     */
    public RestconfDevice getDevice(DeviceId id) {
        return restconfDeviceMap.get(id);
    }

    /**
     * Gets a RESTCONF Device by node identifier.
     *
     * @param ip   device ip
     * @param port device port
     *
     * @return RestconfDevice RESTCONF device
     */
    public RestconfDevice getDevice(IpAddress ip, int port) {
        return null; // TODO: Implement this
    }
    /**
     * Create a RESTCONF device object
     *
     * @param devInfo
     *
     * @return
     */
    public RestconfDevice createDevice(RestconfDeviceInfo devInfo) {
        return deviceFactory.createRestconfDevice(devInfo);
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

    /**
     * Tries to connect to a specific RESTCONF device, if the connection is successful
     * it creates and adds the device to the ONOS core as a RestconfDevice.
     *
     * @param deviceId deviceId of the device to connect
     * @return RESTCONF device
     * @throws RestconfException when device is not available
     */
    public RestconfDevice connectDevice(DeviceId deviceId) throws RestconfException {

        throw new RestconfException("TODO: Need to implement");
        // TODO: put connectivity guts into the RestconfDevice interface/impl
    }

    /**
     * Disconnects a RESTCONF device and removes it from the core.
     *
     * @param deviceId id of the device to remove
     * @param remove   true if device is to be removed from core
     */
    public void disconnectDevice(DeviceId deviceId, boolean remove) {
        // TODO: Implement this
    }


    /**
     * Removes a RESTCONF device from the core.
     *
     * @param deviceId id of the device to remove
     */
    @Override
    public void removeDevice(DeviceId deviceId) {
        // TODO: Implement this
    }

    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Device ID
     * @param msg Message to send
     */
    @Override
    public void write(DeviceId id, Byte[] msg) {
        this.getDevice(id).sendMsg(msg);
    }

    /**
     * Send a RESTCONF message to a managed RESTCONF device
     *
     * @param id  Device ID
     * @param msg Message to send
     */
    @Override
    public void processPacket(DeviceId id, Byte[] msg) {
    }

    /**
     * Gets all the nodes information.
     *
     * @return map of devices
     */
    @Override
    public Map<DeviceId, RestconfDevice> getDevicesMap() {
        return restconfDeviceMap;
    }

    /**
     * Device factory for the specific RestconfDevice implementation
     */
    private class DefaultRestconfDeviceFactory implements RestconfDeviceFactory {
        /**
         * Creates a new RESTCONF device
         *
         * @param deviceInfo RESTCONF device seed information
         *
         * @return New device
         */
        @Override
        public RestconfDevice createRestconfDevice(RestconfDeviceInfo deviceInfo) {
            return new DefaultRestconfDevice(deviceInfo);
        }
    }
}

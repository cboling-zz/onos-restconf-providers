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
package org.onosproject.provider.restconf.device.impl;

import com.google.common.base.Preconditions;
import com.google.common.collect.Maps;
import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.onlab.packet.ChassisId;
import org.onlab.packet.IpAddress;
import org.onlab.util.SharedScheduledExecutors;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.incubator.net.config.basics.ConfigException;
import org.onosproject.net.*;
import org.onosproject.net.config.ConfigFactory;
import org.onosproject.net.config.NetworkConfigEvent;
import org.onosproject.net.config.NetworkConfigListener;
import org.onosproject.net.config.NetworkConfigRegistry;
import org.onosproject.net.device.*;
import org.onosproject.net.driver.DriverService;
import org.onosproject.net.provider.AbstractProvider;
import org.onosproject.net.provider.ProviderId;
import org.onosproject.restconf.*;
import org.slf4j.Logger;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;

import static org.onosproject.net.config.basics.SubjectFactories.APP_SUBJECT_FACTORY;
import static org.slf4j.LoggerFactory.getLogger;

/**
 * Provider which will try to fetch the details of RESTConf devices from the core
 * and run a capability discovery on each of the device.
 */
@Component(immediate = true)
public class RestconfDeviceProvider extends AbstractProvider
        implements DeviceProvider {
    private final Logger log = getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceProviderRegistry providerRegistry;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected RestconfController controller;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected NetworkConfigRegistry cfgService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DriverService driverService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    // TODO:Keep this?  -> protected Map<DeviceId, RESTConfDevice> restconfDeviceMap = new ConcurrentHashMap<DeviceId, RESTConfDevice>();

    private static final String APP_NAME = "org.onosproject.restconf";
    private static final String SCHEME_NAME = "restconf";
    private static final String DEVICE_PROVIDER_PACKAGE = "org.onosproject.restconf.provider.device";
    private static final String UNKNOWN = "unknown";

    private DeviceProviderService providerService;
    private RestconfDeviceListener deviceListener = new InternalDeviceProvider();

    private final ConfigFactory appConfigFactory =
            new ConfigFactory<ApplicationId, RestconfProviderConfig>(APP_SUBJECT_FACTORY,
                    RestconfProviderConfig.class,
                    "restconf",
                    false) {
                @Override
                public RestconfProviderConfig createConfig() {
                    return new RestconfProviderConfig();
                }
            };

    private final NetworkConfigListener configListener = new InternalConfigListener();
    private ApplicationId appId;
    private HashMap<String, ScheduledFuture<?>> executorResults = Maps.newHashMap();

    public static int connectionTimeout = RestconfProviderConfig.DEFAULT_CONNECTION_TIMEOUT;
    public static int eventInterval = RestconfProviderConfig.DEFAULT_EVENT_INTERVAL;

    // TODO: Make number of initial threads tunable (network config structure)
    // Probably want to create with just '1', then after reading config (or notify on config update)
    // the number can be increased/decreased as appropriate
    //    private ExecutorService executor =
    //            Executors.newFixedThreadPool(numWorkers, groupedThreads("onos/restconfdeviceprovider", "device-installer-%d", log));

    //private ScheduledExecutorService executor;

    /**
     * Create a device provider for the RESTCONF protocol
     */
    public RestconfDeviceProvider() {
        super(new ProviderId(SCHEME_NAME, DEVICE_PROVIDER_PACKAGE));
    }

    @Activate
    public void activate() {
        // During early debugging, failure during 'activate' can leave this component
        // registered with the ProviderService which can cause errors when reloading
        // the same image to debug the issue. Note that a 'onos-app reinstall' will
        // help unregister should you wish to remove the following 'try/catch'.
        try {
            providerService = providerRegistry.register(this);

            appId = coreService.registerApplication(APP_NAME);
            cfgService.registerConfigFactory(appConfigFactory);
            cfgService.addListener(configListener);

            controller.getDevices().forEach(device -> device.addEventListener(deviceListener));
            //executor = SharedScheduledExecutors.getSingleThreadExecutor();

            // Connect from persistent storage first

            connectInitialDevices();

            // Now any devices in network configuration file

            connectDevices();

            log.info("Started");
        } catch (Exception ex) {
            // Failure during activation, make sure we clean up

            log.error("Exception during startup: {}", ex.toString());
            deactivate();
        }
    }

    @Deactivate
    public void deactivate() {
        providerRegistry.unregister(this);
        providerService = null;

        cfgService.unregisterConfigFactory(appConfigFactory);

        controller.getDevices().forEach(device -> device.removeEventListener(deviceListener));

        log.info("Stopped");
    }

    /**
     * Triggers an asynchronous probe of the specified device, intended to
     * determine whether the device is present or not. An indirect result of this
     * should be invocation of
     * {@link org.onosproject.net.device.DeviceProviderService#deviceConnected} )} or
     * {@link org.onosproject.net.device.DeviceProviderService#deviceDisconnected}
     * at some later point in time.
     *
     * @param deviceId ID of device to be probed
     */
    @Override
    public void triggerProbe(DeviceId deviceId) {
        // TODO: This will be implemented later.
        log.info("Triggering probe on device {}", deviceId);
    }

    /**
     * Notifies the provider of a mastership role change for the specified
     * device as decided by the core.
     *
     * @param deviceId device identifier
     * @param newRole  newly determined mastership role
     */
    @Override
    public void roleChanged(DeviceId deviceId, MastershipRole newRole) {
        // TODO: This will be implemented later.
    }

    /**
     * Checks the reachability (connectivity) of a device from this provider.
     *
     * @param deviceId device identifier
     *
     * @return true if reachable, false otherwise
     */
    @Override
    public boolean isReachable(DeviceId deviceId) {
        // TODO: RestconfDevice device = controller.getRestconfDevice(deviceId);
//        if (device == null) {
//            log.debug("Requested device id: {} is not associated to any " +
//                    "RESTCONF Device", deviceId.toString());
//            return false;
//        }
//        return device.isActive();
        return false;
    }

    private class InternalDeviceProvider implements RestconfDeviceListener {

        private static final String IPADDRESS = "ipaddress";
        // TODO: Any other custom annotations?

        /**
         * Notifies that the RESTCONF node was added.
         *
         * @param device RESTCONF Device object
         */
        @Override
        public void deviceAdded(RestconfDevice device) {
            /**
             * Notifies that the RESTCONF node was added.
             *
             * @param devInfo Device information
             */
            Preconditions.checkNotNull(device, "RESTCONF Device is null");
            DeviceId did = device.getDeviceId();
            RestId rid = device.getRestconfId();

            if ((providerService == null) && (controller.getDevice(rid) != null)) {
                return;
            }
            ChassisId cid = new ChassisId(rid.toLong());
            IpAddress ipAddress = device.getDeviceInfo().getIpAddress();

            // TODO: After discovery, can add the MANAGEMENT_ADDRESS annotation?

            SparseAnnotations annotations = DefaultAnnotations.builder()
                    .set(IPADDRESS, ipAddress.toString())
                    .set(AnnotationKeys.PROTOCOL, SCHEME_NAME.toUpperCase())
                    .set(AnnotationKeys.CHANNEL_ID, cid.toString())
                    .build();

            DeviceDescription deviceDescription = new DefaultDeviceDescription(
                    did.uri(),
                    Device.Type.SWITCH, // TODO: Change after discovery?
                    UNKNOWN,            // TODO: Change after discovery? manufacturer
                    UNKNOWN,            // TODO: Change after discovery? hwVersion
                    UNKNOWN,            // TODO: Change after discovery? swVersion
                    UNKNOWN,            // TODO: Change after discovery? serialNumber
                    cid,
                    annotations);

            // Signal the core that a device has been discovered/connected

            providerService.deviceConnected(did, deviceDescription);
        }

        /**
         * Notifies that the RESTCONF node was removed.
         *
         * @param id Device ID
         */
        @Override
        public void deviceRemoved(DeviceId id) {
            Preconditions.checkNotNull(id, "Device ID is null");
            // TODO: DeviceId deviceId = nodeId.getDeviceId();
            // TODO: providerService.deviceDisconnected(deviceId);
        }

        /**
         * Notifies that the RESTCONF node was removed.
         *
         * @param id   Device ID
         * @param info Updated device information
         */
        @Override
        public void deviceModified(DeviceId id, RestconfDeviceInfo info) {
            Preconditions.checkNotNull(id, "Device ID is null");
            Preconditions.checkNotNull(info, "RESTCONF Device info is null");

            // TODO: Update device if needed (IP Address CANNOT change !!!)
        }
    }

    private void connectInitialDevices() {
        // TODO: Do we want to handle devices restored from persistent storage separately?

        for (RestconfDevice device : controller.getDevices()) {
            try {
                deviceListener.deviceAdded(device);

            } catch (Exception e) {
                log.warn("Failed initially adding {} : {}",
                        device.getDeviceId().toString(), e.getMessage());
                log.debug("Error details:", e);

                // disconnect to trigger device-add later
                // TODO: device.disconnectDevice();
            }
        }
    }

    private void connectDevices() {

        // merge any new devices in from configuration file

        RestconfProviderConfig cfg = cfgService.getConfig(appId, RestconfProviderConfig.class);

        if (cfg != null) {
            try {
                for (RestconfDeviceInfo devInfo : cfg.getDeviceInfo().values()) {
                    RestconfDevice device = controller.getDevice(devInfo.getRestconfId());

                    if (device != null) {
                        // If new information, may need to kick device back to DISCOVERY
                        // state.

                        deviceListener.deviceModified(device.getDeviceId(), devInfo);
                    } else {
                        deviceListener.deviceAdded(controller.createDevice(devInfo));
                    }
                }
            } catch (ConfigException e) {
                log.error("Cannot read config error " + e);
            }
        }
    }

    private class InternalConfigListener implements NetworkConfigListener {

        @Override
        public void event(NetworkConfigEvent event) {
            RestconfProviderConfig cfg = cfgService.getConfig(appId,
                    RestconfProviderConfig.class);

            reconfigureNetwork(cfg);
            log.info("Reconfigured: {}", event.type().toString());
        }

        @Override
        public boolean isRelevant(NetworkConfigEvent event) {
            return event.configClass().equals(RestconfProviderConfig.class) &&
                    (event.type() == NetworkConfigEvent.Type.CONFIG_ADDED ||
                            event.type() == NetworkConfigEvent.Type.CONFIG_UPDATED);
        }

        private void reconfigureNetwork(RestconfProviderConfig cfg) {
            // TODO: Throw exception?
            if (cfg == null) {
                return;
            }
            try {
                RestconfDeviceProvider.connectionTimeout = cfg.getConnectionTimeout();
                RestconfDeviceProvider.eventInterval = cfg.getEventInterval();

            } catch (ConfigException e) {
                log.error("Reconfigure Network: ConfigException during parameter read: {}",
                        e.toString());
            }
            connectDevices();
        }
    }
}

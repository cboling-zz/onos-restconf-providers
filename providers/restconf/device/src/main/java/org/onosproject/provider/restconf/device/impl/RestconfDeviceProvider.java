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
import org.onlab.util.SharedScheduledExecutors;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.incubator.net.config.basics.ConfigException;
import org.onosproject.net.DeviceId;
import org.onosproject.net.MastershipRole;
import org.onosproject.net.config.ConfigFactory;
import org.onosproject.net.config.NetworkConfigEvent;
import org.onosproject.net.config.NetworkConfigListener;
import org.onosproject.net.config.NetworkConfigRegistry;
import org.onosproject.net.device.DeviceProvider;
import org.onosproject.net.device.DeviceProviderRegistry;
import org.onosproject.net.device.DeviceProviderService;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.driver.DriverService;
import org.onosproject.net.provider.AbstractProvider;
import org.onosproject.net.provider.ProviderId;
import org.onosproject.restconf.*;
import org.slf4j.Logger;

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
                    true) {
                @Override
                public RestconfProviderConfig createConfig() {
                    return new RestconfProviderConfig();
                }
            };

    private final NetworkConfigListener configListener = new InternalConfigListener();
    private ApplicationId appId;
    private HashMap<String, ScheduledFuture<?>> executorResults = Maps.newHashMap();

    public static int connectionTimeout = RestconfProviderConfig.DEFAULT_CONNECTION_TIMEOUT;
    public static int numWorkers = RestconfProviderConfig.DEFAULT_WORKER_THREADS;
    public static int newNumWorkers = RestconfProviderConfig.DEFAULT_WORKER_THREADS;
    public static int eventInterval = RestconfProviderConfig.DEFAULT_EVENT_INTERVAL;

    // TODO: Make number of initial threads tunable (network config structure)
    // Probably want to create with just '1', then after reading config (or notify on config update)
    // the number can be increased/decreased as appropriate
    //    private ExecutorService executor =
    //            Executors.newFixedThreadPool(numWorkers, groupedThreads("onos/restconfdeviceprovider", "device-installer-%d", log));

    private ScheduledExecutorService executor;

    /**
     * Create a device provider for the RESTCONF protocol
     */
    public RestconfDeviceProvider() {
        super(new ProviderId(SCHEME_NAME, DEVICE_PROVIDER_PACKAGE));
    }

    @Activate
    public void activate() {
        providerService = providerRegistry.register(this);
        appId = coreService.registerApplication(APP_NAME);
        cfgService.registerConfigFactory(appConfigFactory);
        cfgService.addListener(configListener);

        controller.getDevices().forEach(device -> device.addEventListener(deviceListener));
        executor = SharedScheduledExecutors.getSingleThreadExecutor();

        // Connect from persistent storage first

        connectInitialDevices();

        // Now any devices in network configuration file

        connectDevices();

        log.info("Started");
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
        protected static final String ISNULL = "RestconfDeviceInfo is null";

        // TODO: @Override
        public void deviceAdded(RestconfDeviceInfo info) {
            /**
             * Notifies that the RESTCONF node was added.
             *
             * @param devInfo Device information
             */
            Preconditions.checkNotNull(info, ISNULL);
            // Provider service is set to 'null' during deactivation of app

            if (providerService == null) {
                return;
            }

            // DeviceId did = deviceId(uri(info.getRestconfId()));

//            DeviceId deviceId = nodeId.getDeviceId();
//            //Restconf configuration object
//            ChassisId cid = new ChassisId();
//            String ipAddress = nodeId.ip().toString();
//            SparseAnnotations annotations = DefaultAnnotations.builder()
//                    .set(IPADDRESS, ipAddress)
//                    .set(AnnotationKeys.PROTOCOL, SCHEME_NAME.toUpperCase())
//                    .build();
//            DeviceDescription deviceDescription = new DefaultDeviceDescription(
//                    deviceId.uri(),
//                    Device.Type.SWITCH,
//                    UNKNOWN, UNKNOWN,
//                    UNKNOWN, UNKNOWN,
//                    cid,
//                    annotations);
//            providerService.deviceConnected(deviceId, deviceDescription);
        }

        // TODO: @Override
        public void deviceRemoved(RestId deviceId) {
            Preconditions.checkNotNull(deviceId, ISNULL);
            // TODO: DeviceId deviceId = nodeId.getDeviceId();
            // TODO: providerService.deviceDisconnected(deviceId);

        }
    }

    private void connectInitialDevices() {
        // TODO: Do we want to handle devices restored from persistent storage separately?

        for (RestconfDevice device : controller.getDevices()) {
            try {
                deviceListener.deviceAdded(device.getDevideInfo());

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
                        // TODO: Update device, disreguard, ???

                        // TODO: Log whatever we decide to do
                    } else {
                        device = controller.createDevice(devInfo);

                        // TODO: More to DO HERE !!!
                    }
                }
//                cfg.getDeviceInfo().s.getDevicesAddresses().stream()
//                        .forEach(addr -> {
//                                    try {
//                                        RestconfDeviceInfo restconf = new RestconfDeviceInfo(addr.name(),
//                                                addr.password(),
//                                                addr.ip(),
//                                                addr.port());
//                                        controller.connectDevice(restconf);
//                                        Device device = deviceService.getDevice(resttconf.getDeviceId());
//                                        if (device.is(PortDiscovery.class)) {
//                                            PortDiscovery portConfig = device.as(PortDiscovery.class);
//                                            if (portConfig != null) {
//                                                providerService.updatePorts(restconf.getDeviceId(),
//                                                        portConfig.getPorts());
//                                            }
//                                        } else {
//                                            log.warn("No portGetter behaviour for device {}", restconf.getDeviceId());
//                                        }
//
//                                    } catch (IOException e) {
//                                        throw new RuntimeException(
//                                                new RestconfException(
//                                                        "Can't connect to RESTCONF " +
//                                                                "device on " + addr.ip() +
//                                                                ":" + addr.port(), e));
//                                    }
//                                }
//                        );
//
            } catch (ConfigException e) {
                log.error("Cannot read config error " + e);
            }
        }
    }

    private class InternalConfigListener implements NetworkConfigListener {

        @Override
        public void event(NetworkConfigEvent event) {
            if ((event.type() == NetworkConfigEvent.Type.CONFIG_ADDED ||
                    event.type() == NetworkConfigEvent.Type.CONFIG_UPDATED) &&
                    event.configClass().equals(RestconfProviderConfig.class)) {

                RestconfProviderConfig cfg = cfgService.getConfig(appId,
                        RestconfProviderConfig.class);

                reconfigureNetwork(cfg);
                log.info("Reconfigured: {}", event.type().toString());

            } else {
                log.info("Why are we here, is isRelevant not working?");
            }
        }

        @Override
        public boolean isRelevant(NetworkConfigEvent event) {
            return event.configClass().equals(RestconfProviderConfig.class) &&
                    (event.type() == NetworkConfigEvent.Type.CONFIG_ADDED ||
                            event.type() == NetworkConfigEvent.Type.CONFIG_UPDATED);

            // TODO: Also may want to support NetworkConfigEvent.Type.CONFIG_REMOVED.  Investigate this.
        }

        private void reconfigureNetwork(RestconfProviderConfig cfg) {
            // TODO: Throw exception?
            if (cfg == null) {
                return;
            }
            try {
                RestconfDeviceProvider.connectionTimeout = cfg.getConnectionTimeout();
                RestconfDeviceProvider.eventInterval = cfg.getEventInterval();
                RestconfDeviceProvider.newNumWorkers = cfg.getNumberOfWorkerThreads();

                // TODO: drop worker threads if not used... otherwise handle changes

            } catch (ConfigException e) {
                log.error("Reconfigure Network: ConfigException during parameter read: {}",
                        e.toString());
            }
            try {
                Map<String, RestconfDeviceInfo> devices = cfg.getDeviceInfo();

                // TODO: Test how to best handle new/removed devices after we have already
                //       started.  Perhaps only look for additions?

            } catch (ConfigException e) {
                log.error("Reconfigure Network: ConfigException during device read: {}",
                        e.toString());
            }
        }
    }
}

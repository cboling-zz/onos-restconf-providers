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

import static com.google.common.base.Strings.isNullOrEmpty;
import static org.onlab.util.Tools.delay;
import static org.onlab.util.Tools.get;
import static org.onlab.util.Tools.groupedThreads;
import static org.slf4j.LoggerFactory.getLogger;

import java.io.IOException;
import java.net.SocketTimeoutException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Dictionary;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Modified;
import org.apache.felix.scr.annotations.Property;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.onlab.packet.ChassisId;
import org.onosproject.cfg.ComponentConfigService;
import org.onosproject.cluster.ClusterService;
import org.onosproject.net.Device;
import org.onosproject.net.DeviceId;
import org.onosproject.net.MastershipRole;
import org.onosproject.net.device.DefaultDeviceDescription;
import org.onosproject.net.device.DeviceDescription;
import org.onosproject.net.device.DeviceProvider;
import org.onosproject.net.device.DeviceProviderRegistry;
import org.onosproject.net.device.DeviceProviderService;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.provider.AbstractProvider;
import org.onosproject.net.provider.ProviderId;
import org.onosproject.provider.netconf.device.impl.NetconfDevice.DeviceState;
import org.osgi.service.component.ComponentContext;
import org.slf4j.Logger;

/**
 * Provider which will try to fetch the details of RESTCONF devices from the core
 * and run a capability discovery on each of the device.
 */
@Component(immediate = true)
public class NetconfDeviceProvider extends AbstractProvider
        implements DeviceProvider {


    private final Logger log = getLogger(NetconfDeviceProvider.class);

    protected Map<DeviceId, RESTConfDevice> restconfDeviceMap = new ConcurrentHashMap<DeviceId, RESTConfDevice>();

    private DeviceProviderService providerService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceProviderRegistry providerRegistry;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected ClusterService clusterService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected ComponentConfigService cfgService;

    private ExecutorService deviceBuilder = Executors
            .newFixedThreadPool(1, groupedThreads("onos/restconf", "device-creator"));

    // Delay between events in ms.
    private static final int EVENTINTERVAL = 5;

    private static final String SCHEME = "restconf";

    @Property(name = "devConfigs", value = "", label = "Instance-specific configurations")
    private String devConfigs = null;

    @Property(name = "devPasswords", value = "", label = "Instance-specific password")
    private String devPasswords = null;

    /**
     * Creates a provider with the supplier identifier.
     */
    public RESTconfDeviceProvider() {
        super(new ProviderId("restconf", "org.onosproject.provider.restconf"));
    }

    @Activate
    public void activate(ComponentContext context) {
        cfgService.registerProperties(getClass());
        providerService = providerRegistry.register(this);
        modified(context);
        log.info("Started");
    }

    @Deactivate
    public void deactivate(ComponentContext context) {
        cfgService.unregisterProperties(getClass(), false);
        try {
            for (Entry<DeviceId, RESTConfDevice> deviceEntry : restconfDeviceMap
                    .entrySet()) {
                deviceBuilder.submit(new DeviceCreator(deviceEntry.getValue(),
                        false));
            }
            deviceBuilder.awaitTermination(1000, TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            log.error("Device builder did not terminate");
        }
        deviceBuilder.shutdownNow();
        restconfDeviceMap.clear();
        providerRegistry.unregister(this);
        providerService = null;
        log.info("Stopped");
    }

    @Modified
    public void modified(ComponentContext context) {
        if (context == null) {
            log.info("No configuration file");
            return;
        }
        Dictionary<?, ?> properties = context.getProperties();
        String deviceCfgValue = get(properties, "devConfigs");
        log.info("Settings: devConfigs={}", deviceCfgValue);
        if (!isNullOrEmpty(deviceCfgValue)) {
            addOrRemoveDevicesConfig(deviceCfgValue);
        }
    }



    @Override
    public void triggerProbe(DeviceId deviceId) {
        // TODO Auto-generated method stub
    }

    @Override
    public void roleChanged(DeviceId deviceId, MastershipRole newRole) {
        // TODO Auto-generated method stub
    }

    @Override
    public boolean isReachable(DeviceId deviceId) {
        // TODO Auto-generated method stub
        return false;
    }
}
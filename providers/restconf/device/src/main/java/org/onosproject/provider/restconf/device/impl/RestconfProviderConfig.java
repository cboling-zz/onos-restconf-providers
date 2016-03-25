package org.onosproject.provider.restconf.device.impl;

import com.fasterxml.jackson.databind.JsonNode;
import com.google.common.annotations.Beta;
import com.google.common.collect.Sets;
import org.onlab.packet.IpAddress;
import org.onosproject.core.ApplicationId;
import org.onosproject.incubator.net.config.basics.ConfigException;
import org.onosproject.net.config.Config;

import java.util.Set;

/**
 * Configuration for RESTCONF provider.
 */
@Beta
public class RestconfProviderConfig extends Config<ApplicationId> {

    public static final String CONFIG_VALUE_ERROR = "Error parsing config value";
    private static final String IP = "ip";
    private static final int DEFAULT_TCP_PORT = 830;
    private static final String PORT = "port";
    private static final String NAME = "name";
    private static final String PASSWORD = "password";

    public Set<RestconfDeviceAddress> getDevicesAddresses() throws ConfigException {
        Set<RestconfDeviceAddress> devicesAddresses = Sets.newHashSet();

        try {
            for (JsonNode node : array) {
                String ip = node.path(IP).asText();
                IpAddress ipAddr = ip.isEmpty() ? null : IpAddress.valueOf(ip);
                int port = node.path(PORT).asInt(DEFAULT_TCP_PORT);
                String name = node.path(NAME).asText();
                String password = node.path(PASSWORD).asText();
                devicesAddresses.add(new RestconfDeviceAddress(ipAddr, port, name, password));

            }
        } catch (IllegalArgumentException e) {
            throw new ConfigException(CONFIG_VALUE_ERROR, e);
        }

        return devicesAddresses;
    }

    public class RestconfDeviceAddress {

        // TODO: Extend for REST services...

        private final IpAddress ip;
        private final int port;
        private final String name;
        private final String password;

        public RestconfDeviceAddress(IpAddress ip, int port, String name, String password) {
            this.ip = ip;
            this.port = port;
            this.name = name;
            this.password = password;
        }

        public IpAddress ip() {
            return ip;
        }

        public int port() {
            return port;
        }

        public String name() {
            return name;
        }

        public String password() {
            return password;
        }
    }

}

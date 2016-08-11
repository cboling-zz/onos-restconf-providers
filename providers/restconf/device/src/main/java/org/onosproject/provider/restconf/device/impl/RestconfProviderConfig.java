package org.onosproject.provider.restconf.device.impl;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.google.common.annotations.Beta;
import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import org.onlab.packet.IpAddress;
import org.onosproject.core.ApplicationId;
import org.onosproject.incubator.net.config.basics.ConfigException;
import org.onosproject.net.config.Config;
import org.onosproject.restconf.RestconfDeviceInfo;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import static org.onosproject.net.config.Config.FieldPresence.MANDATORY;
import static org.onosproject.net.config.Config.FieldPresence.OPTIONAL;

/**
 * Configuration for RESTCONF provider application
 *
 *
 * TODO: Weed out per-device configurations and move them into the drivers/device configuration
 */
@Beta
public class RestconfProviderConfig extends Config<ApplicationId> {

    /////////////////////////////////////////////////////////////////////////
    // Constants / Defaults

    public static final int DEFAULT_WORKER_THREADS = 1;        // TODO: Increase later (before release)
    public static final int DEFAULT_EVENT_INTERVAL = 5;        // seconds
    public static final int DEFAULT_CONNECTION_TIMEOUT = 15 * 1000;  // milliseconds
    public static final boolean DEFAULT_ADMIN_STATE_UP = true;

    // TODO: for some values, have a maximum as well...

    static final int DEFAULT_SSL_PORT = 443;
    static final int DEFAULT_TCP_PORT = 80;
    static final boolean DEFAULT_IS_TLS = true;

    static final String DEFAULT_XML_MEDIA_TYPE = "xml";
    static final String DEFAULT_JSON_MEDIA_TYPE = "json";
    static final String DEFAULT_API_ROOT = "/restconf";

    /////////////////////////////////////////////////////////////////////////
    // Application level Properties

    private static String WORKER_THREADS = "workerThreads";
    private static String EVENT_INTERVAL = "eventInterval";
    private static String CONNECTION_TIMEOUT = "connectionTimeout"; // Also per-device
    private static String SSL_PREFERRED = "sslPreferred";

    public static final String CONFIG_VALUE_ERROR = "Error parsing config value";

    /////////////////////////////////////////////////////////////////////////
    // Per Device/node Properties
    //boolean tls = node.path().asBoolean();

    private static String DEVICES = "devices";
    private static String USERNAME = "username";
    private static String PASSWORD = "password";
    private static String CERTIFICATE_PATH = "x509Path";
    private static String IP_ADDRESS = "ipAddress";
    private static String PORT = "port";
    private static String IS_TLS = "useTls";
    private static String API_ROOT = "apiRoot";
    private static String MEDIA_TYPES = "mediaTypes";
    private static String NOTES = "notes";
    private static String ADMIN_UP = "adminStatusUp";

    //    private static String hostRegEx = "^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}"
//            + "[0-9A-Za-z])?(?:\\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\\.?$";
    private static String filePathRegEx = "^(/[^/ ]*)+/?$";

    // TODO: Need a number of times we fail on a permanent redirect 'GET' request before we
    //       start to rediscover from the base URI.
    // TODO: For 302 (Temporary redirects) need a default 'rediscover'/'revert' timeout.
    // TODO: For 302, should we also look at any TTL/cache info in the header

    @Override
    public boolean isValid() {
        return hasOnlyFields(WORKER_THREADS, CONNECTION_TIMEOUT, EVENT_INTERVAL,
                SSL_PREFERRED, DEVICES, USERNAME, PASSWORD, CERTIFICATE_PATH,
                IP_ADDRESS, PORT, IS_TLS, API_ROOT, MEDIA_TYPES, NOTES)
                && isNumber(WORKER_THREADS, OPTIONAL, 1)
                && isNumber(CONNECTION_TIMEOUT, OPTIONAL, 50)
                && isNumber(EVENT_INTERVAL, OPTIONAL, 1, 60)
                && isBoolean(SSL_PREFERRED, OPTIONAL)
                && isString(USERNAME, OPTIONAL)
                && isString(PASSWORD, OPTIONAL)
                && isString(CERTIFICATE_PATH, OPTIONAL, filePathRegEx)
                && isIpAddress(IP_ADDRESS, MANDATORY)
                && isNumber(PORT, OPTIONAL, 0, 65535)
                && isBoolean(IS_TLS, OPTIONAL)
                && isBoolean(ADMIN_UP, OPTIONAL)
                && isString(API_ROOT, OPTIONAL)
                && isString(NOTES, OPTIONAL);
    }

    /**
     * The number of worker threads for device discovery and maintenance
     *
     * @return number of threads (1..n)
     *
     * @throws ConfigException
     */
    public int getNumberOfWorkerThreads() throws ConfigException {
        int count = get(WORKER_THREADS, DEFAULT_WORKER_THREADS);

        if (count < 1) {
            throw new ConfigException("Invalid worker thread count. Must be >= 1");
        }
        return count;
    }

    /**
     * The polling event interval for a discovered device, in seconds
     *
     * @return number of seconds (1..n)
     *
     * @throws ConfigException
     */
    public int getEventInterval() throws ConfigException {
        int count = get(EVENT_INTERVAL, DEFAULT_EVENT_INTERVAL);

        if (count < 1) {
            throw new ConfigException("Invalid device polling interval. Must be >= 1");
        }
        return count;
    }

    /**
     * The number of milliseconds to wait for a response to a REST command
     *
     * @return number of milliseconds (1..n)
     *
     * @throws ConfigException
     */
    public int getConnectionTimeout() throws ConfigException {
        int count = get(CONNECTION_TIMEOUT, DEFAULT_CONNECTION_TIMEOUT);

        if (count < 1) {
            throw new ConfigException("Invalid connection timeout. Must be >= 1 mS");
        }
        return count;
    }

    /**
     * Return an immutable map of the devices in the configuration file
     * <p>
     * The key for the map is the string composed of the IP Address for the
     * device.  The contents of the device info provides further information/clarification
     * for the way to contact/discover the device.
     *
     * @return immutable map of Device Information
     *
     * @throws ConfigException
     */
    public Map<String, RestconfDeviceInfo> getDeviceInfo() throws ConfigException {

        Map<String, RestconfDeviceInfo> devicesInfo = Maps.newHashMap();

        if (object.has(DEVICES)) {
            ArrayNode nodeArray = (ArrayNode) object.path(DEVICES);

            try {
                nodeArray.forEach(node -> {
                    String userName = node.path(USERNAME).asText("");
                    String password = node.path(PASSWORD).asText("");
                    String certPath = node.path(CERTIFICATE_PATH).asText("");
                    IpAddress address = IpAddress.valueOf(node.path(IP_ADDRESS).asText(""));
                    int port = node.path(PORT).asInt(DEFAULT_TCP_PORT);
                    boolean tls = node.path(IS_TLS).asBoolean(DEFAULT_IS_TLS);
                    boolean adminUp = node.path(ADMIN_UP).asBoolean(DEFAULT_ADMIN_STATE_UP);
                    int timeout = get(CONNECTION_TIMEOUT, DEFAULT_CONNECTION_TIMEOUT);
                    String apiRoot = node.path(API_ROOT).asText(DEFAULT_API_ROOT);
                    List<String> mediaTypes = Lists.newArrayList();

                    // The 'notes' section is mainly to allow some comments to be added
                    // per-device to the config JSON, not necessarily the device that we
                    // will create.

                    if (node.has(MEDIA_TYPES)) {
                        node.forEach(mtype -> mediaTypes.add(node.asText()));
                    } else {
                        mediaTypes.add(DEFAULT_XML_MEDIA_TYPE);
                        mediaTypes.add(DEFAULT_JSON_MEDIA_TYPE);
                    }
                    RestconfDeviceInfo device = new RestconfDeviceInfo(address,
                            port, tls, timeout,
                            userName, password, certPath, apiRoot,
                            mediaTypes, adminUp);

                    devicesInfo.put(address.toString(), device);
                });
            } catch (IllegalArgumentException e) {
                throw new ConfigException(CONFIG_VALUE_ERROR, e);
            }
        }
        return Collections.unmodifiableMap(devicesInfo);
    }
}

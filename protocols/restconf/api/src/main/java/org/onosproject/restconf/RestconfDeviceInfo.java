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
package org.onosproject.restconf;

import com.google.common.base.Preconditions;
import org.onlab.packet.IpAddress;
import org.onosproject.net.DeviceId;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Provides information on initial connectivity to a RESTCONF device
 */
public class RestconfDeviceInfo {

    private DeviceId deviceId;
    private final String userName;
    private final String password;
    private final String certificatePath;   // TODO: May want to contain it here, not in a file
    private final IpAddress address;
    private final int port;
    private final boolean useTLS;
    private final String apiRoot;
    private final List<String> mediaTypes;
    private final int socketTimeout;
    private boolean isAdminUp;

    // TODO: Added persistent storage / cluster support?
    // TODO: Do we want to keep sessions to devices opened for a smaller window of time after
    //       a message is sent/received in order to improve performance during tasks that may
    //       take several round-trips to perform?
    // TODO: Any 'cached' connection timeouts may need to be different depending upon RESTCONF
    //       device state (Discovery, ...)

    /**
     * TODO: Complete documentation here...
     *
     * @param ipaddr
     * @param port
     * @param tls
     * @param username
     * @param password
     * @param certificatePath
     * @param apiRoot
     * @param mediaTypes
     */
    public RestconfDeviceInfo(IpAddress ipaddr, int port,
                              boolean tls, int socketTimeout,
                              String username, String password, String certificatePath,
                              String apiRoot, List<String> mediaTypes, boolean adminUp) {

        Preconditions.checkArgument(!username.equals(""), "Empty device user name");
        Preconditions.checkArgument(!apiRoot.equals(""), "Empty RESTCONF API Root");
        Preconditions.checkNotNull(port > 0, "Negative TCP port");
        Preconditions.checkNotNull(ipaddr, "Null ip address");

        // TODO: Validate parameters...  Throw exception on error.

        this.userName = username;
        this.password = password;
        this.certificatePath = certificatePath;
        this.address = ipaddr;
        this.port = port;
        this.useTLS = tls;
        this.socketTimeout = socketTimeout;
        this.apiRoot = apiRoot;
        this.mediaTypes = mediaTypes;
        this.isAdminUp = adminUp;
    }

    /**
     * @return
     */
    public String getUserName() {
        return userName;
    }

    /**
     * @return
     */
    public String getPassword() {
        return password;
    }

    /**
     * @return
     */
    public String getCertificatePath() {
        return certificatePath;
    }

    /**
     * @return
     */
    public IpAddress getIpAddress() {
        return address;
    }

    /**
     * @return
     */
    public int getSocketTimeout() {
        return socketTimeout;
    }

    /**
     * Get the base URL for this device
     *
     * @return http[s]://<ip-addr>:<port>/
     */
    public String getBaseURL() {
        String url = useTLS ? "https://" : "http://";

        return url + address + ":" + port;
    }

    /**
     * @return
     */
    public String getApiRoot() {
        return apiRoot;
    }

    /**
     * @return
     */
    public List<String> getMediaTypes() {
        return Collections.unmodifiableList(mediaTypes);
    }

    /**
     * @return
     */
    public int getPort() {
        return port;
    }

    /**
     * @return
     */
    public boolean getTLS() {
        return useTLS;
    }

    /**
     * Return the DeviceId about the device containing the URI.
     *
     * @return DeviceId
     */
    public DeviceId getDeviceId() {
        if (deviceId == null) {
            deviceId = createDeviceId(address, port);
        }
        return deviceId;
    }

    /**
     * Helper method to create a DeviceId
     *
     * @param address IP Address
     * @param port    port Number
     *
     * @return Device ID
     */
    public static DeviceId createDeviceId(IpAddress address, int port) {
        try {
            return DeviceId.deviceId(new URI("restconf", address.toString() + ":" + port,
                    null));

        } catch (URISyntaxException e) {
            throw new IllegalArgumentException("Unable to build deviceID for device "
                    + address.toString() + ":" + port, e);
        }
    }

    /**
     * Set the Administrative state of the device to either UP or DOWN
     * <p>
     * The default state for a device is UP which allows it to participate with this
     * provider over the RESTCONF protocol. You can place a device in the DOWN state
     * to disable the RESTCONF protocol as needed (during shutdown, to maintain it in a
     * standby mode, perform maintenance, ...)
     *
     * @param setAdminUp If true, the administrative state of the device will be placed in the
     *                   UP state.  Down otherwise.
     */
    public void setAdminState(boolean setAdminUp) {

        if (setAdminUp != isAdminUp) {
            // TODO: Implement this.

            isAdminUp = setAdminUp;
        }
    }

    /**
     * Get the ADMIN state for this device
     *
     * @return current ADMIN UP state.  true = UP, false = down
     */
    public boolean getAdminStateUp() {
        return isAdminUp;
    }

    /**
     * Return the info about the device in a string.
     * String format: "restconf:username@ip:port"
     *
     * @return String device info
     */
    @Override
    public String toString() {
        return "restconf:" + userName + "@" + address + ":" + port;
    }

    @Override
    public int hashCode() {
        return Objects.hash(address, port);
    }

    @Override
    public boolean equals(Object toBeCompared) {
        if (toBeCompared instanceof RestconfDeviceInfo) {
            RestconfDeviceInfo deviceInfo = (RestconfDeviceInfo) toBeCompared;
            if (deviceInfo.address.equals(address)
                    && deviceInfo.getPort() == port) {
                return true;
            }
        }
        return false;
    }
}

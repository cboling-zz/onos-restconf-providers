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
package org.onosproject.restconf;

import com.google.common.base.Preconditions;
import org.onlab.packet.IpAddress;
import org.onosproject.net.DeviceId;

import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Provides information on initial connectivity to a RESTCONF device
 */
public class RestconfDeviceInfo {

    private final String hostName;
    private final String userName;
    private final String password;
    private final String certificatePath;
    private final IpAddress address;
    private final short tcpPort;
    private final short sslPort;
    private final String apiRoot;
    private final List<String> mediaTypes;

    // TODO: Do we want to support persistent connections to devices?
    // TODO: Do we want to keep sessions to devices opened for a smaller window of time after
    //       a message is sent/received in order to improve performance during tasks that may
    //       take several round-trips to perform?
    // TODO: Any 'cached' connection timeouts may need to be different depending upon RESTCONF
    //       device state (Discovery, ...)

    /**
     * TODO: Complete documentation here...
     *
     * @param hostname
     * @param ipaddr
     * @param tcpPort
     * @param sslPort
     * @param username
     * @param password
     * @param certificatePath
     * @param apiRoot
     * @param mediaTypes
     */
    public RestconfDeviceInfo(String hostname, IpAddress ipaddr, short tcpPort,
                              short sslPort, String username, String password,
                              String certificatePath,
                              String apiRoot, List<String> mediaTypes) {

        Preconditions.checkArgument(!apiRoot.equals(""), "Empty RESTCONF API Root");
        Preconditions.checkNotNull(tcpPort > 0, "Negative TCP port");
        Preconditions.checkNotNull(sslPort > 0, "Negative SSL port");
        Preconditions.checkNotNull(ipaddr, "Null ip address");

        // TODO: Validate parameters...  Throw exception on error.

        if ((hostname == null) || hostname.isEmpty()) {
            hostname = ipaddr.toString();
        }
        this.hostName = hostname;
        this.userName = username;
        this.password = password;
        this.certificatePath = certificatePath;
        this.address = ipaddr;
        this.tcpPort = tcpPort;
        this.sslPort = sslPort;
        this.apiRoot = apiRoot;
        this.mediaTypes = mediaTypes;
    }

    /**
     * @return
     */
    public RestId getRestconfId() {
        return RestId.valueOf(address);
    }

    /**
     * @return
     */
    public String getHostName() {
        return hostName;
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
    public String getApiRoot() {
        return apiRoot;
    }

    /**
     * @return
     */
    public List<String> getMediaTYpes() {
        return Collections.unmodifiableList(mediaTypes);
    }

    /**
     * @return
     */
    public short getSslPort() {
        return sslPort;
    }

    /**
     * @return
     */
    public short getTcpPort() {
        return tcpPort;
    }

    @Override
    public int hashCode() {
        return Objects.hash(address);
    }

    @Override
    public boolean equals(Object toBeCompared) {
        if (toBeCompared instanceof RestconfDeviceInfo) {
            RestconfDeviceInfo deviceInfo = (RestconfDeviceInfo) toBeCompared;
            if (deviceInfo.address.equals(address)) {
                return true;
            }
        }
        return false;
    }
}

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
package org.onosproject.restconf.cfgfile;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.onlab.packet.IpAddress;

import java.util.ArrayList;
import java.util.List;

/**
 * RestConf Device entry in JSON Configuration File
 * <p>
 * TODO: Support REST with this as well
 * TODO: A YANG module to describe this would be helpful (as well as other classes)
 */
public class RESTConfDeviceEntry {

    private String hostName;
    private IpAddress ipAddress;
    private List<Integer> portNumbers;
    private String apiRoot;
    private String url;
    private String userName;
    private String password;
    private List<String> mediaTypes;
    private String x509Path;

    /**
     * s
     * Default consturctor
     */
    public RESTConfDeviceEntry() {
        portNumbers = new ArrayList<>();
        portNumbers.add(RESTConfConfiguration.DEFAULT_SSL_PORT);
        portNumbers.add(RESTConfConfiguration.DEFAULT_TCP_PORT);

        mediaTypes = new ArrayList<>();
        mediaTypes.add(RESTConfConfiguration.DEFAULT_XML_MEDIA_TYPE);
        mediaTypes.add(RESTConfConfiguration.DEFAULT_JSON_MEDIA_TYPE);

        apiRoot = RESTConfConfiguration.DEFAULT_API_ROOT;
    }

    public RESTConfDeviceEntry(String name, IpAddress addr,
                               List<Integer> ports, String root,
                               String url, String user, String pwd,
                               List<String> typeList, String certificateFile) {
        hostName = name;
        ipAddress = addr;
        portNumbers = ports;
        apiRoot = root;
        this.url = url;
        userName = user;
        password = pwd;
        mediaTypes = typeList;
        x509Path = certificateFile;
    }

    public String getHostName() {
        return hostName;
    }

    @JsonProperty("hostName")
    public void setHostName(String name) {
        hostName = name;
    }

    public IpAddress getIpAddress() {
        return ipAddress;
    }

    @JsonProperty("ipAddress")
    public void setIpAddress(IpAddress addr) {
        ipAddress = addr;
    }

    public List<Integer> getPortNumbers() {
        return portNumbers;
    }

    @JsonProperty("portNumbers")
    public void setPortNumbers(List<Integer> name) {
        portNumbers = name;
    }

    public String getApiRoot() {
        return apiRoot;
    }

    @JsonProperty("apiRoot")
    public void setApiRoot(String name) {
        apiRoot = name;
    }

    public String getUrl() {
        return url;
    }

    @JsonProperty("url")
    public void setUrl(String url) {
        this.url = url;
    }

    public String getUserName() {
        return userName;
    }

    @JsonProperty("userName")
    public void setUserName(String name) {
        userName = name;
    }

    public String getPassword() {
        return password;
    }

    @JsonProperty("password")
    public void setPassword(String pwd) {
        password = pwd;
    }

    public List<String> getMediaTypes() {
        return mediaTypes;
    }

    @JsonProperty("mediaTypes")
    public void setMediaTypes(List<String> name) {
        mediaTypes = name;
    }

    public String getX509File() {
        return x509Path;
    }

    @JsonProperty("x509Path")
    public void setX509File(String path) {
        x509Path = path;
    }
}

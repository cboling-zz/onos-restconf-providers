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
package org.onosproject.provider.restconf.device.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.onlab.packet.MacAddress;
import org.onosproject.rest.AbstractWebResource;
import org.slf4j.Logger;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.InputStream;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Created by cboling on 9/27/15.
 */
@Path("restconf")
public class RESTConfResource extends AbstractWebResource {

    private final Logger log = getLogger(getClass());

    /**
     * Create a new RESTConf Device
     *
     * @param stream input stream
     * @return response to the request
     */
    @POST
    @Path("add")
    public String deviceAddNotification(InputStream stream) {

        log.info("Received Device create request");

        if (stream == null) {
            log.info("Parameters can not be null");
            return "";
        }
        //RESTManager restService = get(RESTManager.class);
        //RESTDeviceEntry entry = jsonToAccessPoint(stream);
        // Create the access point (TODO Look into what we want to return)
        String returnData = null; // TODO Call into RESTConf service and create a device

        if (returnData != null) {
            return returnData;
        } else {
            return "";
        }
    }

    /**
     * Delete a RESTConf Device
     *
     * @param mac MAC Address of the host
     * @return version string for new (TODO) What do we really want
     */
    @DELETE
    @Path("{mac}")
    public String deviceDeleteNotification(@PathParam("mac") MacAddress mac) {
        if (mac == null) {
            log.info("MAC Address to delete is null");
            return "";
        }
        log.info("Received RESTConf device delete request: Addr= {}", mac.toString());

        //RESTManager restService = get(RESTManager.class);
        //RESTDeviceEntry entry = jsonToAccessPoint(stream);
        // Create the access point (TODO Look into what we want to return)
        String returnData = null; // TODO Call into RESTConf service and delete a device

        if (returnData != null) {
            return returnData;
        } else {
            return "";
        }
    }

    /**
     * Query RESTConf devices
     *
     * @return IP Address map
     */
    @GET
    @Path("list")
    @Produces(MediaType.APPLICATION_JSON)
    public Response deviceGetNotification() {

        log.info("Received Device list request");

        //RESTManager restService = get(RESTManager.class);
        // TODO Get a list of devices
        //List<RESTConfDeviceEntry> list = restService.getAccessPoints();
        ObjectNode result = new ObjectMapper().createObjectNode();
        //result.set("list", new ESTConfDeviceCodec().encode(list, this));

        return ok(result.toString()).build();
    }
    // TODO quite a few other operations and URIs will be needed for this application
}


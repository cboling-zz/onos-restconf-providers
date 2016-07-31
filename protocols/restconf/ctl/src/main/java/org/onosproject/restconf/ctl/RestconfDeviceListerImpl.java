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
package org.onosproject.restconf.ctl;

import org.onosproject.net.DeviceId;
import org.onosproject.restconf.RestconfDevice;
import org.onosproject.restconf.RestconfDeviceInfo;
import org.onosproject.restconf.RestconfDeviceListener;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by cboling on 3/28/16.
 */
public class RestconfDeviceListerImpl implements RestconfDeviceListener {

    final List<DeviceId> removedDevices = new ArrayList<>();
    final List<DeviceId> addedDevices = new ArrayList<>();
    final List<DeviceId> changedDevices = new ArrayList<>();
    // final Map<DeviceId, OFPortStatus> portChangedDevices = new HashMap<>();

    /**
     * Notifies that the RESTCONF node was added.
     *
     * @param device RESTCONF Device object
     */
    public void deviceAdded(RestconfDevice device) {
        // TODO: Implement this

        // Create device ID (may need to be port of RestconfDeviceInfo)

        // Create annotations & Device description

        // Call into provider service
    }

    /**
     * Notifies that the RESTCONF node was removed.
     *
     * @param id Device ID
     */
    public void deviceRemoved(DeviceId id) {
        // TODO: Implement this
    }

    /**
     * Notifies that the RESTCONF node was removed.
     *
     * @param id   Device ID
     * @param info Updated device information
     */
    public void deviceModified(DeviceId id, RestconfDeviceInfo info) {
        // TODO: Implement this
    }
}

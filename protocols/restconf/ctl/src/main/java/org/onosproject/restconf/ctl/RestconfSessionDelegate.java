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
package org.onosproject.restconf.ctl;

import org.onosproject.restconf.RestconfDeviceOutputEvent;

/**
 * Delegate interface associated with a RestconfSessionImpl that is used to
 * receiving notifications of events about the session.
 */
public interface RestconfSessionDelegate {
    /**
     * Notifies the delegate via the specified event.
     *
     * @param event store generated event
     */
    void notify(RestconfDeviceOutputEvent event);
}

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

import com.mastfrog.acteur.headers.HeaderValueType;
import com.mastfrog.netty.http.client.HttpClient;
import com.mastfrog.netty.http.client.HttpRequestBuilder;
import com.mastfrog.netty.http.client.ResponseFuture;
import com.mastfrog.netty.http.client.ResponseHandler;
import io.netty.handler.codec.http.HttpHeaders;
import io.netty.handler.codec.http.HttpResponseStatus;
import org.joda.time.Duration;
import org.onosproject.net.DeviceId;
import org.onosproject.restconf.RestconfDevice;
import org.onosproject.restconf.RestconfDeviceInfo;
import org.onosproject.restconf.RestconfDeviceStateMachineException;
import org.slf4j.Logger;
import com.mastfrog.acteur.headers.Headers;

import static org.slf4j.LoggerFactory.getLogger;
import static com.google.common.base.MoreObjects.toStringHelper;

/**
 * RESTCONF device state machine
 */
public class RestconfDeviceStateMachine {
    /**
     * Idle (temporary) state of the device that occurs just after the device
     * is created by CLI/NetConfig JSON or is being restored from persistent
     * storage after a Control or RESTCONF protocol driver reset.
     */
    static final int IDLE = 0;
    static final int DISCOVERY = 1; // Attempting initial connection and meta-data lookup
    static final int POPULATE = 2;  // Pulling down YANG libraries supported
    static final int ACTIVE = 3;    // Active and ready for operations
    static final int INACTIVE = 4;  // Inactive due to administrative interaction or temporary disconnection
    static final int FAILED = 5;    // Inactive/error, cannot connect to device

    static final int CONNECT = 0;
    static final int DOWNLOAD = 1;
    static final int LOADED = 2;
    static final int ADMIN_DOWN = 3;
    static final int ADMIN_UP = 4;
    static final int ERROR = 5;

    private final Logger log = getLogger(getClass());

    static final String rootResource = ".well-known/host-meta";
    static final String rootResourceFormat = "application/xrd+xml";

    private int currentState = IDLE;
    private int retries = 0;
    private String failureReason = "";

    private RestconfDevice device;
    private DeviceId deviceId;
    private Duration connectTimeout;

    private State[] states = {
            new Idle(), new Discovery(), new Populate(),
            new Active(), new Inactive(), new Failed()
    };
    private static String[] stateName = {
            "IDLE", "DISCOVERY", "POPULATE", "ACTIVE", "INACTIVE", "FAILED"
    };

    public RestconfDeviceStateMachine(RestconfDevice device) {
        RestconfDeviceInfo info = device.getDeviceInfo();

        this.device = device;
        deviceId = device.getDeviceId();
        connectTimeout = Duration.millis(info.getSocketTimeout());
    }

    /**
     * Get the current device state
     *
     * @return Device State
     */
    public int getState() {
        return currentState;
    }

    /**
     * Get the String name for the current state
     *
     * @return String name of state
     */
    public String getStateAsText() {
        return stateName[currentState];
    }

    /**
     * Get reason the device is in the FAILED or INACTIVE state
     *
     * @return Failure reason (blank if not in a failed or inactive state)
     */
    public String getFailureReason() {
        return failureReason;
    }

    @Override
    public String toString() {
        return toStringHelper(this)
                .add("state", getStateAsText())
                .add("retries", retries)
                .toString();
    }

    // State transition table
    //
    //    state ->  IDLE     | DISCOVERY  | POPULATE  |  ACTIVE   |  INACTIVE |  FAILED
    // input
    //---v-------------------------------------------------------------------------------
    // CONNECT     DISCOVERY |   _        |   _       | DISCOVERY | DISCOVERY | DISCOVERY
    //
    // DOWNLOAD      -       |  POPULATE  |   _       |   _       |   _       |   _
    //
    // LOADED        -       |   _        |  ACTIVE   |   _       |   _       |   _
    //
    // ADMIN_DOWN    -       |   _        |   _       |  INACTIVE |   _       |   _
    //
    // ADMIN_UP      -       |   _        |   _       |   _       |  ACTIVE   |   _
    //
    // ERROR         -       |   FAILED   |  FAILED   |  FAILED   |  FAILED   |   _
    //-----------------------------------------------------------------------------------
    //
    // TODO: May not end up supporting ADMIN_UP/DOWN capability to start with...

    private static final int[] idleTransition = {DISCOVERY, IDLE, IDLE, IDLE, IDLE, IDLE};
    private static final int[] discoveryTransition = {DISCOVERY, POPULATE, DISCOVERY, DISCOVERY, DISCOVERY, FAILED};
    private static final int[] populateTransition = {POPULATE, POPULATE, ACTIVE, POPULATE, POPULATE, FAILED};
    private static final int[] activeTransition = {DISCOVERY, ACTIVE, ACTIVE, INACTIVE, ACTIVE, FAILED};
    private static final int[] inactiveTransition = {DISCOVERY, INACTIVE, INACTIVE, INACTIVE, ACTIVE, FAILED};
    private static final int[] failedTransition = {DISCOVERY, FAILED, FAILED, FAILED, FAILED, FAILED};

    // Transistion table

    private static final int[][] transitionTable = {
            idleTransition, discoveryTransition, populateTransition,
            activeTransition, inactiveTransition, failedTransition
    };

    /**
     * Base class for state translation
     */
    abstract class State {
        private final Logger log = getLogger(getClass());

        private String name = "State";

        public void connect() throws RestconfDeviceStateMachineException {
            log.warn("CONNECT transition from this state is not allowed.");
        }

        public void download() throws RestconfDeviceStateMachineException {
            log.warn("LIBRARY DOWNLOAD transition from this state is not allowed.");
        }

        public void loaded() throws RestconfDeviceStateMachineException {
            log.warn("LIBRARY LOADED transition from this state is not allowed.");
        }

        public void adminStatusDown() throws RestconfDeviceStateMachineException {
            log.warn("ADMIN_DOWN transition from this state is not allowed.");
        }

        public void adminStatusUp() throws RestconfDeviceStateMachineException {
            log.warn("ADMIN_UP transition from this state is not allowed.");
        }

        public void error(String reason) throws RestconfDeviceStateMachineException {
            log.warn("ERROR transition from this state is not allowed.");
        }

        public void receiveMessage(HttpResponseStatus status, HttpHeaders headers, String response) {
            log.info("Message reception in this state is ignored");
        }
    }

    class Idle extends State {
        private final Logger log = getLogger(getClass());
        private String name = "IDLE_STATE";
        private HttpClient client = null;

        /**
         * A device in the IDLE state has received a connect message.  It should initiate
         * discovery of the meta-data to locate where the RESTCONF API root is located.
         */
        @Override
        public void connect() {
            log.info("connect: entry");

            // Create async HTTP Client and attempt to discover the Root Resource.

            // TODO: Support SSL
            // TODO: Support more than basic credentials

            client = HttpClient.builder()
                    .followRedirects()
                    .setTimeoweut(connectTimeout)
                    .build();

            String url = device.getBaseURL() + rootResource;

            HttpRequestBuilder builder = client.get()
                    .setURL(url);

            ResponseFuture future = builder.execute(new ResponseHandler<String>(String.class) {
                protected void receive(HttpResponseStatus status, HttpHeaders headers,
                                       String response) {
                    receiveMessage(status, headers, response);
                }
            });
            //public static final HeaderValueType<String> ACCEPT = new StringHeader("Accept".toString());
        }

        @Override
        public void receiveMessage(HttpResponseStatus status, HttpHeaders headers, String response) {
            log.info("TODO: Implement this");
        }
    }

    class Discovery extends State {
        private final Logger log = getLogger(getClass());
        private String name = "DISCOVERY_STATE";

        /**
         * The device is in the DISCOVERY state and knows where the RESTCONF API root
         * is located.  It now needs to examine the mandatory 'ietf-yang-library' to
         * discover the Library version.
         */
        public void download() {
            log.warn("TODO: Implement this");
        }

        public void error(String reason) {
            log.warn("TODO: Implement this");
        }
    }

    class Populate extends State {
        private final Logger log = getLogger(getClass());
        private String name = "POPULATE_STATE";

        /**
         * The schema (YANG modules) were located and downloaded or were not
         * provided since this is optional.  Parse any libraries found for location of
         * drivers that we may need to load and then to active.
         *
         * @throws RestconfDeviceStateMachineException
         */
        public void loaded() throws RestconfDeviceStateMachineException {
            log.warn("LIBRARY LOADED transition from this state is not allowed.");
        }

        public void error(String reason) {
            log.warn("TODO: Implement this");
        }
    }

    class Active extends State {
        private final Logger log = getLogger(getClass());
        private String name = "ACTIVE";

        @Override
        public void connect() {
            log.warn("TODO: Implement this");
        }

        public void adminStatusDown() {
            log.warn("TODO: Implement this");
        }

        public void error(String reason) {
            log.warn("TODO: Implement this");
        }
    }

    class Inactive extends State {
        private final Logger log = getLogger(getClass());
        private String name = "INACTIVE";

        @Override
        public void connect() {
            log.warn("TODO: Implement this");
        }

        public void adminStatusUp() {
            log.warn("TODO: Implement this");
        }

        public void error(String reason) {
            log.warn("TODO: Implement this");
        }
    }

    class Failed extends State {
        private final Logger log = getLogger(getClass());
        private String name = "FAILED";

        @Override
        public void connect() {
            log.warn("TODO: Implement this");
        }
    }

    /**
     * Transition to the next state
     *
     * @param message Transition message
     */
    private void nextState(int message) {
        int prevState = currentState;
        currentState = transitionTable[currentState][message];
        log.info("[]: State change {} -> {}", deviceId.toString(),
                stateName[prevState], stateName[currentState]);
    }

    public void connect() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(CONNECT);

        // TODO: Do message specific actions
    }

    public void download() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(DOWNLOAD);

        // TODO: Do message specific actions
    }

    public void loaded() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(LOADED);

        // TODO: Do message specific actions
    }

    public void adminStatusDown() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(ADMIN_DOWN);

        // TODO: Do message specific actions
    }

    public void adminStatusUp() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(ADMIN_UP);

        // TODO: Do message specific actions
    }

    public void error() throws RestconfDeviceStateMachineException {
        states[currentState].connect();

        // Move to the next state

        nextState(ERROR);

        // TODO: Do message specific actions
    }

}

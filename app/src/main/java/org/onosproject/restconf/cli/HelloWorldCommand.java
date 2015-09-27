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
package org.onosproject.restconf.cli;

import org.apache.karaf.shell.commands.Argument;
import org.apache.karaf.shell.commands.Command;
import org.onosproject.cli.AbstractShellCommand;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Command to show the list of vBNG IP address mapping entries.
 */
@Command(scope = "onos", name = "restconf",
        description = "An example command")

public class HelloWorldCommand extends AbstractShellCommand {

    // TODO Need some real commands!!!
    private static final String FORMAT_HELLO_WORLD = "Blah blah blah.";

    // TODO Probably do not want hostName to be the unique qualifier for an Access Point
    // so this is more of an example to work from when we decide what to is best
    private final Logger log = LoggerFactory.getLogger(getClass());
    @Argument(index = 0, name = "name", description = "Device name of the RESTConfDevice",
            required = false, multiValued = false)
    private String devName = null;

    /**
     * Execute the vwlan CLI command
     */
    @Override
    protected void execute() {

        log.info("Entry");
        print(FORMAT_HELLO_WORLD);
    }
}
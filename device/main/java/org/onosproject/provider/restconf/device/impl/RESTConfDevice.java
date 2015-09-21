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

import static com.google.common.base.Preconditions.checkNotNull;
import static org.onlab.util.Tools.delay;
import static org.slf4j.LoggerFactory.getLogger;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.Format;
import org.jdom2.output.XMLOutputter;
import org.slf4j.Logger;

import com.tailf.jnc.Capabilities;
import com.tailf.jnc.JNCException;
import com.tailf.jnc.SSHConnection;
import com.tailf.jnc.SSHSession;


/**
 * This is a logical representation of actual RESTConf device, carrying all the
 * necessary information to connect and execute RESTConf operations.
 */
public class NetconfDevice {
    private final Logger log = getLogger(NetconfDevice.class);


}
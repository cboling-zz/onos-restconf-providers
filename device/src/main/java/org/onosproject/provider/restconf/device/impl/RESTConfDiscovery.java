package org.onosproject.provider.restconf.device.impl;

import org.apache.felix.scr.annotations.*;
import org.onosproject.cfg.ComponentConfigService;
import org.osgi.service.component.ComponentContext;
import org.slf4j.Logger;

import static org.slf4j.LoggerFactory.getLogger;

/**
 * Created by cboling on 9/27/15.
 */
public class RESTConfDiscovery {
    private static final Logger log = getLogger(RESTConfDiscovery.class);
    private static final int DEFAULT_SSL_PORT = 443;
    private static final int DEFAULT_TCP_PORT = 80;
    private static final String DEFAULT_USERNAME = "";
    private static final String DEFAULT_PASSWORD = "";
    private static final String DEFAULT_API_ROOT = "/restconf";
    private static final String DEFAULT_SCHEME = "https";
    private static final boolean support300Redirects = true;  // Multiple Choices redirects
    private static final boolean support301Redirects = true;  // Moved Permanently redirects
    private static final boolean support302Redirects = true;  // Found redirects
    private static final boolean support303Redirects = true;  // See other redirects
    private static final boolean support307Redirects = true;  // Temporary redirects
    private static final boolean support308Redirects = true;  // Permanent redirects
    private static final String Root_XML_MSG = new StringBuilder(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            .append("<hello xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\">")
            .append("<capabilities><capability>urn:ietf:params:netconf:base:1.0</capability>")
            .append("</capabilities></hello>").toString();
    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected ComponentConfigService cfgService;
    @Property(name = "follow300Redirects", boolValue = support300Redirects, label = "Follow 300 Multiple Choices Redirects")
    private boolean follow300Redirects = support300Redirects;
    @Property(name = "follow301Redirects", boolValue = support301Redirects, label = "Follow 301 Status Moved Permanently Redirects")
    private boolean follow301Redirects = support301Redirects;
    @Property(name = "follow302Redirects", boolValue = support302Redirects, label = "Follow 302 Status Found Redirects")
    private boolean follow302Redirects = support302Redirects;
    @Property(name = "follow303Redirects", boolValue = support303Redirects, label = "Follow 303 Status See Other Redirects")
    private boolean follow303Redirects = support303Redirects;
    @Property(name = "follow307Redirects", boolValue = support307Redirects, label = "Follow 307 Status Temporary Redirects")
    private boolean follow307Redirects = support307Redirects;
    @Property(name = "follow308Redirects", boolValue = support308Redirects, label = "Follow 308 Status Temporary Redirects")
    private boolean follow308Redirects = support308Redirects;

    // TODO: Support modified-since header on requests for host-meta discovery and perhaps in other areas as well

    // https://jersey.java.net/documentation/latest/user-guide.html#d0e10355
    // http://www.hascode.com/2013/12/jax-rs-2-0-rest-client-features-by-example/
    // https://jersey.java.net/documentation/latest/user-guide.html#async
    // https://jfarcand.wordpress.com/2011/03/24/writing-powerful-rest-client-using-the-asynchttpclient-library-and-jersey/

    @Activate
    public void activate(ComponentContext context) {
        cfgService.registerProperties(getClass());
        modified(context);
        log.info("Started");

        // TODO : More to do
    }

    @Deactivate
    public void deactivate(ComponentContext context) {
        cfgService.unregisterProperties(getClass(), false);
        // TODO : More to do

        log.info("Stopped");
    }

    @Modified
    public void modified(ComponentContext context) {
        if (context == null) {
            log.info("No configuration file");
            return;
        }
        // TODO : More to do
    }
}

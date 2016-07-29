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

import javax.ws.rs.ext.RuntimeDelegate;
import java.util.Collections;
import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

/**
 * Implements a javax/ws/rs/core/MediaType class specific for RESTCONF
 * <p>
 * An abstraction for a media type for RESTCONF. Instances are immutable.
 */
public class RestconfMediaType {
    private String type;
    private String subtype;
    private Map<String, String> parameters;
    /**
     * The media type {@code charset} parameter name.
     */
    public static final String CHARSET_PARAMETER = "charset";
    /**
     * The value of a type or subtype wildcard {@value #MEDIA_TYPE_WILDCARD}.
     */
    public static final String MEDIA_TYPE_WILDCARD = "*";
    // Common media type constants
    /**
     * A {@code String} constant representing wildcard {@value #WILDCARD} media type .
     */
    public final static String WILDCARD = "*/*";
    /**
     * A {@link RestconfMediaType} constant representing wildcard {@value #WILDCARD} media type.
     */
    public final static RestconfMediaType WILDCARD_TYPE = new RestconfMediaType();

    public static final String APPLICATION_API_XML = "application/yang.api+xml";
    public static final String APPLICATION_API_JSON = "application/yang.api+json";
    public static final RestconfMediaType APPLICATION_API_XML_TYPE = new RestconfMediaType("application", "yang.api+xml");
    public static final RestconfMediaType APPLICATION_API_JSON_TYPE = new RestconfMediaType("application", "yang.api+json");

    public static final String APPLICATION_DATASTORE_XML = "application/yang.datastore+xml";
    public static final String APPLICATION_DATASTORE_JSON = "application/yang.datastore+json";
    public static final RestconfMediaType APPLICATION_DATASTORE_XML_TYPE = new RestconfMediaType("application", "yang.datastore+xml");
    public static final RestconfMediaType APPLICATION_DATASTORE_JSON_TYPE = new RestconfMediaType("application", "yang.datastore+json");

    public static final String APPLICATION_DATA_XML = "application/yang.data+xml";
    public static final String APPLICATION_DATA_JSON = "application/yang.data+json";
    public static final RestconfMediaType APPLICATION_DATA_XML_TYPE = new RestconfMediaType("application", "yang.data+xml");
    public static final RestconfMediaType APPLICATION_DATA_JSON_TYPE = new RestconfMediaType("application", "yang.data+json");

    public static final String APPLICATION_ERRORS_XML = "application/yang.errors+xml";
    public static final String APPLICATION_ERRORS_JSON = "application/yang.errors+json";
    public static final RestconfMediaType APPLICATION_ERRORS_XML_TYPE = new RestconfMediaType("application", "yang.errors+xml");
    public static final RestconfMediaType APPLICATION_ERRORS_JSON_TYPE = new RestconfMediaType("application", "yang.errors+json");

    public static final String APPLICATION_OPERATION_XML = "application/yang.operation+xml";
    public static final String APPLICATION_OPERATION_JSON = "yang.operation+json";
    public static final RestconfMediaType APPLICATION_OPERATION_XML_TYPE = new RestconfMediaType("application", "yang.operation+xml");
    public static final RestconfMediaType APPLICATION_OPERATION_JSON_TYPE = new RestconfMediaType("application", "yang.operation+json");

    public static final String APPLICATION_SCHEMA = "application/yang";
    public static final RestconfMediaType APPLICATION_SCHEMA_TYPE = new RestconfMediaType("application", "yang");

    /**
     * Creates a new instance of {@code RestconfMediaType} by parsing the supplied string.
     *
     * @param type the media type string.
     *
     * @return the newly created RestconfMediaType.
     *
     * @throws IllegalArgumentException if the supplied string cannot be parsed
     *                                  or is {@code null}.
     */
    public static RestconfMediaType valueOf(String type) {
        return RuntimeDelegate.getInstance().createHeaderDelegate(RestconfMediaType.class).fromString(type);
    }

    private static TreeMap<String, String> createParametersMap(Map<String, String> initialValues) {
        final TreeMap<String, String> map = new TreeMap<String, String>(new Comparator<String>() {

            @Override
            public int compare(String o1, String o2) {
                return o1.compareToIgnoreCase(o2);
            }
        });
        if (initialValues != null) {
            for (Map.Entry<String, String> e : initialValues.entrySet()) {
                map.put(e.getKey().toLowerCase(), e.getValue());
            }
        }
        return map;
    }

    /**
     * Creates a new instance of {@code RestconfMediaType} with the supplied type, subtype and
     * parameters.
     *
     * @param type       the primary type, {@code null} is equivalent to
     *                   {@link #MEDIA_TYPE_WILDCARD}.
     * @param subtype    the subtype, {@code null} is equivalent to
     *                   {@link #MEDIA_TYPE_WILDCARD}.
     * @param parameters a map of media type parameters, {@code null} is the same as an
     *                   empty map.
     */
    public RestconfMediaType(String type, String subtype, Map<String, String> parameters) {
        this(type, subtype, null, createParametersMap(parameters));
    }

    /**
     * Creates a new instance of {@code RestconfMediaType} with the supplied type and subtype.
     *
     * @param type    the primary type, {@code null} is equivalent to
     *                {@link #MEDIA_TYPE_WILDCARD}
     * @param subtype the subtype, {@code null} is equivalent to
     *                {@link #MEDIA_TYPE_WILDCARD}
     */
    public RestconfMediaType(String type, String subtype) {
        this(type, subtype, null, null);
    }

    /**
     * Creates a new instance of {@code RestconfMediaType} with the supplied type, subtype and
     * {@value #CHARSET_PARAMETER} parameter.
     *
     * @param type    the primary type, {@code null} is equivalent to
     *                {@link #MEDIA_TYPE_WILDCARD}
     * @param subtype the subtype, {@code null} is equivalent to
     *                {@link #MEDIA_TYPE_WILDCARD}
     * @param charset the {@value #CHARSET_PARAMETER} parameter value. If {@code null} or empty
     *                the {@value #CHARSET_PARAMETER} parameter will not be set.
     */
    public RestconfMediaType(String type, String subtype, String charset) {
        this(type, subtype, charset, null);
    }

    /**
     * Creates a new instance of {@code RestconfMediaType}, both type and subtype are wildcards.
     * Consider using the constant WILDCARD_TYPE instead.
     */
    public RestconfMediaType() {
        this(MEDIA_TYPE_WILDCARD, MEDIA_TYPE_WILDCARD, null, null);
    }

    private RestconfMediaType(String type, String subtype, String charset, Map<String, String> parameterMap) {

        this.type = type == null ? MEDIA_TYPE_WILDCARD : type;
        this.subtype = subtype == null ? MEDIA_TYPE_WILDCARD : subtype;

        if (parameterMap == null) {
            parameterMap = new TreeMap<String, String>(new Comparator<String>() {

                @Override
                public int compare(String o1, String o2) {
                    return o1.compareToIgnoreCase(o2);
                }
            });
        }

        if (charset != null && !charset.isEmpty()) {
            parameterMap.put(CHARSET_PARAMETER, charset);
        }
        this.parameters = Collections.unmodifiableMap(parameterMap);
    }

    /**
     * Getter for primary type.
     *
     * @return value of primary type.
     */
    public String getType() {
        return this.type;
    }

    /**
     * Checks if the primary type is a wildcard.
     *
     * @return true if the primary type is a wildcard.
     */
    public boolean isWildcardType() {
        return this.getType().equals(MEDIA_TYPE_WILDCARD);
    }

    /**
     * Getter for subtype.
     *
     * @return value of subtype.
     */
    public String getSubtype() {
        return this.subtype;
    }

    /**
     * Checks if the subtype is a wildcard.
     *
     * @return true if the subtype is a wildcard.
     */
    public boolean isWildcardSubtype() {
        return this.getSubtype().equals(MEDIA_TYPE_WILDCARD);
    }

    /**
     * Getter for a read-only parameter map. Keys are case-insensitive.
     *
     * @return an immutable map of parameters.
     */
    public Map<String, String> getParameters() {
        return parameters;
    }

    /**
     * Create a new {@code RestconfMediaType} instance with the same type, subtype and parameters
     * copied from the original instance and the supplied {@value #CHARSET_PARAMETER} parameter.
     *
     * @param charset the {@value #CHARSET_PARAMETER} parameter value. If {@code null} or empty
     *                the {@value #CHARSET_PARAMETER} parameter will not be set or updated.
     *
     * @return copy of the current {@code RestconfMediaType} instance with the {@value #CHARSET_PARAMETER}
     * parameter set to the supplied value.
     *
     * @since 2.0
     */
    public RestconfMediaType withCharset(String charset) {
        return new RestconfMediaType(this.type, this.subtype, charset, createParametersMap(this.parameters));
    }

    /**
     * Check if this media type is compatible with another media type. E.g.
     * image/* is compatible with image/jpeg, image/png, etc. Media type
     * parameters are ignored. The function is commutative.
     *
     * @param other the media type to compare with.
     *
     * @return true if the types are compatible, false otherwise.
     */
    public boolean isCompatible(RestconfMediaType other) {
        return other != null && // return false if other is null, else
                (type.equals(MEDIA_TYPE_WILDCARD) || other.type.equals(MEDIA_TYPE_WILDCARD) || // both are wildcard types, or
                        (type.equalsIgnoreCase(other.type) && (subtype.equals(MEDIA_TYPE_WILDCARD)
                                || other.subtype.equals(MEDIA_TYPE_WILDCARD))) || // same types, wildcard sub-types, or
                        (type.equalsIgnoreCase(other.type) && this.subtype.equalsIgnoreCase(other.subtype))); // same types & sub-types
    }

    /**
     * Compares {@code obj} to this media type to see if they are the same by comparing
     * type, subtype and parameters. Note that the case-sensitivity of parameter
     * values is dependent on the semantics of the parameter name, see
     * {@link <a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.7">HTTP/1.1</a>}.
     * This method assumes that values are case-sensitive.
     * <p/>
     * Note that the {@code equals(...)} implementation does not perform
     * a class equality check ({@code this.getClass() == obj.getClass()}). Therefore
     * any class that extends from {@code RestconfMediaType} class and needs to override
     * one of the {@code equals(...)} and {@link #hashCode()} methods must
     * always override both methods to ensure the contract between
     * {@link Object#equals(java.lang.Object)} and {@link Object#hashCode()} does
     * not break.
     *
     * @param obj the object to compare to.
     *
     * @return true if the two media types are the same, false otherwise.
     */
    @SuppressWarnings("UnnecessaryJavaDocLink")
    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof RestconfMediaType)) {
            return false;
        }

        RestconfMediaType other = (RestconfMediaType) obj;
        return (this.type.equalsIgnoreCase(other.type)
                && this.subtype.equalsIgnoreCase(other.subtype)
                && this.parameters.equals(other.parameters));
    }

    /**
     * Generate a hash code from the type, subtype and parameters.
     * <p/>
     * Note that the {@link #equals(java.lang.Object)} implementation does not perform
     * a class equality check ({@code this.getClass() == obj.getClass()}). Therefore
     * any class that extends from {@code RestconfMediaType} class and needs to override
     * one of the {@link #equals(Object)} and {@code hashCode()} methods must
     * always override both methods to ensure the contract between
     * {@link Object#equals(java.lang.Object)} and {@link Object#hashCode()} does
     * not break.
     *
     * @return a generated hash code.
     */
    @SuppressWarnings("UnnecessaryJavaDocLink")
    @Override
    public int hashCode() {
        return (this.type.toLowerCase() + this.subtype.toLowerCase()).hashCode() + this.parameters.hashCode();
    }

    /**
     * Convert the media type to a string suitable for use as the value of a
     * corresponding HTTP header.
     *
     * @return a string version of the media type.
     */
    @Override
    public String toString() {
        return RuntimeDelegate.getInstance().createHeaderDelegate(RestconfMediaType.class).toString(this);
    }
}

/**
 * 
 */
package org.cisecurity.tools.ciscat.xsd;

import java.util.HashMap;

import javax.xml.XMLConstants;

import org.cisecurity.tools.ciscat.base.NamespaceContextBase;
import org.cisecurity.tools.ciscat.base.NamespaceContextBase;

/**
 * @author bmunyan
 *
 */
public class CiscatSchemaValidatorNamespaceContext extends NamespaceContextBase {

	public CiscatSchemaValidatorNamespaceContext() {
		logger.info("Created Schema Validator Namespace Context...");
		
		HashMap<String, String> scap12map = new HashMap<String, String>();
		
		//scap12map.put(XMLConstants.XMLNS_ATTRIBUTE, "http://scap.nist.gov/schema/scap/source/1.2");
		//scap12map.put("cat", "urn:oasis:names:tc:entity:xmlns:xml:catalog");
		//scap12map.put("xlink", "http://www.w3.org/1999/xlink");
		//scap12map.put("xsi", "http://www.w3.org/2001/XMLSchema-instance");
                //scap12map.put("xccdf", "http://checklists.nist.gov/xccdf/1.2");
                //scap12map.put("cve", "http://benchmarks.cisecurity.org/cve/1.0");
                //scap12map.put("cce", "http://benchmarks.cisecurity.org/cce/1.0");
		//scap12map.put("xs", "http://www.w3.org/2001/XMLSchema");
		scap12map.put("ds", "http://www.w3.org/2000/09/xmldsig#");
		//scap12map.put("xsl", "http://www.w3.org/1999/XSL/Transform");
		//scap12map.put("dc", "http://purl.org/dc/elements/1.1/");

                //scap12map.put("win", "http://oval.mitre.org/XMLSchema/oval-system-characteristics-5#windows");
                //scap12map.put("core", "http://oval.mitre.org/XMLSchema/oval-system-characteristics-5");
				
		setMap(scap12map);
	}
}

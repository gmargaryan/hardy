
package org.cisecurity.tools.ciscat.xsd;

import gov.nist.scap.schema.assetReportingFormat.x11.AssetReportCollectionDocument;
import gov.nist.scap.schema.scap.source.x12.DataStreamCollectionDocument;
import java.io.IOException;
import java.io.InputStream;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.cert.CertificateEncodingException;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import javax.xml.XMLConstants;
import org.apache.logging.log4j.Logger;
import org.apache.xml.security.signature.XMLSignature;
import org.apache.xml.security.keys.KeyInfo;
import javax.xml.transform.Source;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;
import org.apache.logging.log4j.LogManager;
import org.cisecurity.tools.ciscat.CisCertChecker;
import org.cisecurity.tools.ciscat.fact.CiscatRestrictionsFactory;
import org.cisecurity.tools.ciscat.impl.oval.OvalNamespaceContext;
import org.cisecurity.tools.ciscat.impl.oval.comp.VersionComparator;
import org.cisecurity.tools.ciscat.impl.scap12.util.Scap12HashUtilities;
import org.cisecurity.tools.ciscat.util.CiscatConstants;
import org.cisecurity.tools.ciscat.util.CiscatUtilities;
import org.cisecurity.tools.ciscat.util.CiscatXmlUtilities;
import org.cisecurity.tools.ciscat.util.XPathUtilities;
import org.mitre.oval.xmlSchema.ovalCommon5.OperationEnumeration;
import org.mitre.oval.xmlSchema.ovalResults5.ResultEnumeration;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * Perform Schema & XML Digital Signature validations
 * @author bmunyan
 */
public class CiscatSchemaValidator {
    private Logger _logger = LogManager.getLogger("org.cisecurity.tools.ciscat.xsd");

    private boolean _verifyXmlSignature = false;
    private ArrayList<String>   _errors = new ArrayList<String>();

    /**
     * constructor
     * @param verifyXmlSignature
     */
    public CiscatSchemaValidator(boolean verifyXmlSignature) {
        _verifyXmlSignature = verifyXmlSignature;
        _errors.clear();
    }

    //
    //  Start:  Public Entry Points for Validation
    //

    /**
     * validate SCAP 1.1/ECL XCCDF benchmark document
     * @param document
     * @return
     */
    public int validateXccdf(Document document) {
        _logger.info("CiscatSchemaValidator::validateXccdf -- [START]");

        Source[] legacySchemas = {
            new StreamSource(getClass().getResource("validator-xccdf11-benchmark.xsd").toString())
        };
        
        int rtn = validate(legacySchemas, document, document.getBaseURI());
        
        _logger.info("CiscatSchemaValidator::validateXccdf -- [ END ]");
        return rtn;
    }

    /**
     * validate SCAP 1.1/ECL XCCDF benchmark document
     * @param document
     * @return
     */
    public int validateXccdf11(Document document, ArrayList<Document> ovalSubdocuments) {
        _logger.info("CiscatSchemaValidator::validateXccdf11 -- [START]");

        Source[] legacySchemas = {
            new StreamSource(getClass().getResource("validator-xccdf11-benchmark.xsd").toString())
        };

        int rtn = validate(legacySchemas, document, document.getBaseURI());
        if (rtn != CiscatConstants.SUCCESS) {
            return rtn;
        }

        rtn = validateOvalSubDocuments(ovalSubdocuments);
        if (rtn != CiscatConstants.SUCCESS) {
            return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
        }
        _logger.info("CiscatSchemaValidator::validateXccdf11 -- [ END ]");
        return CiscatConstants.SUCCESS;
    }

    /**
     * validate XCCDF 1.2 benchmark document
     * @param document
     * @return
     */
    public int validateXccdf12(Document document, ArrayList<Document> ovalSubdocuments) {
        _logger.info("CiscatSchemaValidator::validateXccdf12 -- [START]");
        
        Source[] xccdf12Schemas = {
            new StreamSource(getClass().getResource("validator-xccdf12-benchmark.xsd").toString())
            //new StreamSource(getClass().getResourceAsStream("validator-xccdf12-benchmark.xsd"))
        };
        
        int rtn = validate(xccdf12Schemas, document, document.getBaseURI());
        if (rtn != CiscatConstants.SUCCESS) {
            return rtn;
        }

        // validate any referenced OVAL definitions files...
        rtn = validateOvalSubDocuments(ovalSubdocuments);
        if (rtn != CiscatConstants.SUCCESS) {
            return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
        }
        _logger.info("CiscatSchemaValidator::validateXccdf12 -- [ END ]");
        return rtn;
    }

    /**
     * validate SCAP 1.2 datastream collection document
     * @param collection
     * @return
     */
    public int validateDatastreamCollection(DataStreamCollectionDocument collection) {
        _logger.info("CiscatSchemaValidator::validateDatastreamCollection -- [START]");

        Source[] scap12Schemas = {
            new StreamSource(getClass().getResource("validator-data-stream-collection.xsd").toString())
        };
        
        Document document = CiscatXmlUtilities.getInstance().createXmlDocument(collection);
        int rtn = validate(scap12Schemas, document, document.getBaseURI());
        
        _logger.info("CiscatSchemaValidator::validateDatastreamCollection -- [ END ]");
        return rtn;
    }
    
    /**
     * Validate an Asset Reporting Format XML report.
     * @param arf
     * @return 
     */
    public int validateARF(AssetReportCollectionDocument arf) {
        _logger.info("CiscatSchemaValidator::validateARF -- [START]");

        Source[] arfSchemas = {
            new StreamSource(getClass().getResource("validator-asset-reporting-format.xsd").toString())
        };

        Document document = CiscatXmlUtilities.getInstance().createXmlDocument(arf);
        
        int rtn = validate(arfSchemas, document, document.getBaseURI());
        _logger.info("CiscatSchemaValidator::validateARF -- [ END ]");
        return rtn;
    }

    /**
     * validate OVAL Definitions document
     * @param document
     * @return
     */
    public int validateOvalDefinitions(Document document) {
        _logger.info("CiscatSchemaValidator::validateOvalDefinitions -- [START]");

        ArrayList<Document> ovalSubdocuments = new ArrayList<Document>();
        ovalSubdocuments.add(document);
        int rtn = validateOvalSubDocuments(ovalSubdocuments);
        _logger.info("CiscatSchemaValidator::validateOvalDefinitions -- [ END ]");
        if (rtn != CiscatConstants.SUCCESS) {
            return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
        }
        return rtn;
    }

    /**
     * validate OVAL Definitions document
     * @param document
     * @return
     */
    public int validateOvalVariables(Document document) {
        _logger.info("CiscatSchemaValidator::validateOvalVariables -- [START]");

        int rtn = CiscatConstants.SUCCESS;
        
        Source[] legacyOval53Schemas = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.4.xsd").toString())
        };
        Source[] scap11Oval58Schemas = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.8.xsd").toString())
        };
        Source[] oval510Schemas      = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.10.1.xsd").toString())
        };
        Source[] oval511Schemas      = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.11.xsd").toString())
        };
        Source[] oval5111Schemas     = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.11.1.xsd").toString())
        };
        Source[] oval5112Schemas     = {
            new StreamSource(getClass().getResource("validator-oval-variables-5.11.2.xsd").toString())
        };
        
        if (document.getDocumentElement().getAttribute("xmlns:oval") != null) {
            // Try to validate the file then...

            _logger.info("CiscatSchemaValidator::validateOvalVariables -- Getting OVAL schema version...");
            String schema_version =
                XPathUtilities.asString(
                    document,
                    "/oval:oval_variables/oval:generator/oval-common:schema_version", 
                    new OvalNamespaceContext());
            _logger.info("CiscatSchemaValidator::validateOvalVariables -- Found schema_version = '" + schema_version.toString() + "'...");

            Source[] schemas = null;

            final String LEGACY_MAX   = "5.4";
            final String SCAP11_MAX   = "5.8";
            final String OVAL510_MAX  = "5.10.1";
            final String OVAL511_MAX  = "5.11";
            final String OVAL5111_MAX = "5.11.1";
            VersionComparator vc = new VersionComparator();

            ResultEnumeration.Enum legacy   = vc.compare(schema_version, LEGACY_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
            ResultEnumeration.Enum scap11   = vc.compare(schema_version, SCAP11_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
            ResultEnumeration.Enum oval510  = vc.compare(schema_version, OVAL510_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
            ResultEnumeration.Enum oval511  = vc.compare(schema_version, OVAL511_MAX, OperationEnumeration.EQUALS);
            ResultEnumeration.Enum oval5111 = vc.compare(schema_version, OVAL5111_MAX, OperationEnumeration.EQUALS);

            if (legacy == ResultEnumeration.TRUE) {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.3/4 schemas...");
                schemas = legacyOval53Schemas;
            } else if (scap11 == ResultEnumeration.TRUE) {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.8 schemas...");
                schemas = scap11Oval58Schemas;
            } else if (oval510 == ResultEnumeration.TRUE) {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.10 schemas...");
                schemas = oval510Schemas;
            } else if (oval511 == ResultEnumeration.TRUE) {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.11 schemas...");
                schemas = oval511Schemas;
            } else if (oval5111 == ResultEnumeration.TRUE) {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.11.1 schemas...");
                schemas = oval5111Schemas;
            } else {
                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validating against OVAL 5.11.2 schemas...");
                schemas = oval5112Schemas;
            }

            try {
                Schema tmpSchema =
                    SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema").newSchema(schemas);

                tmpSchema.newValidator().validate(new DOMSource(document));

                _logger.info("CiscatSchemaValidator::validateOvalVariables -- Validation Succeeded.");
            } catch (SAXException ex) {
                String errorMessage =
                    "An OVAL variables file referenced by the selected OVAL definitions is invalid according to its schema." + ex.getLocalizedMessage();
                _logger.warn(errorMessage, ex);
                _errors.add(errorMessage);
                rtn = CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
            } catch (IOException io) {
                _logger.warn("Error loading OVAL schemas for validation -- " + io.getLocalizedMessage());
                _errors.add("Error loading OVAL schemas for validation -- " + io.getLocalizedMessage());
                rtn = CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
            }

        }
        
        _logger.info("CiscatSchemaValidator::validateOvalVariables -- [ END ]");
        if (rtn != CiscatConstants.SUCCESS) {
            return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
        }
        return rtn;
    }

    /**
     * Return any validation errors collected by schema validation
     * @return ArrayList of error messages.
     */
    public ArrayList<String> getValidationErrors() {
        return _errors;
    }
    
    //
    // ----------------- PRIVATE METHODS -----------------
    //

    /**
     * perform XML schema validations
     * @param schemas
     * @param document
     * @param baseUrl
     * @return
     */
    private int validate(Source[] schemas, Document document, String baseUrl) {
        int rtn = CiscatConstants.SUCCESS;

        _logger.info("CiscatSchemaValidator::validate (schemas, document, baseUrl) -- [START]");
        try {
            Schema datastreamCollectionSchema =
                SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI).newSchema(schemas);

            Validator datastreamCollectionValidator = datastreamCollectionSchema.newValidator();

            //
            // Use the CIS-CAT Error Handler to collect any Error/FatalError Messages...
            //
            CiscatSchemaValidatorErrorHandler csveh = new CiscatSchemaValidatorErrorHandler();

            datastreamCollectionValidator.setErrorHandler(csveh);
            datastreamCollectionValidator.validate(new DOMSource(document));

            if (csveh.isError()) {
                _errors = csveh.getErrors();

                _logger.warn("Schema Validator::validate -- Schema Validation Errors collected by Error Handler...");
                return CiscatConstants.ERROR_VALIDATING_XML;
            }
        } catch (SAXException ex) {
            _logger.warn("Schema Validator::validate -- SAXException: ", ex);
            return CiscatConstants.ERROR_VALIDATING_XML;
        } catch (IOException io) {
            _logger.warn("Schema Validator::validate -- IOException: ", io);
            return CiscatConstants.ERROR_VALIDATING_XML;
        }

        // Determine if any system restrictions (such as execution of the Community version)
        // require validation of the CIS certificate...
        if (CiscatRestrictionsFactory.getRestrictionHandler().checkXmlSigntaure()) {
            rtn = validateCISSignature(document, baseUrl);
            if (rtn != CiscatConstants.SUCCESS) {
                return CiscatConstants.ERROR_XCCDF_SIGNATURE;
            }
        }

        if (_verifyXmlSignature && !CiscatRestrictionsFactory.getRestrictionHandler().checkXmlSigntaure()) {
            rtn = validateXmlSignature(document, baseUrl);
            if (rtn != CiscatConstants.SUCCESS) {
                return CiscatConstants.ERROR_XML_SIGNATURE;
            }
        }
        _logger.info("CiscatSchemaValidator::validate (schemas, document, baseUrl) -- [ END ]");
        return rtn;
    }

    /**
     * Validate that CIS signed the benchmark
     * This means that there is a signature attached to the XML, it is a valid
     * signature, and that the hash of that signature matches the CIS "thumbprint"
     * The "extra" piece of the logic which necessitates this method is the
     * validation of the "thumbprint"
     * @param document
     * @param baseUrl
     * @return
     */
    private int validateCISSignature(Document document, String baseUrl) {
        final String MSG1 = "Unable to find signature in benchmark. All benchmarks must be signed by CIS.";
        final String MSG2 = "This benchmark is not signed by CIS.";
        final String MSG3 = "The digital signature on the benchmark you've selected is invalid.  This typically indicates that the benchmark policy has been modified.";

        _logger.info("CiscatSchemaValidator::validateCISSignature -- [START]");
        _logger.info("CiscatSchemaValidator::validateCISSignature -- Step 1: Validate XML Signature...");

        int rtn = validateXmlSignature(document, baseUrl);
        if (rtn != CiscatConstants.SUCCESS) {
            return CiscatConstants.ERROR_XML_SIGNATURE;
        }

        _logger.info("CiscatSchemaValidator::validateCISSignature -- Step 2: Validate CIS Thumbprint...");

        try {
            Element document_signature =
                (Element)XPathUtilities.asNode(
                    document.getDocumentElement(),
                    "//*/ds:Signature[1]",
                    new CiscatSchemaValidatorNamespaceContext());

            if (document_signature == null) {
                _logger.warn(MSG1);
                _errors.add(MSG1);
                return CiscatConstants.ERROR_XCCDF_SIGNATURE;
            }

            XMLSignature signature = new XMLSignature(document_signature, baseUrl);
            KeyInfo      keyInfo   = signature.getKeyInfo();
            if (keyInfo != null) {
                X509Certificate x509Certificate = signature.getKeyInfo().getX509Certificate();
                String          bmkThumbprint   = getCertificateThumbprint(x509Certificate);

                _logger.info("CiscatSchemaValidator::validateCISSignature -- CIS Thumbprint = '" + CiscatConstants.CIS_THUMBPRINT + "'");
                _logger.info("CiscatSchemaValidator::validateCISSignature -- Bmk Thumbprint = '" + bmkThumbprint + "'");
                
                boolean bThumbprintCheck =
                    CiscatConstants.CIS_THUMBPRINT.equalsIgnoreCase(bmkThumbprint);

                _logger.info("CiscatSchemaValidator::validateCISSignature -- bThumbprintCheck = " + bThumbprintCheck);

                if (!bThumbprintCheck) {
                    _logger.warn(MSG2);
                    _errors.add(MSG2);
                    return CiscatConstants.ERROR_XCCDF_SIGNATURE;

                } else if (x509Certificate == null) {
                    _logger.warn(MSG1);
                    _errors.add(MSG1);
                    return CiscatConstants.ERROR_XCCDF_SIGNATURE;
                }

                // Verify the CIS certificate chain...
                _logger.info("CiscatSchemaValidator::validateCISSignature -- Step 3: Validate CIS Certificate Chain...");
                CisCertChecker checker = new CisCertChecker();
                checker.checkCert(x509Certificate, CiscatUtilities.getInstance().getCiscatBuildDate());
            } else {
                _logger.warn(MSG1);
                _errors.add(MSG1);
                return CiscatConstants.ERROR_XCCDF_SIGNATURE;
            }
        } catch (Exception ex) {
            _logger.warn(MSG3, ex);
            _errors.add(MSG3);
            return CiscatConstants.ERROR_XCCDF_SIGNATURE;
        }
        _logger.info("CiscatSchemaValidator::validateCISSignature -- [ END ]");
        return CiscatConstants.SUCCESS;
    }

    /**
     * Validate the XML digital signature...
     * @param document
     * @param baseUrl
     * @return
     */
    private int validateXmlSignature(Document document, String baseUrl) {
        final String MSG1 = "Unable to find signature in benchmark. All benchmarks must be signed.";
        final String MSG2 = "The digital signature on the benchmark you've selected is invalid.  This typically indicates that the benchmark policy has been modified.";

        _logger.info("CiscatSchemaValidator::validateXmlSignature (Document) -- START");
        try {
            Element signatureElement =
                (Element)XPathUtilities.asNode(
                    document.getDocumentElement(),
                    "//*/ds:Signature[1]",
                    new CiscatSchemaValidatorNamespaceContext());

            if (signatureElement == null) {
                _logger.warn("CiscatSchemaValidator::validateXmlSignature (Document) -- " + MSG1);
                _errors.add(MSG1);
                return CiscatConstants.ERROR_XML_SIGNATURE;
            }
            _logger.info("CiscatSchemaValidator::validateXmlSignature (Document) -- Found <ds:Signature>; Validating...");
            return validateXmlSignature(document, signatureElement, baseUrl);
        } catch(Exception ex) {
            _logger.warn("CiscatSchemaValidator::validateXmlSignature (Document) -- " + MSG2, ex);
            _errors.add(MSG2);
            return CiscatConstants.ERROR_XML_SIGNATURE;
        }
    }

    /**
     * Using the ds:Signature element found in the XML document, validate the signature
     * @param signatureElement
     * @param file
     * @return int success/failure value
     */
    private int validateXmlSignature(Document document, Element signatureElement, String baseUrl) {
        _logger.info("START -- CIS-CAT Schema Validator :: validateXmlSignature");

        try {
            XMLSignature signature = new XMLSignature(signatureElement, baseUrl);
            signature.setFollowNestedManifests(false);

            //
            // NOTE:  During SCAP 1.2 validation, a requirement existed to validate digital
            // signatures of data-stream-collections.  References in the signatures pointed
            // to data-streams within the collection.  In order for those signatures to validate,
            // the data-stream @id's needed to be noted as an "id attribute".  So here we have
            // to find/loop through any data-stream elements and set their @id's to be
            // "id attributes"...
            //
            NodeList ds = document.getElementsByTagName("data-stream");
            for (int i = 0; i < ds.getLength(); ++i) {
                Element e = (Element)ds.item(i);
                e.setIdAttribute("id", true);
            }

            KeyInfo keyInfo = signature.getKeyInfo();
            _logger.debug(keyInfo);
            if (keyInfo != null) {
                _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Found <KeyInfo>...");
                if (keyInfo.containsX509Data()) {
                    _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Found X509 Data within KeyInfo...");
                }
                X509Certificate x509_certificate = signature.getKeyInfo().getX509Certificate();
                _logger.debug(x509_certificate);

                boolean valid;
                if (x509_certificate != null) {
                    _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Found X509Certificate; Checking signature value...");
                    valid = signature.checkSignatureValue(x509_certificate);
                } else {
                    PublicKey publicKey = signature.getKeyInfo().getPublicKey();
                    if (publicKey != null) {
                        _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Did NOT find X509Certificate, but found Public Key; Using Public Key to validate signature...");
                        valid = signature.checkSignatureValue(publicKey);
                    } else {
                        _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- No Public Key found; Can't check signature...");
                        valid = false;
                    }
                }

                if (valid) {
                    _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Signature Validation Successful!");

//                    _logger.info("CiscatSchemaValidator::validateXmlSignature (Element) -- Validating CIS Thumbprint...");
//                    boolean bThumbprintCheck =
//                        CiscatConstants.CIS_THUMBPRINT.equalsIgnoreCase(getCertificateThumbprint(x509_certificate));
//                    if (!bThumbprintCheck) {
//                        _logger.warn("CiscatSchemaValidator::validateXmlSignature (Element) -- This benchmark does not have a valid CIS Thumbprint...");
//                        _errors.add("(Thumbprint) The digital signature on the benchmark you've selected is invalid.  This typically indicates that the benchmark policy has been modified.");
//                        return CiscatConstants.ERROR_XML_SIGNATURE;
//                    }
                } else {
                    _logger.warn("CiscatSchemaValidator::validateXmlSignature (Element) -- This benchmark does not have a valid signature...");
                    _errors.add("The digital signature on the benchmark you've selected is invalid.  This typically indicates that the benchmark policy has been modified.");
                    return CiscatConstants.ERROR_XML_SIGNATURE;
                }
            } else {
                _logger.warn("CiscatSchemaValidator::validateXmlSignature (Element) -- Unable to find signature in benchmark. All benchmarks must be signed...");
                _errors.add("Unable to find signature in benchmark. All benchmarks must be signed");
                return CiscatConstants.ERROR_XML_SIGNATURE;
            }
        } catch(Exception ex) {
            _logger.warn("CiscatSchemaValidator::validateXmlSignature (Element) -- Unable to verify signature for benchmark...", ex);
            _errors.add("The digital signature on the benchmark you've selected is invalid.  This typically indicates that the benchmark policy has been modified.");
            return CiscatConstants.ERROR_XML_SIGNATURE;
        }
        _logger.info("END -- CIS-CAT Schema Validator :: validateXmlSignature");
        return CiscatConstants.SUCCESS;
    }

    /**
     * validate documents referenced by the enclosing document, used to validate
     * OVAL sub-documents referenced by XCCDF benchmarks
     * @param uri
     * @param nodeList
     * @return
     */
    private int validateOvalSubDocuments(ArrayList<Document> ovalSubdocuments) {
        _logger.info("START -- CIS-CAT Schema Validator :: validateOvalSubDocuments");

        // Legacy OVAL 5.3/4 Schemas...
        Source[] legacyOval53Schemas = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.4.xsd").toString())
        };
        
        // Legacy OVAL 5.8 Schemas...
        Source[] scap11Oval58Schemas = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.8.xsd").toString())
        };
        
        // OVAL 5.10 & 5.10.1 Schemas...
        Source[] oval510Schemas      = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.10.1.xsd").toString())
        };
        
        // OVAL 5.11 Schemas...
        Source[] oval511Schemas      = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.11.xsd").toString())
        };
        
        // OVAL 5.11.1 Schemas...
        Source[] oval5111Schemas     = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.11.1.xsd").toString())
        };
        
        // OVAL 5.11.2 Schemas...
        Source[] oval5112Schemas     = {
            new StreamSource(getClass().getResource("validator-oval-definitions-5.11.2.xsd").toString())
        };

        for (Document currOvalSubdocument : ovalSubdocuments) {
            if (currOvalSubdocument.getDocumentElement().getAttribute("xmlns:oval") != null) {
                // Try to validate the file then...

                _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Getting OVAL schema version...");
                String schema_version =
                    XPathUtilities.asString(
                        currOvalSubdocument,
                        "/oval:oval_definitions/oval:generator/oval-common:schema_version",
                        new OvalNamespaceContext());
                _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Found schema_version = '" + schema_version.toString() + "'...");

                Source[] schemas = null;

                final String LEGACY_MAX   = "5.4";
                final String SCAP11_MAX   = "5.8";
                final String OVAL510_MAX  = "5.10.1";
                final String OVAL511_MAX  = "5.11";
                final String OVAL5111_MAX = "5.11.1";
                VersionComparator vc = new VersionComparator();

                ResultEnumeration.Enum legacy   = vc.compare(schema_version, LEGACY_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
                ResultEnumeration.Enum scap11   = vc.compare(schema_version, SCAP11_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
                ResultEnumeration.Enum oval510  = vc.compare(schema_version, OVAL510_MAX, OperationEnumeration.LESS_THAN_OR_EQUAL);
                ResultEnumeration.Enum oval511  = vc.compare(schema_version, OVAL511_MAX, OperationEnumeration.EQUALS);
                ResultEnumeration.Enum oval5111 = vc.compare(schema_version, OVAL5111_MAX, OperationEnumeration.EQUALS);

                if (legacy == ResultEnumeration.TRUE) {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.3/4 schemas...");
                    schemas = legacyOval53Schemas;
                } else if (scap11 == ResultEnumeration.TRUE) {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.8 schemas...");
                    schemas = scap11Oval58Schemas;
                } else if (oval510 == ResultEnumeration.TRUE) {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.10 schemas...");
                    schemas = oval510Schemas;
                } else if (oval511 == ResultEnumeration.TRUE) {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.11 schemas...");
                    schemas = oval511Schemas;
                } else if (oval5111 == ResultEnumeration.TRUE) {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.11.1 schemas...");
                    schemas = oval5111Schemas;
                } else {
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validating against OVAL 5.11.2 schemas...");
                    schemas = oval5112Schemas;
                }

                try {
                    Schema tmpSchema =
                        SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema").newSchema(schemas);

                    tmpSchema.newValidator().validate(new DOMSource(currOvalSubdocument));
                    
                    _logger.info("CiscatSchemaValidator::validateOvalSubDocuments -- Validation Succeeded.");
                } catch (SAXException ex) {
                    String errorMessage =
                        "An OVAL definitions file referenced by the selected benchmark is invalid according to its schema." + ex.getLocalizedMessage();
                    _logger.warn(errorMessage, ex);
                    _errors.add(errorMessage);
                    return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
                } catch (IOException io) {
                    _logger.warn("Error loading OVAL schemas for validation -- " + io.getLocalizedMessage());
                    _errors.add("Error loading OVAL schemas for validation -- " + io.getLocalizedMessage());
                    return CiscatConstants.ERROR_OVAL_SUB_DOCUMENTS;
                }

            }
        }
        _logger.info("END -- CIS-CAT Schema Validator :: validateOvalSubDocuments");
        return CiscatConstants.SUCCESS;
    }

    /**
     * Hash the certificate value
     * @param cert
     * @return
     * @throws NoSuchAlgorithmException
     * @throws CertificateEncodingException
     */
    private String getCertificateThumbprint(X509Certificate certificate) throws NoSuchAlgorithmException, CertificateEncodingException {
        _logger.info("CiscatSchemaValidator::getCertificateThumbprint -- [START]");

        Scap12HashUtilities hashUtilities = new Scap12HashUtilities();

        String certificateHash = hashUtilities.computeCertificateHash(
            certificate,
            Scap12HashUtilities.HashAlgorithm.SHA1);

        _logger.info("CiscatSchemaValidator::getCertificateThumbprint -- [ END ]");
        return certificateHash;
    }
}

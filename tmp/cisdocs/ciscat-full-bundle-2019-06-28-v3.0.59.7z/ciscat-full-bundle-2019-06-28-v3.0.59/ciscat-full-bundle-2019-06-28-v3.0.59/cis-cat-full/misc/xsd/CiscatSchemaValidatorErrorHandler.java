
package org.cisecurity.tools.ciscat.xsd;

import java.util.ArrayList;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

/**
 * Log and collect errors resulting from Schema Validation
 * @author bmunyan
 */
public class CiscatSchemaValidatorErrorHandler implements ErrorHandler {
    private Logger _logger = LogManager.getLogger("org.cisecurity.tools.ciscat.base");

    private ArrayList<String> _errors = new ArrayList<String>();

    /**
     * Constructor
     */
    public CiscatSchemaValidatorErrorHandler() {
        _errors.clear();
    }

    /**
     * @return if any error messages have been collected
     */
    public boolean isError() {
        return (_errors.size() > 0);
    }

    /**
     * @return the list of collected error messages
     */
    public ArrayList<String> getErrors() {
        return _errors;
    }

    /**
     * Catch errors -- Log them...
     * @param exception
     * @throws SAXException
     */
    public void error(SAXParseException exception) throws SAXException {
        _logger.warn("CiscatSchemaValidatorErrorHandler::error -- Caught [ERROR] - " + exception.getLocalizedMessage());
        _errors.add(buildMessage(exception));
    }

    /**
     * Catch Fatal Errors -- Log them...
     * @param exception
     * @throws SAXException
     */
    public void fatalError(SAXParseException exception) throws SAXException {
        _logger.warn("CiscatSchemaValidatorErrorHandler::error -- Caught [FATAL ERROR] - " + exception.getLocalizedMessage());
        _errors.add(buildMessage(exception));
    }

    /**
     * Catch warnings...
     * @param exception
     * @throws SAXException
     */
    public void warning(SAXParseException exception) throws SAXException {
        _logger.warn("CiscatSchemaValidatorErrorHandler::error -- Caught [WARNING] - " + exception.getLocalizedMessage());
    }

    //
    // ------------ PRIVATE METHODS --------------
    //

    /**
     * Construct the error message
     * @param exception
     * @return
     */
    private String buildMessage(SAXParseException exception) {
        StringBuilder sb = new StringBuilder();

        sb.append(exception.getLocalizedMessage());

        return sb.toString();
    }
}

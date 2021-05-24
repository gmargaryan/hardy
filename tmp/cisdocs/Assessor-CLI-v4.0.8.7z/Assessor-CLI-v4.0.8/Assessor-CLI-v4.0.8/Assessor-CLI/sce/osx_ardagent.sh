#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Disable Remote Management
# 

output=$(
ps -ef | egrep ARDAgent
)

# If result returns fail, otherwise pass.
if [ "$output" == *"/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents"* ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
else
    # passing
    echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
fi

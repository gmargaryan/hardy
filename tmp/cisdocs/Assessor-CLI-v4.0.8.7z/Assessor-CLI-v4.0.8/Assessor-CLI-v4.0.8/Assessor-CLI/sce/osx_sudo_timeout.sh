#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Reduce the sudo timeout period
# 

output=$(
sudo cat /etc/sudoers | grep timestamp 
)

# If results returns pass, otherwise fail.
if [ "$output" == "Defaults timestamp_timeout=0" ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
fi

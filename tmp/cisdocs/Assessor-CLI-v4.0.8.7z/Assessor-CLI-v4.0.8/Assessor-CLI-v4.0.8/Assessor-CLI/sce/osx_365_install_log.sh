#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Retain install.log for 365 or more days
# 

output=$(
grep -i ttl /etc/asl/com.apple.install  
)

# If results returns pass, otherwise fail.
if [ "$output" == "* file /var/log/install.log mode=0640 format=bsd rotate=utc compress file_max=5M ttl=365" ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
fi

#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Ensure security auditing retention
# 

output=$(
sudo cat /etc/security/audit_control | egrep expire-after
)

# If either result returns pass, otherwise fail.
if [ "$output" == "expire-after:60D" ] || [ "$output" == "expire-after:1G" ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
fi

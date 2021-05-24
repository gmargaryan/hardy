#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Configure Security Auditing Flags
# 

output=$(
sudo egrep "^flags:" /etc/security/audit_control
)

# If results returns pass, otherwise fail.
if [ "$output" == "flags:lo,aa,fd,fm,-all" ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
fi

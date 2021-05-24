#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Ensure EFI version is valid and being regularly checked
# 

output=$(
/usr/libexec/firmwarecheckers/eficheck/eficheck --integrity-check |  awk 'NR==2'
)

# If result contains string pass, otherwise fail.
if [ "$output" == "Primary allowlist version match found. No changes detected in primary hashes." ] ; then
	echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
fi


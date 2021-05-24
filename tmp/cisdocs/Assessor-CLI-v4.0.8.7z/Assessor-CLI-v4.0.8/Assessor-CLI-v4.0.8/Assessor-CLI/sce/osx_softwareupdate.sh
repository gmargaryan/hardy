#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Ensure Software is up to date
# 

output=$(
softwareupdate -l
)

# If result returns software updates fail, otherwise pass.
if [ "$output" == *"Software Update found the following new or updated software:"* ]; then
	echo "$output"
    exit "${XCCDF_RESULT_FAIL:-102}"
else
    # print the reason why we are failing
    echo "$output"
    exit "${XCCDF_RESULT_PASS:-101}"
fi


output=$(softwareupdate -l)
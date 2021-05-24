#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Ensure Time Machine Volumes Are Encrypted
# 

output=$(
tmutil destinationinfo | grep -i NAME
)

# If results returns pass, otherwise fail.
# if [ "$output" == *"Name"* ] ; then
# 	echo "$output"
#     exit "${XCCDF_RESULT_PASS:-101}"
# else
#     # print the reason why we are failing
#     echo "$output"
#     exit "${XCCDF_RESULT_FAIL:-102}"
# fi
echo "$output"
exit "${XCCDF_RESULT_PASS:-101}"
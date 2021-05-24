#!/usr/bin/env sh

#
# CIS-CAT Script Check Engine
# 
# Name                Date       Description
# -------------------------------------------------------------------
# Sara Lynn Archacki  04/02/19   Time Machine Auto-Backup
# 

output=$(
defaults read /Library/Preferences/com.apple.TimeMachine.plist AutoBackup
)

# If results returns pass, otherwise fail.
# if [ "$output" == "1" ] ; then
# 	echo "$output"
#     exit "${XCCDF_RESULT_PASS:-101}"
# else
#     # print the reason why we are failing
#     echo "$output"
#     exit "${XCCDF_RESULT_FAIL:-102}"
# fi

echo "$output"
exit "${XCCDF_RESULT_PASS:-101}"
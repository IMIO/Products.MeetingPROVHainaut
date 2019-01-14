#!/bin/sh
/srv/archgenxml/archgenxml-2.7/bin/archgenxml --cfg generate.conf MeetingCPASLalouviere.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/meetingbplalouviere_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingitembplalouviere_workflow ../profiles/default/workflows
rm -rf tmp

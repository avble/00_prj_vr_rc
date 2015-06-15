#!/bin/sh 
curl -X GET  http://192.168.1.108:5000/device/getDevicesFromNetwork/networkID1 --header "Content-Type:text/xml"

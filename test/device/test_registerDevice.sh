#!/bin/sh
curl -X POST -d @$1 http://115.77.49.188:5000/device/registerDevice --header "Content-Type:text/xml"
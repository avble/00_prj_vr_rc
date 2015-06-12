#!/bin/sh
curl -X POST -d @$1 http://172.16.1.67:5000/device/registerDevice --header "Content-Type:text/xml"

#!/bin/bash
while true
do
	turnserver --server-relay -v -X 115.77.49.188	
	sleep 4
	turnadmin -k -u 100 -r 100 -p 100 
	echo "Re-run server ..... "
	sleep 10
done

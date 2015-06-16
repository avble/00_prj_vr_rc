from flask import Flask
from flask import request
import device, peer
import os, sys 

app = Flask(__name__)


@app.route('/')
def index():
	return 'index page' 

@app.route('/helloworld', methods = ['POST', 'GET'])
def helloworld():
	return 'hello world' 

@app.route('/device/registerDevice', methods = ['POST'])
def uri_device_register():
	if device.device_register(request.data) != 0:
        	return 'register device fail \n', 201
	else: 
		return 'register device successful \n' 

@app.route('/device/getDevice', methods = ['GET'])
def uri_device_get():
	return 'register device' 

@app.route('/device/resetDevice/<uniqueId>', methods = ['POST'])
def uri_device_reset(uniqueId):
	#return 'reset device successfully'
	# show the post with the given id, the id is an integer
	if device.device_reset(uniqueId) == 0:
		return 'reset device successfully'
	else:
		return 'reset device fail'


@app.route('/device/getDevicesFromNetwork/<NetworkID>', methods = ['GET'])
def uri_device_get_devices_from_network(NetworkID):
	return device.device_get_device_from_networkid(NetworkID)



##### peer service #################
@app.route('/peer/registerPeer', methods = ['POST'])
def uri_device_peer():
	if peer.device_peer(request.data) != 0:
        	return 'register device fail \n', 201
	else: 
		return 'register device successful \n' 



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5001)

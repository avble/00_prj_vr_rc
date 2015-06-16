from flask import Flask
from flask import request
import device, peer
import os, sys 
from flask import render_template

app = Flask(__name__)



################################################
##### common API #################
def get_data_from_post_request(rq):
	data_all = ''
	data = rq.stream.read()
	while len(data_all) < rq.content_length:
		data_all += data
		data = rq.stream.read()
	return data_all

################################################
##### for testing purpose #################
@app.route('/')
def index():
	return 'index page' 

@app.route('/helloworld', methods = ['POST', 'GET'])
def helloworld():
	return 'hello world' 


@app.route('/helloworld1', methods = ['POST', 'GET'])
def helloworld1():
	print get_data_from_post_request(request)
	return "OK"

################################################
##### device service #################

@app.route('/device/registerDevice', methods = ['POST', 'GET'])
def uri_device_register():
	data = get_data_from_post_request(request)
	if device.device_register(data) != 0:
        	return 'register device fail \n', 201
	else: 
		return 'register device successful \n' 

@app.route('/device/getDevice/<deviceID>', methods = ['GET'])
def uri_device_get(deviceID):
	return device.device_getDevice(deviceID)

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


################################################
##### peer service #################

@app.route('/peer/registerPeer', methods = ['POST'])
def uri_peer_register():
	data = get_data_from_post_request(request)
	print "[Debug] : ", data
	if peer.peer_register(data) != 0:
        	return 'register peer fail \n', 201
	else: 
		return 'register peer successful \n' 

@app.route('/peer/resetPeer/<uniqueId>', methods = ['POST'])
def uri_peer_reset(uniqueId):
	#return 'reset device successfully'
	# show the post with the given id, the id is an integer
	if peer.peer_reset(uniqueId) == 0:
		return 'reset device successfully'
	else:
		return 'reset device fail'


@app.route('/peer/getPeer/<deviceID>', methods = ['GET'])
def uri_peer_get(deviceID):
	return peer.peer_getDevice(deviceID)


################################################
### view page 

@app.route('/view/')
def view_page():
    return render_template('view.html')




if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5001)


from flask import Flask
from flask import request
import device

app = Flask(__name__)


@app.route('/')
def index():
	return 'index page' 

@app.route('/helloworld', methods = ['POST', 'GET'])
def helloworld():
	return 'hello world' 

@app.route('/device/registerDevice', methods = ['POST'])
def device_register():
	if device.device_register(request.data) != 0:
        	return 'register device fail \n', 201
	else: 
		return 'register device successful \n' 

@app.route('/device/getDevice', methods = ['GET'])
def device_get():
	return 'register device' 

@app.route('/device/resetDevice', methods = ['POST'])
def device_reset():
	# show the post with the given id, the id is an integer
	return 'reset device' 

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0')

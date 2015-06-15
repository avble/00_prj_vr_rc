from flask import Flask
app = Flask(__name__)

#@app.route('/helloworld/')
#def helloworld():
#	return "hello world" 

@app.route('/')
def index():
    return 'index page\n' 

@app.route('/helloworld', methods = ['POST', 'GET'])
def helloworld():
    return 'hello world\n' 

@app.route('/device/registerDevice', methods = ['POST'])
def device_register():
    return 'register device' 

@app.route('/device/resetDevice', methods = ['POST'])
def device_reset():
    # show the post with the given id, the id is an integer
    return 'reset device' 

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')

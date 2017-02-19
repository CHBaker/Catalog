# import flask class from Flask library
from flask import Flask
# create instance of flask class with name of app as argument
app = Flask(__name__)

# decorators wrap pre-defined flask functions to execute
# Helloworld if either route is requested
@app.route('/')
@app.route('/hello')
def HelloWorld():
	return "Hello World!"

# main app running is named __main__ all others named __name__
if __name__ == '__main__':
	# reloads page when code changes
	app.debug = True
	# runs unless this file is imported
	app.run(host = '0.0.0.0', port = 5000)
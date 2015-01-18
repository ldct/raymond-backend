#!/usr/bin/env python

import binascii, os

import bottle
from bottle import response, request

from binascii import unhexlify

@bottle.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@bottle.get('/')
def health():
    response.content_type = 'application/json'
    if os.path.isdir("./task_data"):
        return { 'status': 'ok' }
    else:
        return {
            'status': 'bad',
            'message': 'task_data directory does not exist'
	}
@bottle.post('/task')
def create_task():
    response.content_type = 'application/json'

    task_id = binascii.hexlify(os.urandom(8))

    print(request.query.get('category'))

    os.mkdir('./task_data/' + task_id)
    with open('./task_data/' + task_id + '/status', 'a') as f:
        f.write('queued\n')

    s = request.body.read()

    with open('./task_data/' + task_id + '/image.jpg', 'wb') as f:
        f.write(s)

    return task_id

@bottle.get('/task_data/<filename:path>')
def get_task_data(filename):
    return bottle.static_file(filename, root='./task_data')

@bottle.get('/tasks')
def list_tokens():
    response.content_type = 'application/json'
    return {
        'tasks': os.listdir('./task_data')
    }

@bottle.get('/tasks.html')
def list_tokens():

    def make_li(dirname):
        return "<li > <a href='/task_data/%s/status'> %s </a> </li>" % (dirname, dirname)

    response.content_type = 'text/html'
    return """
    <h1> Hi </h1>

    <ol>

    """ + \
    " ".join(make_li(dirname) for dirname in os.listdir('./task_data')) + \
    """

    </ol>

    """

@bottle.get('/task/<name>')
def get_task(name):
    with open ('./task_data/' + name + '/status', 'r') as f:
        return '\n'.join(f.readlines())

try:
    bottle.run(host='0.0.0.0', port=80, debug=False )
except:
    bottle.run(host='localhost', port=8080, debug=True)

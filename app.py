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
    if os.path.isdir("./tasks"):
        return { 'status': 'ok' }
    else:
        return {
            'status': 'bad',
            'message': 'tasks directory does not exist'
	}
@bottle.post('/task')
def create_task():
    response.content_type = 'application/json'

    task_id = binascii.hexlify(os.urandom(8))

    os.mkdir('./tasks/' + task_id)
    with open('./tasks/' + task_id + '/status', 'a') as f:
        f.write('queued')

    s = request.body.read()
    print(s)

    with open('./tasks/' + task_id + '/image.jpg', 'wb') as f:
        f.write(s)

    return task_id

@bottle.get('/tasks')
def list_tokens():
    response.content_type = 'application/json'
    return os.listdir('./tasks')

@bottle.get('/task/<name>')
def get_task(name):
    with open ('./tasks/' + name + '.status', 'r') as f:
        return '\n'.join(f.readlines())

try:
    bottle.run(host='0.0.0.0', port=80, debug=False )
except:
    bottle.run(host='localhost', port=8080, debug=True)

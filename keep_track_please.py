import zmq
import time
import sys
import json
import urllib2
from firebase import firebase

firebase = firebase.FirebaseApplication('https://blistering-fire-9098.firebaseio.com', None)

port = "5519"

context = zmq.Context()
socket  = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
while True:
    js = socket.recv_json()
    result = firebase.post('/', js)
    print "New thing to keep track of "+ str(js)
    time.sleep(.1)
    socket.send("Got it thanks!")

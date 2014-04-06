import zmq
context = zmq.Context()
print "connect to server"
port = "5519"
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)

#js = pickle.load( open( "json.txt", "rb" ) )
for request in range(1):
    socket.send_json({u'email': u'dax.earl@gmail.com',
  u'min': 7,
  u'thread': u'http://www.reddit.com/r/hackpsu_easyama/comments/22abfi/random_new_post/',
  u'trigger': u'count'})
    message = socket.recv()
    print "recieved reply " ,"[",message,"]"

from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, send
from cameraLaptop import Camera
from robot import Robot
from warehouse import Warehouse

app = Flask(__name__)

socketio = SocketIO(app)
button = 0


#Array to hold instances of robots
startX = 0
startY = 0
robotArray = []

#Double Array to represent the warehouse
warehouse = Warehouse(2,3)

#Returns the robot with session id sid from robotArray
def getRobot(sid, robotArray):
	for r in robotArray:
		if(r.getId() == sid):
			return r
	print("No robot with sid " + sid + " exists")

def talkToRobot(command):
	if (command == 'Up'):
		send('up pressed', broadcast=True)
	if (command == 'down'):
		send('down pressed', broadcast=True)
	if (command == 'right'):
		send('right pressed', bradcast=True)
	if (command == 'left'):
		send('left pressed', broadcast=True)

@socketio.on('connect', namespace='/robot')
def handleRobotConnect():
	robotArray.append(Robot(request.sid, startX,startY))
	warehouse.addRobot(startX,startY)
	print('Robot ' + robotArray[len(robotArray)-1].getId() + ' joins the warehouse!')

@socketio.on('disconnect', namespace='/robot')
def handleRobotDisconnect():
	for i,r in enumerate(robotArray):
		if(robotArray[i].getId() == request.sid):
			pos = r.getPosition()
			warehouse.removeRobot(pos[0], pos[1])
			print('Robot ' + robotArray[i].getId() + ' leaves the warehouse!')
			robotArray.pop(i)

@socketio.on('connect', namespace='/camera')
def handleCameraConnect():
	print('Camera connected!')

@socketio.on('message')
def handleMessage(msg):
	print('session id: ' + request.sid)
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('manual request')
def handleManualReq():
	global button
	if(button == 0):
		msg = " take control"
		button = request.sid
		send(msg, broadcast=True)
   
	elif (request.sid != button):
		send("Occupied")
   
	else:
		send("released")
		button = 0

@socketio.on('command')
def handleCommand(msg):
	if(button == 0):
		msg = "need to take control first"
		send(msg, broadcast=True)
		return

	c = msg['command']
	#Temporary ack
	ack = '1234'
	socketio.emit('move', {'id' : ack, 'command' : c}, namespace= '/robot')
	send(c, broadcast=True)

	while True:
		@socketio.on('result')
		def handleResult(msg):
			if(msg['re-id'] == ack):
				if(msg['status'] == 'successful'):
					send(msg['status'], broadcast=True)
					r = getRobot(request.sid, robotArray)
					pos1 = r.getPosition()
					if(c == 'move-straight'):
						pos2 = r.nextMove()
						if(warehouse.moveRobot(pos1,pos2)):
							r.move()
						warehouse.showWarehouse()
					if(c == 'drop'):
						r.drop()
					if(c == 'pick up'):
						r.pickup()
					else:
						r.turn(c)
				else:
					send(msg['status'], broadcast=True)
		break


@app.route('/')
def index():
	return render_template('index.html')


#TUTORIAL BORJAR HAR
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	socketio.emit('send img')
	@socketio.on('return frame')
	def handleFrame(frame):

		return Response(frame,
			mimetype='multipart/x-mixed-replace; boundary=frame')
#TUTORIAL SLUTAR HAR



if __name__ == '__main__':
	socketio.run(app, host = "192.168.1.106", debug = True)


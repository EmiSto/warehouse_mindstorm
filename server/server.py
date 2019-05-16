from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit, join_room, rooms
from warehouse import Warehouse
import json

#CAMERA imports
import numpy as np
import cv2
import base64

# import redis
# r = redis.Redis(host='localhost', port=6379, db=0)

# Change this base on host ip network address
host = '130.243.223.214'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initial online dict, dictionary of robot and it's state
status_dict = {}

# An object to represent the warehouse
wh = Warehouse(4,4)

#======================================================================
# Server get any connect or disconnect request, then update the online 
# list to client

@socketio.on('connect')
def connect():
    emit('server_update_status', status_dict, broadcast=True)
    print('connected')


@socketio.on('disconnect')
def disconnect():
    for room_id in status_dict.keys():
        if room_id in rooms():
            #Remove the robot from the warehouse map
            x = status_dict[room_id]['robot_x_pos']
            y = status_dict[room_id]['robot_y_pos']
            wh.removeRobot(x,y)
            status_dict.pop(room_id)
            break

    print(rooms())   
    emit('server_update_status', status_dict, broadcast=True)
    print('disconnected')

#======================================================================


#=======================================================================
# Server take request from client

@socketio.on('client_command')
def client_command(request):
    robot_id = request.get('robot_id')
    command = request.get('command')
    payload = request.get('payload')

    if payload is None:
        server_robot_manual(command, robot_id)
    else:
        server_robot_auto(command, payload, robot_id)

#=======================================================================


#======================================================================
# Server process the request from client and then send command to robot

def server_robot_manual(command, robot_id):
    '''
    if command == 'move_forward':
        request_object = {
            'command': 'move_forward'
        }
    elif command == 'move_backward':
        request_object = {
            'command': 'move_backward'
        }
    elif command == 'move_right':
        request_object = {
            'command': 'move_right'
        }
    elif command == 'move_left':
        request_object = {
            'command': 'move_left'
        }
    elif command == 'pick':
        request_object = {
            'command': 'pick'
        }
    elif command == 'drop':
        request_object = {
            'command': 'drop'
        }

    
    elif command == 'turn_right':
        request_object = {
            'command': 'turn_right'
        }
    elif command == 'turn_left':
        request_object = {
            'command': 'turn_left'
        }
    '''
    request_object = { 'command': command}
    emit('server_command_robot', request_object, room=robot_id)


def server_robot_auto(command, payload, robot_id):
    if command == 'delivery':
        start = payload.get('start')
        end = payload.get('end')
        # TODO: process the request and send continously command to robot
        # to get and drop the object without crashing

#======================================================================


#=======================================================================
# Server take request from robot

@socketio.on('robot_status')
def robot_update_status(request):
    robot_id = request.get('robot_id')
    robot_direction = request.get('robot_direction')
    robot_x_pos = request.get('robot_x_pos')
    robot_y_pos = request.get('robot_y_pos')
    robot_payload = request.get('robot_payload')
    robot_status = request.get('robot_status')

    # Update the onlines dict and return to client
    join_room(robot_id)

    #Remove robots current position from the warehouse map
    if(robot_status == 1):
        wh.removeRobot(robot_x_pos,robot_y_pos)

    status_dict[robot_id] = {
        'robot_direction': robot_direction,
        'robot_x_pos': robot_x_pos,
        'robot_y_pos': robot_y_pos,
        'robot_payload': robot_payload,
        'robot_status': robot_status
    }
    
    #Add robot at its position on the wharehouse map
    if(robot_status == 0):
        wh.addRobot(robot_x_pos,robot_y_pos)
        #TODO:UPDATE BROWSER CLIENT ABOUT NEW POSITION
        socketio.emit('moveRobot', {'direction' : robot_direction})

    print('>>>>>>>>>>>>>>>>>>>>', status_dict)
    wh.showWarehouse()
    emit('server_update_status', status_dict, broadcast=True)

#=======================================================================


#=======================================================================
# Server takes request from camera client

frame = None

#When camera client has connected server asks for images
@socketio.on('connect', namespace = '/camera')
def handleCameraConnect():
    print('Camera connected')
    socketio.emit('send frame', namespace = '/camera')

#Client returns frames one at a time which server decodes
# and shows
#TODO: send the frame to the browser client
@socketio.on('return frame', namespace='/camera')
def handleFrame(frame):
    print("=========frame got through----------")
    frame = frame['data']
    socketio.emit('show img', {'data' : frame})
    frame = np.frombuffer(frame, np.uint8)
    frame = cv2.imdecode(frame, 3)

    bFrame = base64.b64encode(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    socketio.emit('send img', {'data': bFrame})
    #frame = (b'--frame\r\n'
              # b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')



#======================================================================




@app.route('/')
def get_index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host=host, debug=True)
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, rooms
import json

# import redis
# r = redis.Redis(host='localhost', port=6379, db=0)

# Change this base on host ip network address
host = '192.168.1.188'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initial online dict, dictionary of robot and it's state
status_dict = {}

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
    robot_status = request.get('robot_status')

    # Update the onlines dict and return to client
    join_room(robot_id)

    status_dict[robot_id] = {
        'robot_direction': robot_direction,
        'robot_x_pos': robot_x_pos,
        'robot_y_pos': robot_y_pos,
        'robot_status': robot_status
    }
    print('>>>>>>>>>>>>>>>>>>>>', status_dict)

    emit('server_update_status', status_dict, broadcast=True)

#=======================================================================


@app.route('/')
def get_index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host=host, debug=True)
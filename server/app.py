from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, join_room, rooms
from auto import *
import cv2


# Change this base on host ip network address
host = '0.0.0.0'
port = 80

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# global vars
status_dict = {}
command_list = list()
path = list()
current_index = 0   # current position : path[current_index]
is_picking = False
is_finished = False

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


# In auto mode, we have to initialize starting point, head point, and target point
# head point is the point right in front of robot
# in other word, the init direction of robot is starting point -> head point
@socketio.on('init_points')
def init_point(data):
    print(data)
    start_point = data.get('start_point')
    head_point = data.get('head_point')
    target_point = data.get('target_point')
    robot_id = data.get('robot_id')

    xy_start_point = start_point.split(',')
    x_start_point = int(xy_start_point[0])
    y_start_point = int(xy_start_point[1])

    xy_head_point = head_point.split(',')
    x_head_point = int(xy_head_point[0])
    y_head_point = int(xy_head_point[1])

    xy_target_point = target_point.split(',')
    x_target_point = int(xy_target_point[0])
    y_target_point = int(xy_target_point[1])

    start_point = (x_start_point, y_start_point)
    head_point = (x_head_point, y_head_point)
    target_point = (x_target_point, y_target_point)

    payload = {
        'x_start_point': x_start_point,
        'y_start_point': y_start_point
    }

    emit('init_robot', payload, room=robot_id)

    global current_index, path, command_list

    command_list, path = run(start_point, head_point, target_point)

    print(command_list)
    print(path)
    print('command robot: ' + str(command_list[current_index]))
    command_robot_auto(command_list[current_index], path[current_index+1], robot_id)


#=======================================================================
# Server take request from client

@socketio.on('client_command')
def client_command(request):
    print('client command')
    robot_id = request.get('robot_id')
    command = request.get('command')

    commands = [command]

    print(request)
    command_robot_manual(commands, robot_id)

#=======================================================================



#======================================================================

# for auto control
def command_robot_auto(commands, next_point, robot_id):
    payload = {
        'commands': commands,
        'next_point': next_point
    }
    print(payload)
    emit('server_command_robot', payload, room=robot_id)

# Server process the request from client and then send command to robot
def command_robot_manual(commands, robot_id):
    payload = {
        'commands': commands
    }
    print(payload)
    emit('server_command_robot', payload, room=robot_id)

#======================================================================


#=======================================================================
# Server take request from robot

@socketio.on('robot_status')
def robot_update_status(request):
    global current_index, path, command_list, is_picking, is_finished

    robot_id = request.get('robot_id')
    # robot_direction = request.get('robot_direction')
    robot_x_pos = request.get('robot_x_pos')
    robot_y_pos = request.get('robot_y_pos')
    robot_status = request.get('robot_status')

    # Update the onlines dict and return to client
    join_room(robot_id)

    status_dict[robot_id] = {
        'robot_x_pos': robot_x_pos,
        'robot_y_pos': robot_y_pos,
        'robot_status': robot_status
    }
    print('>>>>>>>>>>>>>>>>>>>>', status_dict)

    emit('server_update_status', status_dict, broadcast=True)

    # Command robot to go on
    if robot_status == 0:
        # not reach the destination yet
        if current_index < len(path) - 2:
            current_index += 1
            print(current_index)
            print('command robot: ' + str(command_list[current_index]))
            command_robot_auto(command_list[current_index], path[current_index+1], robot_id)

        # robot reached the destination and pick object
        elif current_index == len(path) - 2:
            current_index += 1
            print(current_index)
            print('robot' + robot_id + ' reached destination')
            if is_picking is False:
                commands = ['pick']
                is_picking = True
            else:
                commands = ['drop']
                is_finished = True

            command_robot_auto(commands, path[current_index], robot_id)

        # robot picked object and come back
        else:
            if is_finished is False:
                print('come back...')
                current_index = 0
                path_length = len(path)
                # head_point = get_head_point(path[path_length - 2], path[path_length -1])
                command_list, path = run(path[path_length-1], path[path_length-2], path[0])
                print(command_list)
                print(path)
                command_robot_auto(command_list[current_index], path[current_index + 1], robot_id)

#=======================================================================


def generate_frame():
    # for external camera app
    camera_ip = '192.168.1.167'
    cap = cv2.VideoCapture('http://' + camera_ip + ':8080/video')

    # for webcam
    # cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, host=host, port=port, debug=True)
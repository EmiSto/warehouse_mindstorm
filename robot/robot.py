import sys
import socketio
import json

sio = socketio.Client()

# Change this base on host ip network address 
host = '130.243.234.142'

robot = {}
robot['id'] = sys.argv[1]   # unique robot id
robot['direction'] = 0  # 4 directions: 0=UP,1=RIGHT,2=DOWN,3=LEFT
robot['x'] = 0
robot['y'] = 0  
robot['payload'] = 0 #0 if not holding item, 1 if holding item
robot['status'] = 0 # 0 is not busy, 1 is busy

is_fake = sys.argv[2]


if is_fake == 'fake':
    from fake_take_action import command_robot
else:
    from take_action import command_robot


def get_robot_status():
    print(robot['status'])
    response_object = {
        'robot_id': robot['id'],
        'robot_direction': robot['direction'],
        'robot_x_pos': robot['x'],
        'robot_y_pos': robot['y'],
        'robot_payload' : robot['payload'],
        'robot_status': robot['status'],
    }
    return response_object

# updating status of the robot depending on the command
# assuming move right and move left only turns the robot and does not move
def update_robot_status(command):
    if(command == 'move_forward'):
        move()
    elif(command == 'move_backward'):
        robot['direction'] = (robot['direction'] - 2) % 4
        move()
    elif(command == 'move_right'):
        robot['direction'] = (robot['direction'] + 1) % 4
        move()
    elif(command == 'turn_right'):
        robot['direction'] = (robot['direction'] + 1) % 4
    elif(command == 'move_left'):
        robot['direction'] = (robot['direction'] - 1) % 4
        move()
    elif(command == 'turn_left'):
        robot['direction'] = (robot['direction'] - 1) % 4
    elif(command == 'pick' and robot['payload'] == 0):
        robot['payload'] = 1
    elif(command == 'drop' and robot['payload'] == 1):
        robot['payload'] = 0
    else:
        print("Something went wrong with update_status")
    
def move():
    if(robot['direction'] == 0):
        robot['y'] += 1
    elif(robot['direction'] == 1):
        robot['x'] += 1
    elif(robot['direction'] == 2):
        robot['y'] -= 1
    else:
        robot['x'] -= 1

@sio.on('connect')
def on_connect():
    print('connected to server')
    response_object = get_robot_status()
    sio.emit('robot_status', response_object)


@sio.on('disconnect')
def on_disconnect():
    print('disconnected to server')


@sio.on('server_command_robot')
def process_command(request):
    if robot['status'] == 0:
        # At first, notify all client that robot is busy
        robot['status'] = 1
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)
        
        command = request.get('command')
        print(">>> command from server: ", command)
        #Update status of robot. If fake run the update_robot_status
        # else the robot will give the new results
        #TODO: add if robot has payload for the automatic part
        if(sys.argv[2] == 'fake'):
            update_robot_status(command)
        else:
            direction, x_pos, y_pos = command_robot(command)
            robot['direction'] = direction
            robot['x'] = x_pos
            robot['y'] = y_pos
        
        # After finish, send robot status to client
        robot['status'] = 0
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)


sio.connect('http://'+host+':5000')
sio.wait()
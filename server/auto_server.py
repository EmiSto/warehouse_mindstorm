# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, emit, join_room, rooms
#import json

from astar import astar

maze = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]] # not final size 


class directions: 
    WEST = 'west'
    EAST = 'east'
    NORTH = 'north'
    SOUTH = 'south'
# each point is stored as (x, y) 
def get_direction(current_point, next_point):
    if current_point[0] == next_point[0] and next_point[1] > current_point[1]:
        return directions.EAST
    if current_point[0] == next_point[0] and next_point[1] < current_point[1]:
        return directions.WEST
    if next_point[0] > current_point[0] and next_point[1] == current_point[1]:
        return directions.SOUTH
    if next_point[0] < current_point[0] and next_point[1] == current_point[1]:
        return directions.NORTH

def get_command(current_direction, next_direction):
    command = ''
    turn_left_combinations = [(directions.NORTH, directions.WEST), (directions.WEST, directions.SOUTH), \
        (directions.SOUTH, directions.EAST), (directions.EAST, directions.NORTH)]
    turn_right_combinations = [(directions.NORTH, directions.EAST), (directions.EAST, directions.SOUTH),\
        (directions.SOUTH, directions.WEST), (directions.WEST, directions.NORTH)]
    go_straight_combinations = [(directions.EAST,directions.EAST), (directions.SOUTH,directions.SOUTH), \
        (directions.NORTH, directions.NORTH), (directions.WEST, directions.WEST)]
    go_backward_combinations = [(directions.NORTH, directions.SOUTH), (directions.SOUTH, directions.NORTH), \
        (directions.WEST, directions.EAST), (directions.EAST, directions.WEST)]

    if (current_direction, next_direction) in turn_left_combinations: 
        command = ['turn_left', 'move_forward']
    elif (current_direction, next_direction) in turn_right_combinations: 
        command = ['turn_right', 'move_forward']
    elif (current_direction, next_direction) in go_straight_combinations: 
        command = 'move_forward'
    elif (current_direction, next_direction) in go_backward_combinations: 
        command = 'move_backward' 
    return command

def get_path(starting_point, destination_point): # path must follow the line ( no diagonal )
    astar_path = astar(maze, starting_point, destination_point)
    for i in range(0,len(astar_path)):
        point = astar_path[i]
        next_point =astar_path[i+1]
        if point[0] != next_point[0] and point[1] != next_point[1]:
            astar_path.insert(i+1, (point[1], next_point[0]))
    return astar_path

def run(starting_point, starting_headto_point, destination_point):
    command_list = []
    initial_direction = get_direction(starting_point, starting_headto_point)
    path = get_path(starting_point, destination_point)
    current_direction = initial_direction
    for i in range(0, len(path)):
        current_point = path[i]
        if i < len(path)-1:
            next_point = path[i+1]
        else:
            break 
        next_direction = get_direction(current_point, next_point)
        # print('next direction is: %s' %next_direction)
        command = get_command(current_direction, next_direction)
        command_list.append(command)
        headto_point = ()
        if next_point[0] > current_point[0]:
            headto_point_x = next_point[0] + 1 
            headto_point_y = next_point[1]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[0] < current_point[0]:
            headto_point_x = next_point[0] - 1 
            headto_point_y = next_point[1]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[1] > current_point[1]:
            headto_point_y = next_point[1] + 1
            headto_point_x = next_point[0]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[1] < current_point[1]:
            headto_point_y = next_point[1] - 1
            headto_point_x = next_point[0]
            headto_point = (headto_point_x, headto_point_y)
        # print('head to point is: %s' % (headto_point,))
        current_direction = get_direction(next_point, headto_point)
        # print('current direction is: %s', current_direction)

    return command_list, path

def main():
    starting_point = (0,0)
    starting_headto_point = (0,1)
    destination_point = (2,4)
    command_list = run(starting_point, starting_headto_point, destination_point)
    print(command_list)

if __name__ == '__main__': 
    main()


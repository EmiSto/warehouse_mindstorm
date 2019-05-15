from time import sleep


def moveForward():
    print("move forward")
    sleep(0.2)
    

def moveBackward():
    print("move backward")
    sleep(0.2)
    

def turnLeft():
    print("turn left")
    sleep(0.2)
   

def turnRight():
    print("turn right")
    sleep(0.2)


def handUp():
    print("hand up")
    sleep(0.5)
    

def handDown():
    print("hand down")
    sleep(0.5)


def turn_degree(angle):
    print("turn degree ", angle)
    sleep(0.5)


def PIDControl():
    print("PID control")
    sleep(1)


def moveOutOfGreen():
    print("move out of green")
    sleep(0.1)


def command_robot(command):
    if command == "move_forward":
        moveOutOfGreen()
        PIDControl()
        return True
    if command == "move_backward":
        moveOutOfGreen()
        moveBackward()

        turn_degree(-92)    # turn left
        turn_degree(-92)    # turn left

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "move_left":
        moveOutOfGreen()
        moveBackward()
        
        turn_degree(-92)    # turn left

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "move_right":
        moveOutOfGreen()
        moveForward()

        turn_degree(87)       # turn right

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "pick":
        handUp()
    elif command == "drop":
        moveForward()
        handDown()
        moveBackward()
    elif command == "beep":
        sound.beep()
        return True
    elif command == "turn_right":
        moveOutOfGreen()
        moveForward()

        turn_degree(87)       # turn right
        return True
    elif command == "turn_left":
        moveOutOfGreen()
        moveBackward()
        
        turn_degree(-92)    # turn left
        return True
    return False


print("ROBOT READYYYYYY !!!!")
print('version 3.0')
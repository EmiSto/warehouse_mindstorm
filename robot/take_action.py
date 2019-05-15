from ev3dev2.motor import MoveTank,MoveSteering, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sound import Sound

from time import sleep

# Initial Motor
tank_pair = MoveTank(OUTPUT_A, OUTPUT_D)
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D)
motor = Motor(OUTPUT_B) # small motor

# Initial sound
sound = Sound()

# Initial Sensor
color = ColorSensor()
gyro = GyroSensor()


def moveForward():
    print("move forward")
    tank_pair.on(left_speed=20, right_speed=20)
    sleep(0.1)
    tank_pair.off(brake=False)
    

def moveBackward():
    print("move backward")
    tank_pair.on(left_speed=-20, right_speed=-20)
    sleep(0.1)
    tank_pair.off(brake=False)
    

def turnLeft():
    print("turn left")
    tank_pair.on(left_speed=-20, right_speed=20)
    sleep(0.1)
    tank_pair.off(brake=False)
   

def turnRight():
    print("turn right")
    tank_pair.on(left_speed=20, right_speed=-20)
    sleep(0.1)
    tank_pair.off(brake=False)


def handUp():
    print("hand up")
    motor.on(speed=10)
    sleep(0.5)
    motor.off(brake=False)
    

def handDown():
    print("hand down")
    motor.on(speed=-10)
    sleep(0.5)
    motor.off(brake=False)
    

def turn_degree(angle):
    past_gyro = gyro.angle
    ki = 0.5
    max_speed=30

    while True:
        current_gyro = gyro.angle
        changed_angle = current_gyro - past_gyro

        error = angle - changed_angle
        if error == 0:
            tank_pair.off(brake=True)
            break

        pid = ki * error
        if pid > max_speed:
            speed = max_speed
        elif pid < max_speed*-1:
            speed = max_speed*-1
        else:
            speed = pid

        tank_pair.on(left_speed=speed, right_speed=speed*-1)


def PIDControl():
    expectation_red = 130
    last_error = 0
    kp = 0.1
    ki = 0
    base_speed = 20
    max_speed = 30

    # default = input("use default: ")
    # if default == 'y':
    #     pass
    # else:
    #     kp = float(input("enter p: "))
    #     ki = float(input("enter i: "))
    #     base_speed = int(input("enter base_speed: "))
    #     max_speed = int(input("enter max_speed: "))

    while True:
        red = color.rgb[0]
        green = color.rgb[1]
        blue = color.rgb[2]

        # Stop if color sensor display no color
        if red == 0:
            print('STOP !!!')
            tank_pair.off(brake=False)
            break
        
        # Stop if robot enter green area
        if green in range(200, 256) and red in range(0, 150) and blue in range(0, 150):
            print('STOP !!!')
            tank_pair.off(brake=False)
            break

        # Calculate for error parameters
        error = red - expectation_red
        delta_error = error - last_error

        last_error = error

        if error > 100:
            error = 100
        elif error < -100:
            error = -100

        # Calculate pid
        pid = kp * error + ki * delta_error
        
        # Calculate left speed and right speed of motor based on pid
        left_speed = max(0, min(base_speed + pid, max_speed))
        right_speed = max(0, min(base_speed - pid, max_speed))

        tank_pair.on(left_speed=left_speed, right_speed=right_speed)


def moveOutOfGreen():
    while True:
        red = color.rgb[0]
        green = color.rgb[1]
        blue = color.rgb[2]

        if green in range(200, 256) and red in range(0, 150) and blue in range(0, 150): 
            tank_pair.on(left_speed=20, right_speed=20)
        else:
            print('STOP !!!')
            tank_pair.off(brake=False)
            break


def displayColor():
    red = color.rgb[0]
    green = color.rgb[1]
    blue = color.rgb[2]
    print("Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
    print("Color: " + color.color_name)


def displayAngle():
    print("Angle: " + str(gyro.angle))


def command_robot(command):
    if command == "move_straight":
        moveOutOfGreen()
        PIDControl()
        return 0, 0, 0
    elif command == "move_left":
        moveOutOfGreen()
        moveBackward()
        turn_degree(-92)
        return 0, 0, 0
    elif command == "move_right":
        moveOutOfGreen()
        moveForward()
        turn_degree(87)
        return 0, 0, 0
    elif command == "turn_left":
        
    elif command == "beep":
        sound.beep()
        return 0, 0, 0
    return False


sound.beep()
print("ROBOT READYYYYYY !!!!")
print('version 3.0')
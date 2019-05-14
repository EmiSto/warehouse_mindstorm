class Robot(object):

    def __init__(self, id, x, y):
        self.id = id
        self.holdingItem = False
        #x,y, direction: 0=up, 1=right, 2=down, 3=left
        self.position = [x,y,0]
    
    def pickup(self):
        if(self.holdingItem):
            print("Already holding item")
            return False
        print("Picking up item")
        self.holdingItem = True
        return True

    def drop(self):
        if(not(self.holdingItem)):
            print("Not holding any item")
            return False
        print("Droping item")
        self.holdingItem = False
        return True
    
    def turn(self, direction):
        if(direction == 'move-right'):
            self.position[2] += 1
            print("Turning right")
        elif(direction == 'move-left'):
            print("Turning left")
            self.position[2] -= 1
        if(self.position[2] < 0 or self.position[2] > 3):
            self.position[2] = 0

    def move(self):
        direction = self.position[2]
        if(direction == 0):
            self.position[1] += 1
            print("moving up")
        elif(direction == 1):
            self.position[0] += 1
            print("moving right")
        elif(direction == 2):
            self.position[1] -= 1
            print("moving down")
        else:
            self.position[0] -= 1
            print("moving left")

    def nextMove(self):
        direction = self.position[2]
        if(direction == 0):
            return(self.position[0],(self.position[1] + 1))
        elif(direction == 1):
            return((self.position[0] + 1), self.position[1])
        elif(direction == 2):
            return(self.position[0],(self.position[1] - 1))
        else:
            return((self.position[0] - 1), self.position[1])

    def getId(self):
        return self.id
    
    def getPosition(self):
        return (self.position[0], self.position[1])
'''
r = Robot('4')
r.pickup()
r.pickup()
for i in range(4):
    r.move()
    r.turn('right')
r.drop()
r.drop()

robotArray = []
r = Robot('4')
robotArray.append(r)
r = Robot('3')
robotArray.append(r)
r = Robot('2')
robotArray.append(r)
r = Robot('1')
robotArray.append(r)

print(robotArray[2].id)
for i,r in enumerate(robotArray):
    print(i)
    if(robotArray[i].getId() == '2'):
        robotArray.pop(i)
print(robotArray[2].id)

for r in robotArray:
    print("robot id: " + r.getId())
'''


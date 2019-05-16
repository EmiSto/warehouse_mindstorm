class Warehouse(object):

    def __init__(self, x, y):

        #format (x,y) where y increases upwards 
        # and x increases to the right
        self.grid = [0] * y
        for i in range(y):
            self.grid[i] = [0]*x
        self.x = x
        self.y = y
    
    def _boundary(self, x, y):
        if(y >= self.y or y < 0 or x >= self.x or x < 0):
            print("Out of bounds!")
            return False
        return True

    def addRobot(self, x, y):
        if(self._boundary(x,y)):
            self.grid[-(y+1)][x] = 1
            print("Robot added")
            return True
        print("Robot not added")
        return False

    def removeRobot(self, x, y):
        if(self.grid[-(y+1)][x] == 0 or not(self._boundary(x,y))):
            print("No robot to remove!")
            return False
        self.grid[-(y+1)][x] = 0
        print("Robot removed")
        return True

    def moveRobot(self, pos1, pos2):
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        if(self.grid[-(y1+1)][x1] == 0 or not(self._boundary(x1,y1))):
            print("No robot to move!")
            return False
        elif(not(self._boundary(x2,y2))):
            print("Robot will hit the wall, it did not move")
            return False
        elif(self.grid[-(y2+1)][x2] == 1):
            print("Robbot already there!")
            return False

        self.grid[-(y1+1)][x1] = 0
        self.grid[-(y2+1)][x2] = 1
        print("Robot moved")
        return True

    def showWarehouse(self):
        for i in range(self.y):
            print(self.grid[i])
        
'''
wh = Warehouse(5,5)
wh.showWarehouse()
wh.addRobot(0,0)
wh.addRobot(2,2)
wh.showWarehouse()

wh.moveRobot((2,2), (2,3))
wh.showWarehouse()
'''
'''
Wharehouse(3,3):

y2  [0][0]  [0][1] [0][2]
y1  [1][0]  [1][1] [1][2] 
y0  [2][0]  [2][1] [2][2]
    x0      x1     x2
'''
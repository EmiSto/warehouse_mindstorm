### Requirement

* python3
* pip3

### Design Document
[link here](https://drive.google.com/drive/folders/1wc1ggQuIj61BuqFYHF8bx3vWkFf4LDhJ)

### Server - Client

You can run server - client in ```server``` folder:

* Install packages:

```
$ pip3 install -r requirements
```

* Modify the ```host``` variable in ```server.py``` and ```templates/index.html``` based on server's network ip address (use ```ifconfig``` to determine)

* Run server-client:

```
$ python server.py
```


### Robot

You can run robot in ```robot``` folder:

* Install packages:

```
$ pip3 install -r requirements
```

* Modify the ```host``` variable in ```robot.py```  based on server's network ip address (use ```ifconfig``` to determine)

* Run robot: There are two option to run robot, fake robot (use for your computer) or real robot (use for lego ev3). By this way, we can create many virtual robots as we want:
```
// Run fake robot, please change the robot_id (for example: robot01)
$ python robot.py robot_id fake

// Run real robot, please change the robot_id (for example: robot02)
$ python robot.py robot_id real
```

*Notify*: The robot_id is unique

### Todo

* Make sure robot can't move outside grid or into another robot
* Represent the grid on the browser
* Arduino - Server - Client
* Auto controlling robot
* Camera - Server - Client
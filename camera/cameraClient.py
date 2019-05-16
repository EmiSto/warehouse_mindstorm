import numpy as np
import cv2
import socketio
import time

sio = socketio.Client()

#Change this base on host ip network address
host = '130.243.223.214'

cap = cv2.VideoCapture(0)

@sio.on('connect', namespace = '/camera')
def handleConnect():
    print('Camera connection established')

@sio.on('send frame', namespace = '/camera')
def handleSend(tmp):
    while(True):
        # Capture frame-by-frame
        _, frame = cap.read()

        #send frame to server. First converts it into jpg then to string.
        #sleeping to lessen the latency problem
        frame = cv2.imencode('.jpg', frame)[1].tostring()
        time.sleep(0.5)
        sio.emit('return frame', {'data': frame})


sio.connect('http://'+host+':5000/camera')
sio.wait()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
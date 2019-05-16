import numpy as np
import cv2
import socketio

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

        #send frame to server
        frame = cv2.imencode('.jpg', frame)[1].tostring()
        sio.emit('return frame', {'data': frame})

        # Display the resulting frame
        #cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break


sio.connect('http://'+host+':5000/camera')
sio.wait()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# sklearn.cluster import KMeans         #libreria de mach
import os
import sys
import cv2
import numpy as np
import time
import keyboard
from multiprocessing import Process

cap = cv2.VideoCapture(0)

whT = 320
confThreshold = 0.5
nmsThreshold = 0.3              #detetes the amonnt of boxes the smaller # the lesser boxes

classesFile = 'coco.names'
classNames = []

presence_counter = 0
absence_counter = 0

key_a = ""
key_w = ""

start_1 = 0
stop_1 = 0
final_1 = 0

start_2 = 0
stop_2 = 0
final_2 = 0

counter_start = 0
counter_stop = 0
counter_final = 0
key_counter = ""

with open(classesFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')


modelConfiguration = 'yolov3.cfg'
modelWeigths = 'yolov3.weights'


#modelConfiguration = 'yolov3-tiny.cfg'
#modelWeigths = 'yolov3-tiny.weights'


net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeigths)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def emergencyFunction():
    global presence_counter
    global absence_counter
    
    if keyboard.is_pressed('r'):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        
    if keyboard.is_pressed('a'):
        presence_counter = 8 
        absence_counter = 0
        
##        while True:
##            counter_start = counter_start + 1
##            if keyboard.is_pressed('s') or counter_start > 50:
##                counter_start = 0
##                break
##            time.sleep(1)
                
    elif keyboard.is_pressed('w'):
        presence_counter = 0 
        absence_counter = 10

def findObjects(outputs,img):
    global presence_counter
    global absence_counter

    hT,wT,cT = img.shape
    bbox = []
    classIds = []
    confs = []
    
    emergencyFunction()
    
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            
            if confidence > confThreshold:
                w,h = int(det[2]*wT) , int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
                
    #print(len(bbox))
    indeces = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)
    indeces = tuple(indeces)
    

# ( %%%%%%%%%%%%%%%%%%%%%%%%%%%    ABSENCE CONDITIONS    %%%%%%%%%%%%%%%%%%%%%%%%%%%
    
        
    if  (not indeces) == True:
        if absence_counter > 4 and absence_counter < 9:
            presence_counter = 0
            absence_counter = absence_counter + 1
            
        elif absence_counter >= 9:
            print("w")
            keyboard.press('w')
            presence_counter = 0
            
            
        elif absence_counter < 9:
            absence_counter = absence_counter + 1

            
    elif (0 in classIds) == False:
        if absence_counter > 4 and absence_counter < 9:
            presence_counter = 0
            absence_counter = absence_counter + 1
            
        elif absence_counter >= 9:
            print("w")
            keyboard.press('w')
            presence_counter = 0
            
            
        elif absence_counter < 9:
            absence_counter = absence_counter + 1
            
#%%%%%%%%%%%%%%%%%%%%%%%%%%%    ABSENCE CONDITIONS    %%%%%%%%%%%%%%%%%%%%%%%%%%%  )
            
            
    emergencyFunction()
    print("\npresence_check_point: ", presence_counter)
    print("absence_check_point: ", absence_counter,"\n")
    
    for i in indeces:
        i = i[0]
        box = bbox[i]
        print("classIds[i]: ", classIds[i])

        if classNames[classIds[i]] == "persona":
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)                        # color, thickness
            cv2.putText(img,f'{classNames[classIds[i]].upper()}', 
                        (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

            
# ( $$$$$$$$$$$$$$$$$$$$$        Presence conditions        $$$$$$$$$$$$$$$$$$
            
    if (0 in classIds) == True:
        if presence_counter > 3 and presence_counter < 6:
            presence_counter = presence_counter + 1
            absence_counter = 0

        
        elif presence_counter >= 6:
            print("a")
            keyboard.press('a')
            absence_counter = 0


            #timeout = time.time() + 55
##            while True:
##                counter_start = counter_start + 1
##                keyboard.press('a')
##                
##                if keyboard.is_pressed('s') or counter_start > 55:
##                    counter_start = 0
##                    break
##                time.sleep(1)
            
        elif presence_counter < 6:
            presence_counter = presence_counter + 1

#$$$$$$$$$$$$$$$$$$$$$        Presence conditions        $$$$$$$$$$$$$$$$$$ )

    emergencyFunction()


def videoFunction():            
    while True:
       
        success, img = cap.read()

        emergencyFunction()
        
        blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob)
        
        layerNames = net.getLayerNames()

        outputNames =  [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

            
        outputs = net.forward(outputNames)

        emergencyFunction()
        
        findObjects(outputs, img)
        
        cv2.imshow('Image',img)
        
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

        cv2.waitKey(1)
            
    
    
if __name__ == '__main__':
    videoFunction()


    

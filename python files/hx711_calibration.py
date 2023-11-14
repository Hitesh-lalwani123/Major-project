import serial.tools.list_ports
import cv2


def myfunc(): 
    
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial(timeout=1)

    portsList = []

    for onePort in ports:
        portsList.append(str(onePort))
        print(str(onePort))

    val = input("Select Port: COM")

    for x in range(0, len(portsList)):
        if portsList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(portVar)

    serialInst.baudrate = 9600
    serialInst.port = portVar
    serialInst.open()
    while True:
        
        if serialInst.in_waiting:
            packet = serialInst.readline()
            curr = packet.decode('utf')
            # myval = int(curr)
            # num = 0
            # for val in curr: 
            #     if(val.isnumeric()):
            #         num = num + int(val)
            # print(num) 
                
            # print('this is curr'+ curr)
            

            curr=float(curr)
            if(curr> 10.0):
                print(curr)
        


myfunc()
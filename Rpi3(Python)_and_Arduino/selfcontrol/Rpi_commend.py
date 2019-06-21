import serial
import time
import pygame
import sys

pygame.init()
pygame.display.set_mode((600,400))
try:
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.1)
except:
    port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=0.1)
print(port)

def readVal(port):
    
    check = 0
    leftF = 0
    rightF = 0
    upF = 0
    downF = 0
    scratch_close=0
    scratch_open=0
    bacleft = 0
    bacright = 0
    forleft = 0
    forright = 0
    scratch_time=0
    while True:
        #st=time.monotonic() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 2second
                
                if event.key == pygame.K_a:
                    #print("left1")
                    leftF = 1
                if event.key == pygame.K_d:
                    #print("right1")
                    rightF = 1
                if event.key == pygame.K_w:
                    #print("up1")
                    upF = 1
                if event.key == pygame.K_s:
                    #print("down1")
                    downF = 1
                if event.key == pygame.K_r:
                 #   scratch_time=time.time()
                    scratch_open=1
                if event.key == pygame.K_f:
                    scratch_close=1
                if event.key == pygame.K_z:
                    bacleft=1
                if event.key == pygame.K_c:
                    bacright=1
                if event.key == pygame.K_q:
                    forleft=1
                if event.key == pygame.K_e:
                    forright=1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    #print("left0")
                    leftF = 0
                if event.key == pygame.K_d:
                    #print("right0")
                    rightF = 0
                if event.key == pygame.K_w:
                    #print("up0")
                    upF = 0
                if event.key == pygame.K_s:
                    #print("down0")
                    downF = 0   
                if event.key == pygame.K_r:
                    #print("down0")
                    scratch_open = 0
                if event.key == pygame.K_f:
                    #print("down0")
                    scratch_close = 0
                if event.key == pygame.K_z:
                    bacleft = 0
                if event.key == pygame.K_c:
                    bacright = 0
                if event.key == pygame.K_q:
                    forleft=0
                if event.key == pygame.K_e:
                    forright=0
                
        check = leftF + rightF + upF + downF + scratch_close + scratch_open + bacleft + bacright + forleft + forright
        
            
        if check == 0 or check >1:
            #print("STOP")
            port.write(b'')
        if check == 1:
            if leftF == 1:
                #print("python_LEFT")
                port.write(b'a')
            if rightF ==1:
                #print("TURN_RIGHT")
                port.write(b'd')
            if upF ==1:
                #print("FOWARD")
                port.write(b'w')
            if downF ==1:
                #print("BACKWARD")
                port.write(b's')
            if scratch_open ==1:
                #print("SCRATCH_OPEN")
                port.write(b'r')
            if scratch_close==1:
                #print("SCRATCH_CLOSE")
                port.write(b'f')
            if bacleft==1:
                #print("BACLEFT")
                port.write(b'z')
            if bacright==1:
                #print("BACRIGHT")
                port.write(b'c')
            if forleft == 1:
                #print("FORLEFT")
                port.write(b'q')
            if forright==1:
                #print("FORRIGHT")
                port.write(b'e')
        print(port.readall())
        #end = time.monotonic()
        #try:
            #print(end-st)
            #time.sleep(1-(end-st))
        #except:
            #continue
        



while True:
    
    readVal(port)
    

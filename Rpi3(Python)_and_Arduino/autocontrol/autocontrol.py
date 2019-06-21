#!/usr/bin/env python
# coding: utf-8
import numpy as np
import cv2
import serial
import time
import sys , getopt
import pymongo
from bson.objectid import ObjectId
import smtplib
from email.mime.text import MIMEText

# 圖像 640 * 480
xCenter=320
xThreshold=30
showImg=1

# house color 
color_house = ""
# object color 
color_object = ""
# house HSV threshold
color_house_lower = {
    "blue":[95,100,40],
    "red":[0,100,0],
    "yellow":[20,50,0],
    "green":[60,45,40],
    "purple":[150,50,0]
}
color_house_upper = {
    "blue":[120,255,255],
    "red":[10,255,255],
    "yellow":[40,255,255],
    "green":[85,225,200],
    "purple":[180,180,100]
}
# object HSV threshold
color_object_lower = {
    "Blue_Ball":[95,100,40],
    "Red_Ball":[0,134,0],
    "Yellow_Ball":[20,200,147],
    "Green_Ball":[59,165,89],
    "Purple_Ball":[150,50,0]
}
color_object_upper = {
    "Blue_Ball":[110,255,255],
    "Red_Ball":[10,255,255],
    "Yellow_Ball":[40,255,220],
    "Green_Ball":[68,225,190],
    "Purple_Ball":[180,150,100]
}

# email
user_email = ""
# mongodb 
Collection_orders = ""
orders_date = ""
db_state_2 = ["Ready to ship","Go to house"]
nowstate = ""

def mongodb_query():
    global user_email
    global color_house
    global color_object
    global Collection_orders
    global db_state_2
    global orders_date
    # MongoDB登入
    # ShoppingCart Cluster
    client = pymongo.MongoClient("mongodb+srv://test190520:test190520@cluster0-gzdzv.azure.mongodb.net/test?retryWrites=true")
    # DataBase "test"
    db = client.test
    # 表單 orders、users
    Collection_orders = db.orders
    Collection_users = db.users

    ordercount = len(list(Collection_orders.find({'state':db_state_2[1]})))
    if ordercount <= 0:
        print(db_state_2[1]," None!!!")
    else:
        # 查詢是否正在運送，若大於一筆訂單，則以時間最早優先送貨
        for itm in list(Collection_orders.find({'state':db_state_2[1]})):
            if orders_date == "":
                orders_date = itm.get('orderdate')
            else :
                if orders_date > itm.get('orderdate'):
                    orders_date = itm.get('orderdate')
        print(orders_date)
        order = list(Collection_orders.find({'orderdate': orders_date}))[0]
        # print(order)
        # 送達地
        color_house = order["address"]
        items = order["cart"]["items"]
        items_key = list(items.keys())
        # 夾取物
        color_object = items[items_key[0]]["item"]["title"]
        # print(color_object)
        user = order["user"]
        # print(type(user_email)) <class 'bson.objectid.ObjectId'>
        
        # User email
        user_email = list(Collection_users.find({"_id": ObjectId(user)}))[0]["email"]
        # print(type(user_email))
        # auroral.13king518@gmail.com
        return db_state_2[1]

    ordercount = len(list(Collection_orders.find({'state':db_state_2[0]})))
    if ordercount <= 0:
        print(db_state_2[0]," None!!!")
        return "No waiting orders"
    else:
        # 查詢是否正在出貨，若大於一筆訂單，則以時間最早優先出貨
        for itm in list(Collection_orders.find({'state':db_state_2[0]})):
            if orders_date == "":
                orders_date = itm.get('orderdate')
            else :
                if orders_date > itm.get('orderdate'):
                    orders_date = itm.get('orderdate')
        print(orders_date)
        order = list(Collection_orders.find({'orderdate': orders_date}))[0]
        # print(order)
        # 送達地
        color_house = order["address"]
        items = order["cart"]["items"]
        items_key = list(items.keys())
        # 夾取物
        color_object = items[items_key[0]]["item"]["title"]
        # print(color_object)
        user = order["user"]
        # print(type(user_email)) <class 'bson.objectid.ObjectId'>
        
        # User email
        user_email = list(Collection_users.find({"_id": ObjectId(user)}))[0]["email"]
        # print(type(user_email))
        # auroral.13king518@gmail.com
        return db_state_2[0]

def Go_to_house():
    global Collection_orders
    global color_object
    global nowstate
    global orders_date
    global db_state_2

    #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
    order_state_update = {
        'state':'Go to house'
    }
    Collection_orders.update_one({'orderdate': orders_date},{'$set':order_state_update})
    nowstate=db_state_2[1]

def Ready_notice_email(gmail_user = 'ji3941u4ul6@gmail.com',gmail_password = 'xj4vm,3fu6'):
    global color_object
    global orders_date
    # your gmail password
    content = color_object + " is ready to ship("+orders_date+"). You can see the order in your Shopping Cart User Account. Thank for your choice. Have a nice day!" 
    msg = MIMEText(content)
    msg['Subject'] = 'Shopping Cart_Item Order State'
    msg['From'] = "Shopping Cart_Administrator"
    msg['To'] = user_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()   
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print('Ready to ship Email sent!')
    
    

def Arrived_notice_email(gmail_user = 'ji3941u4ul6@gmail.com',gmail_password = 'xj4vm,3fu6'):
    global Collection_orders
    global color_object
    global nowstate
    global orders_date
    #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    order_state_update = {
        'state':'arrived 【'+time_string+"】"
    }
    Collection_orders.update_one({'orderdate': orders_date},{'$set':order_state_update})
    content = color_object + " is arrived("+time_string+"). You can see the order in your Shopping Cart User Account. Thank for your choice. Have a nice day!" 
    msg = MIMEText(content)
    msg['Subject'] = 'Shopping Cart_Item Order State'
    msg['From'] = "Shopping Cart_Administrator"
    msg['To'] = user_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print("Arrived Email sent!")
    nowstate = 'arrived 【'+time_string+"】"


def readIndex(argv): 
    global color_house
    global color_object
    global nowstate
    try:
        opts, args = getopt.getopt(argv,"h:o:s:",["house=","object=","state="])
    except getopt.GetoptError:
        print('test190602.py -h <house> -o <object> -s <state>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-m':
            print('test190601.py -h <house> -o <object> -s <state>')
            sys.exit()
        if opt in ("-h", "--house"):
            color_house = arg
            #print(color_house)
        if opt in ("-o", "--object"):
            color_object = arg
            #print(color_object)
        if opt in ("-s", "--state"):
            nowstate = arg



def detectCircle(color,switch):
    global color_house_lower
    global color_house_upper
    # 開始計時
    st=time.monotonic()

    
    #讀取照片一帧畫面
    try: 
        ret, frame = cap.read()
    except:
    #判断是否成功打开摄像头
        print ('No Camera Connect!!!')
    
    #調整畫面大小
    frame=cv2.resize(frame,(320,240))
    
    
    


    if switch=="house":
        #根据阈值构建掩膜
        
        frame=frame[10:70,:]
        lower=np.array(color_house_lower[color])
        upper=np.array(color_house_upper[color]) 
    elif switch=="object":
        #根据阈值构建掩膜
        lower=np.array(color_object_lower[color])
        upper=np.array(color_object_upper[color]) 
    else:
        print("No swith house or object!!!")
    cv2.imshow("frame",frame)

    #转到HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #根据阈值构建掩膜
    mask = cv2.inRange(hsv, lower, upper)
    #腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    mask[:,0:1]=0
    mask[:,-1]=0
    mask[0:1,:]=0
    mask[-1,:]=0
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #初始化圆形轮廓质心
    center = None
    #如果存在轮廓
    if len(cnts) > 0:
        #找到面积最大的轮廓
        c = max(cnts, key = cv2.contourArea)
        #确定面积最大的轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #计算轮廓的矩
        M = cv2.moments(c)
        #计算质心
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        #只有当半径大于10时，才执行画图
        if True:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    else:
        #如果图像中没有检测到東西
        print("No detecting!!!")
        x=-1
        y=-1
        radius=-1
        return x,y,radius
            
    cv2.imshow('Frame', frame)
    k = cv2.waitKey(1)&0xFF
    # 結束計時
    end=time.monotonic()
    #print(end-st)
    try:
        return x,y,radius
    except:
        print("Detecting Error!!!")
        x=-1
        y=-1
        radius=-1
        return x,y,radius

    
def searchBall(color,switch):
    # 空陣列存偵測數值
    circles1=np.zeros(0)
    notfind=True
    
    findConfirmTimes=5
    frontDuration=2    
    
    findTimes=0
    index_search = [b'a',b'a',b'a',b'a',b'a',b'd',b'd',b'd',b'd',b'd'] # only a
    i_search = 0
    t1=time.monotonic()
    
    while notfind :
        st=time.monotonic() 
        x, y, radius=detectCircle(color,switch)
        if x==-1 and y==-1 and radius==-1:
            findTimes=0
            print(index_search[i_search])
            port.write(index_search[i_search])
            if i_search == 9:
                i_search = 0
                print(time.monotonic()-t1)
                t1=time.monotonic()
            else:
                i_search +=1
        else:
            findTimes += 1
            print((x,y))
            if findTimes == findConfirmTimes:
                notfind = False
                print("Leave Search Mode !!!")
                return None
        end = time.monotonic()
        try:
            #print(end-st)
            time.sleep(0.13-(end-st))
        except:
            continue
    
def catchBall(color,switch):
    print("Go to catching model!!!")
    circles1=np.zeros(0)
    finalSize=175
    finalApproach=2
    sizeConfirmTimes=1

    index_before_move = []
    index_search = [b'z',b'z',b'z',b'c',b'c',b'c',b'c',b'c',b'c',b'z',b'z',b'z'] # only d
    lostTimes=0
    lostTimes_index=0
    sizeConfirm=0

    while True:
        print(index_before_move)
        st=time.monotonic()
        x, y, radius = detectCircle(color,switch)
        if x==-1 and y==-1 and radius==-1:       
            lostTimes +=1
        else:            
            if radius*2 >= finalSize:
                sizeConfirm += 1
                if sizeConfirm == sizeConfirmTimes:
                    break
                continue                    
            
            if (x*2)>(xCenter+xThreshold):
                print(b'e')
                port.write(b'e')
                index_before_move=[b'e']+index_before_move
            elif (x*2)<(xCenter-xThreshold):
                print(b'q')
                port.write(b'q')
                index_before_move=[b'q']+index_before_move
            else: 
                print(b'w')
                port.write(b'w')
                index_before_move=[b'w']+index_before_move
            lostTimes =0
            lostTimes_index = 0

        # 之前動作最多存8個    
        
        if len(index_before_move)>=8:
            print("YES")
            del(index_before_move[-1])
        
        if lostTimes>5:
            if len(index_before_move)>0:
                #print("index_before_move: ",index_before_move[0])
                if index_before_move[0]==b'e':
                    print(b'c')
                    port.write(b'c')
                if index_before_move[0]==b'q':
                    print(b'z')
                    port.write(b'z')
                if index_before_move[0]==b'w':
                    print(b's')
                    port.write(b's')
                del(index_before_move[0])
            else:
                print("index_search")
                print(index_search[lostTimes_index%len(index_search)])
                port.write(index_search[lostTimes_index%len(index_search)])
                lostTimes_index += 1
        
        end=time.monotonic()
        try:
            time.sleep(0.1-(end-st))
        except:
            continue
    #final approach
    
    port.write(b'w')
    #print(port.readall())

    #close the claw
    port.write(b'r')
    print("r")
    #if(showImg):
    #    cap.release()
    #    cv2.destroyAllWindows()


def searchDest(color,switch):
    port.readall()
    dest=np.zeros(0)
    notfind=True
    findConfirmTimes=3
  
    findTimes=0
    index_search = [b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w']
    i_search = 0

    while notfind :
        st=time.monotonic() 
            
        x, y, radius=detectCircle(color,switch)
        if x==-1 or ( radius<8):
            findTimes=0
            print(index_search[i_search])
            port.write(index_search[i_search])
            if i_search == 9:
                i_search = 0
            else:
                i_search +=1
        else:
            findTimes += 1
            print((x,y))
            if findTimes == findConfirmTimes:
                notfind = False
                print("Leave Search Mode !!!")
                return None
        end = time.monotonic()
        try:
            #print(end-st)
            time.sleep(0.13-(end-st))
        except:
            continue
            

    
def goDest(color,switch):
    port.readall()
    print("Go to catching model!!!")
    circles1=np.zeros(0)
    finalSize=200
    finalApproach=2
    sizeConfirmTimes=1

    index_before_move = []
    index_search = [b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w',b'w'] # only d
    lostTimes=0
    lostTimes_index=0
    sizeConfirm=0

    while True:
        print(index_before_move)
        st=time.monotonic()
        x, y, radius = detectCircle(color,switch)
        if x==-1 and y==-1 and radius==-1:       
            lostTimes +=1
        else:            
            if radius*2 >= finalSize:
                sizeConfirm += 1
                if sizeConfirm >= sizeConfirmTimes:
                    if(color_percent(color,70,320,switch)>0.75):
                        break
                # continue                    
            
            if (x*2)>(xCenter+xThreshold):
                print(b'e')
                port.write(b'e')
                index_before_move=[b'e']+index_before_move
            elif (x*2)<(xCenter-xThreshold):
                print(b'q')
                port.write(b'q')
                index_before_move=[b'q']+index_before_move
            else: 
                print(b'w')
                port.write(b'w')
                index_before_move=[b'w']+index_before_move
            lostTimes =0
            lostTimes_index = 0

        # 之前動作最多存8個    
        
        if len(index_before_move)>=8:
            print("YES")
            del(index_before_move[-1])
        
        if lostTimes>5:
            if len(index_before_move)>0:
                #print("index_before_move: ",index_before_move[0])
                if index_before_move[0]==b'e':
                    print(b'c')
                    port.write(b'c')
                if index_before_move[0]==b'q':
                    print(b'z')
                    port.write(b'z')
                if index_before_move[0]==b'w':
                    print(b's')
                    port.write(b's')
                del(index_before_move[0])
            else:
                print("index_search")
                print(index_search[lostTimes_index%10])
                port.write(index_search[lostTimes_index%10])
                lostTimes_index += 1
        
        end=time.monotonic()
        try:
            time.sleep(0.12-(end-st))
        except:
            continue
    #final approach
    
        
        
    #print(port.readall())

    #close the claw
    port.write(b'f')
    print("f")
    #if(showImg):
    #    cap.release()
    #    cv2.destroyAllWindows()

#x height y width
def color_percent(color,x,y,switch):
    

    
    #讀取照片一帧畫面
    try: 
        ret, frame = cap.read()
    except:
    #判断是否成功打开摄像头
        print ('No Camera Connect!!!')
    
    #調整畫面大小
    frame=cv2.resize(frame,(320,240))
    
    frame=frame[:x,:y]

    if switch=="house":
        #根据阈值构建掩膜
        
        lower=np.array(color_house_lower[color])
        upper=np.array(color_house_upper[color]) 
    elif switch=="object":
        #根据阈值构建掩膜
        lower=np.array(color_object_lower[color])
        upper=np.array(color_object_upper[color]) 
    else:
        print("No swith house or object!!!")
        
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    total=x*y*255
    count=np.sum(mask)
    
    cv2.imshow('Frame', frame)
    k = cv2.waitKey(1)&0xFF
    print(count/total)
    return count/total
        

if __name__=="__main__":
    try:
        port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=0.3)
    except:
        port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.3)
    print(port)
    
    cap = cv2.VideoCapture(0)
    time.sleep(0.2)
    for i in range(10): # close夾爪
        port.write(b'r')
        time.sleep(0.1)
        print("j")
    time.sleep(0.1)
    nowstate = mongodb_query()
    # print(sys.argv[1:])
    if len(sys.argv) >=4 :
        readIndex(sys.argv[1:])



    while nowstate == "No waiting orders" or nowstate == db_state_2[0] or nowstate == db_state_2[1]:
        try:
            print(nowstate)
            print("orders_date: ",orders_date)
    
            if nowstate == db_state_2[0]:
                Ready_notice_email()
                print("house: ",color_house)
                print("object: ",color_object)
                print("nowstate: ",nowstate)

                for i in range(10): # 關閉障
                    port.write(b'j')
                    time.sleep(0.1)
                    print("j")
                time.sleep(0.1)
                
                port.write(b'f') # 開夾爪
                time.sleep(1)
                searchBall(color_object,"object")
                catchBall(color_object,"object")
                Go_to_house()
                time.sleep(3)

                               

            if nowstate == db_state_2[1]:
                # for i in range(300):
                #     if(i==30):
                #         port.write(b'e')
                #     else:
                #         port.write(b'w')
                #     time.sleep(0.12)
                searchDest(color_house,"house")
                time.sleep(1)

                goDest(color_house,"house")
                cap.release()
                cv2.destroyAllWindows()
                Arrived_notice_email()
                orders_date=""
                nowstate = ""
                port.write(b'l')
                time.sleep(3)
                
        except KeyboardInterrupt:
            cap.release()
            cv2.destroyAllWindows()
            pass

        nowstate = mongodb_query()

    

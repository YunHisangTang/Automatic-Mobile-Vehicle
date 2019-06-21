import cv2
import numpy as np
import time

camera = cv2.VideoCapture(0)
(ret, image) = camera.read()
HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
def getpos(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(HSV[y,x])
#th2=cv2.adaptiveThreshold(imagegray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)



# def detectCircle(color,switch):
#     global color_house_lower
#     global color_house_upper
#     # 開始計時
#     st=time.monotonic()

    
#     #讀取照片一帧畫面
#     try: 
#         ret, frame = cap.read()
#     except:
#     #判断是否成功打开摄像头
#         print ('No Camera Connect!!!')
    
#     #調整畫面大小
#     frame=cv2.resize(frame,(320,240))
    
    
    


#     if switch=="house":
#         #根据阈值构建掩膜
        
#         frame=frame[:70,:]
#         lower=np.array(color_house_lower[color])
#         upper=np.array(color_house_upper[color]) 
#     elif switch=="object":
#         #根据阈值构建掩膜
#         lower=np.array(color_object_lower[color])
#         upper=np.array(color_object_upper[color]) 
#     else:
#         print("No swith house or object!!!")
#     cv2.imshow("frame",frame)

#     #转到HSV空间
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     #根据阈值构建掩膜
#     mask = cv2.inRange(hsv, lower, upper)
#     #腐蚀操作
#     mask = cv2.erode(mask, None, iterations=2)
#     #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
#     mask = cv2.dilate(mask, None, iterations=2)
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#     #初始化圆形轮廓质心
#     center = None
#     #如果存在轮廓
#     if len(cnts) > 0:
#         #找到面积最大的轮廓
#         c = max(cnts, key = cv2.contourArea)
#         #确定面积最大的轮廓的外接圆
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         #计算轮廓的矩
#         M = cv2.moments(c)
#         #计算质心
#         center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
#         #只有当半径大于10时，才执行画图
#         if True:
#             cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#             cv2.circle(frame, center, 5, (0, 0, 255), -1)
#     else:
#         #如果图像中没有检测到東西
#         print("No detecting!!!")
#         x=-1
#         y=-1
#         radius=-1
#         return x,y,radius
            
#     cv2.imshow('Frame', frame)
#     k = cv2.waitKey(1)&0xFF
#     # 結束計時
#     end=time.monotonic()
#     #print(end-st)
#     try:
#         return x,y,radius
#     except:
#         print("Detecting Error!!!")
#         x=-1
#         y=-1
#         radius=-1
#         return x,y,radius




# while True:
#     st=time.monotonic()
#     detectCircle("yellow","house")
#     end=time.monotonic()
#     time.sleep(0.1-(end-st))
    











#摄像头释放
camera.release()
HSV=cv2.resize(HSV,(320,240))
cv2.imshow("imageHSV",HSV[:70,:])
cv2.imshow('image',HSV)
cv2.setMouseCallback("imageHSV",getpos)
cv2.waitKey(0)
#print (image(10,10,10))

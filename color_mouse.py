import cv2
import numpy as np
import pyautogui
import sys

cap = cv2.VideoCapture(0)

#bimg = np.zeros((640, 480, 3), np.uint8)
m=0
n=0
a=0
k=0

fgbg = cv2.createBackgroundSubtractorMOG2()

cir1=0
cir2=0
r1=0

while(True):

    cir=0

    bimg = np.zeros((640, 480, 3), np.uint8)
    ret, frame = cap.read()
    #height, width, channels = frame.shape
    #print(height, width, channels)
    #boundaries = [([110,100,50], [130,255,255])] #blue
    boundaries = [([94,80,2], [126,255,255])] #blue1
    boundaries1 = [([25, 52, 72], [102, 255, 255])] #green1
    #boundaries1 = [([81, 100, 50], [140, 255, 255])]  # green
    #boundaries1 = [([150, 100, 50], [180, 255, 255])]
    #boundaries1 = [([40, 40, 40], [60, 255, 255])] #violet
    boundaries2 = [([161,155,84], [179,255,255])] #red1

    # create NumPy arrays from the boundaries
    lower = np.array(boundaries[0][0], dtype="uint8")
    upper = np.array(boundaries[0][1], dtype="uint8")

    lower1 = np.array(boundaries1[0][0], dtype="uint8")
    upper1 = np.array(boundaries1[0][1], dtype="uint8")

    lower2 = np.array(boundaries2[0][0], dtype="uint8")
    upper2 = np.array(boundaries2[0][1], dtype="uint8")

    fgmask = fgbg.apply(frame)
    cv2.imshow('background_subtraction', fgmask)

    gray= frame.copy()
    frame1 =cv2.bitwise_and(frame,frame, mask=fgmask)
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(gray,lower,upper)
    mask1=cv2.inRange(gray,lower1,upper1)
    mask2=cv2.inRange(gray,lower2,upper2)

    res = cv2.bitwise_and(frame, frame, mask=mask)
    res1 = cv2.bitwise_and(frame, frame, mask=mask1)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)

    cv2.imshow('colour_blue', res)
    #cv2.imshow('colour_green', res1)
    cv2.imshow('colour_red', res2)
    output=gray.copy()
    gray = cv2.GaussianBlur(mask,(25,25),cv2.BORDER_DEFAULT)
    gray1 = cv2.GaussianBlur(mask1, (25, 25), cv2.BORDER_DEFAULT)
    gray2 = cv2.GaussianBlur(mask2, (25, 25), cv2.BORDER_DEFAULT)
    cimg = frame.copy()
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.9, 120,
                               param1=50, param2=30, minRadius=10, maxRadius=200)
    circles1 = cv2.HoughCircles(gray1, cv2.HOUGH_GRADIENT, 0.9, 120,
                               param1=50, param2=30, minRadius=10, maxRadius=200)
    circles2 = cv2.HoughCircles(gray2, cv2.HOUGH_GRADIENT, 0.9, 120,
                                param1=50, param2=30, minRadius=10, maxRadius=200)
    cv2.imshow('video', gray)
    #cv2.imshow('video1', gray1)
    cv2.imshow('video2', gray2)

    if circles is not None:
        cir=1
        if k==24:
            k=0

        if k%2==0:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                print(x,y,r)
                print("j")
                if a==0 and x!=0 and y!=0:
                    m=x
                    n=y
                    a=1
                    r1=r
                elif x!=0 and y!=0:
                    cv2.circle(cimg, (x, y), r, (0, 255, 255), 4)
                    cv2.rectangle(cimg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.circle(bimg, (x, y), r, (0, 255, 255), 4)
                    cv2.rectangle(bimg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                    #cv2.line(bimg, (m, n), (x, y), (255, 0, 0), 3)
                    #pyautogui.moveTo(1920-x*3, y*2.25, duration=0)
                    m=x
                    n=y
        k+=1

    if circles1 is not None and cir1==0 and circles2 is None:
        cir1=1
        if k == 24:
            k = 0

        if k % 1 == 0:
            circles1 = np.round(circles1[0, :]).astype("int")
            for (x, y, r) in circles1:
                print(x,y,r)
                print("k")
                if a == 0 and x != 0 and y != 0:
                    m = x
                    n = y
                    a = 1
                elif x != 0 and y != 0:
                    cv2.circle(cimg, (x, y), r, (255, 0, 0), 4)
                    cv2.rectangle(cimg, (x - 5, y - 5), (x + 5, y + 5), (128, 0, 255), -1)
                    cv2.circle(bimg, (x, y), r, (0, 255, 255), 4)
                    cv2.rectangle(bimg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                    #cv2.line(bimg, (m, n), (x, y), (255, 0, 0), 3)
#                    if cir==0:
#                         pyautogui.click()
#                    elif cir==1:
#                         pyautogui.doubleClick()
                    m = x
                    n = y
        k += 1
    else:
        cir1=0



    if circles2 is not None and cir2==0 and circles1 is None and circles is None:
        cir2=1
        if k==24:
            k=0

        if k%2==0:
            circles2 = np.round(circles2[0, :]).astype("int")
            for (x, y, r) in circles2:
                if a==0 and x!=0 and y!=0:
                    m=x
                    n=y
                    a=1
                elif x!=0 and y!=0:
                    cv2.circle(cimg, (x, y), r, (0, 0, 255), 4)
                    cv2.rectangle(cimg, (x - 5, y - 5), (x + 5, y + 5), (128, 0, 0), -1)
                    cv2.circle(bimg, (x, y), r, (0, 255, 255), 4)
                    cv2.rectangle(bimg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                    #cv2.line(bimg, (m, n), (x, y), (255, 0, 0), 3)
                    # pyautogui.click(button='right')
                    m=x
                    n=y
        k+=1
    else:
        cir2=0


    if circles1 is not None and circles is None and circles2 is not None:
        if k == 24:
            k = 0

#        if k % 1 == 0:
            #pyautogui.scroll(10)  # scroll up 10 "clicks"
        k += 1

    if circles1 is None and circles is not None and circles2 is not None:
        if k == 24:
            k = 0

#        if k % 1 == 0:
            #pyautogui.scroll(-10)  # scroll down 10 "clicks"
        k += 1

    #cv2.line(bimg, (377, 201), (311,264), (238,130,238),3)
    #cv2.line(bimg, (311,264), (196, 329), (238, 130, 238), 3)
    #cv2.line(bimg, (196, 329), (1, 224), (238, 130, 238), 3)
    #cv2.line(bimg, (1, 224), (40,60), (238, 130, 238), 3)


    #cv2.circle(bimg, (314, 128), 20, (0, 255, 255), 4)
    #cv2.rectangle(bimg, (314 - 5, 128 - 5), (314 + 5, 128 + 5), (0, 128, 255), -1)

    #cv2.circle(bimg, (244, 130), 21, (0, 0, 255), 4)
    #cv2.rectangle(bimg, (244 - 5, 130 - 5), (244 + 5, 130 + 5), (0, 128, 255), -1)


    #    cv2.line(bimg, (40,60), (149,0), (238,130,238),3)
 #   cv2.line(bimg, (149,0), (271, 28), (238, 130, 238), 3)
  #  cv2.line(bimg, (271, 28), (375, 28), (238, 130, 238), 3)
   # cv2.line(bimg, (375, 28), (377,201), (238, 130, 238), 3)

    cv2.imshow('l', bimg)
    cv2.imshow('video4', cimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

img = cv2.imread('000127.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite('houghlines1.jpg',gray)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imwrite('houghlines2.jpg',edges)

minLineLength = 1000
maxLineGap = 100
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)
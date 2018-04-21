import cv2
import numpy as np

print (cv2.__version__)

img = cv2.imread('000125.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imwrite('lineas_2_gray.jpg',gray)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
# cv2.imwrite('lineas_2_edges.jpg',edges)

minLineLength = 100
maxLineGap = 10

lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength = 100,maxLineGap = 10)

edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
width, height,channels = img.shape

cv2.line(img,(int(height/2),0),(int(height/2),width),(255,0,0),2)
cv2.line(img,(0,int(width/2)),(height,int(width/2)),(255,0,0),2)
cv2.line(edges,(int(height/2),0),(int(height/2),width),(255,0,0),2)
cv2.line(edges,(0,int(width/2)),(height,int(width/2)),(255,0,0),2)

# print (len(lines))
# print (lines)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(edges,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('lineas_2_edges.jpg',edges)
cv2.imwrite('lineas_2_1.jpg',img)

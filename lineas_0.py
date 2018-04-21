import cv2
import numpy as np

print (cv2.__version__)

img = cv2.imread('000127.png')
img2 = cv2.imread('000127.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite('lineas_0_gray.jpg',gray)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
edges2 = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imwrite('lineas_0_edges.jpg',edges)

lines = cv2.HoughLines(edges,1,np.pi/180,230)
minLineLength = 1000
maxLineGap = 100
linesP = cv2.HoughLinesP(edges,1,np.pi/180,250,
                        minLineLength,maxLineGap)

edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
edges2 = cv2.cvtColor(edges2,cv2.COLOR_GRAY2BGR)

print (len(lines))
for i in range(0,len(lines),1):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(i*20,255,255),2)
        cv2.line(edges,(x1,y1),(x2,y2),(0,255-i*5,i*5),2)

cv2.imwrite('lineas_0_edgesFInal.jpg',edges)
cv2.imwrite('lineas_0_1.jpg',img)

print (len(linesP))
for i in range(0,len(linesP),1):
    for x1,y1,x2,y2 in linesP[i]:
        cv2.line(img2,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.line(edges2,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('lineas_0_edgesFInal_P.jpg',edges2)
cv2.imwrite('lineas_0_1_P.jpg',img2)
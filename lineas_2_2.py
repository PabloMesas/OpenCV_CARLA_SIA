import cv2
import numpy as np

print (cv2.__version__)

img = cv2.imread('000125.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imwrite('lineas_2_gray.jpg',gray)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imwrite('lineas_edges.jpg',edges)

lines = cv2.HoughLines(edges,1,np.pi/180,200)

edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
width, height,channels = img.shape

cv2.line(img,(int(height/2),0),(int(height/2),width),(255,0,0),2)
cv2.line(img,(0,int(width/2)),(height,int(width/2)),(255,0,0),2)
cv2.line(edges,(int(height/2),0),(int(height/2),width),(255,0,0),2)
cv2.line(edges,(0,int(width/2)),(height,int(width/2)),(255,0,0),2)

print (len(lines))
for line in lines:
    for rho,theta in line:
        a = np.cos(theta) #pendiente
        b = np.sin(theta) #pendiente
        x0 = a*rho #desplazamiento en X
        y0 = b*rho #desplazamiento en Y
        if theta*(180/np.pi) < 89 and theta*(180/np.pi) > 1 and y0 > int(width/2) :
            # print ('rho ' + str(rho)+ ' theta (en grados) '+ str(theta*(180/np.pi)))
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            # x2 = int(x0 - int(height/2)*(-b))
            x2 = int(height/2)
            y2 = int((rho - int(height/2)*(a))/b)

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
            
            # print ('X0 ' + str(x0) + ' Y0 '+ str(y0))
            cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.line(edges,(x0,y0),(int(x0+100),int(y0+100)),(0,255,0),2)
            cv2.line(edges,(x2,y2),(x2,y2),(0,255,0),6)
        elif theta*(180/np.pi) >91 and theta*(180/np.pi) < 179:
            # print ('rho ' + str(rho)+ ' theta (en grados) '+ str(theta*(180/np.pi)))
            x1 = int(height/2)
            y1 = int((rho - int(height/2)*(a))/b)

            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
            
            # print ('X0 ' + str(x0) + ' Y0 '+ str(y0))
            cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
            # cv2.line(edges,(x0,y0),(int(x0+100),int(y0+100)),(0,255,0),2)
            cv2.line(edges,(x1,y1),(x1,y1),(255,160,0),6)
            
cv2.line(edges,(int(height/2),int(width/2)),(int(height/2),int(width/2)),(255,100,100),8) # Punto medio

cv2.imwrite('lineas_2_edges.jpg',edges)
cv2.imwrite('lineas_2_1.jpg',img)
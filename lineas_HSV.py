import numpy as np
import cv2
print (cv2.__version__)

cap = cv2.VideoCapture('./Originales/longroad1.gif')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True :
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range Road Line color in HSV
        road_line_color = np.uint8([[[109,196,217 ]]])
        hsv_green = cv2.cvtColor(road_line_color,cv2.COLOR_BGR2HSV)
        lower_road_line_color = np.array([14,100,100])
        upper_road_line_color = np.array([40,255,217])

        mask = cv2.inRange(hsv, lower_road_line_color, upper_road_line_color)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        _, binary = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        cv2.imwrite('./Salida/lineas_edges.jpg',binary)
        lines = cv2.HoughLines(binary,1,np.pi/180,200)
        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        try:
            for line in lines:
                for rho,theta in line:
                    a = np.cos(theta) #pendiente
                    b = np.sin(theta) #pendiente
                    x0 = a*rho #desplazamiento en X
                    y0 = b*rho #desplazamiento en Y
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))

                    cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)                    
                    cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
        except TypeError:
            print('Error Loco')

        cv2.imshow("result", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
import numpy as np
import cv2
print (cv2.__version__)

cap = cv2.VideoCapture('./Originales/longroad1.gif')

while(cap.isOpened()):
    ret, frame = cap.read()
    original_frame = frame.copy()
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
        # cv2.imwrite('./Salida/lineas_edges.jpg',binary)
        kernel = np.ones((12,12),np.uint8)
        closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        erosion = cv2.erode(closing,kernel,iterations = 1)

        lines_p = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength = 80,maxLineGap = 50)
        lines = cv2.HoughLines(erosion,1,np.pi/180,100)
        
        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
        binary = cv2.cvtColor(binary,cv2.COLOR_GRAY2BGR)


        try:
            print (len(lines_p))
            for line in lines_p:
                x1,y1,x2,y2 = line[0]
                cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
                cv2.line(edges,(x1,y1),(x2,y2),(255,0,0),2)
                # cv2.line(binary,(x1,y1),(x2,y2),(255,0,0),2)

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
                    # cv2.line(binary,(x1,y1),(x2,y2),(0,0,255),2)
        except TypeError:
            print('En este frame no hay líneas')

        except ValueError:
            print('En este frame no se detectan líneas por el método probabilístico')

        # Mostrar ventana
        small_original = cv2.resize(original_frame, (0,0), fx=0.5, fy=0.5)
        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        small_edges = cv2.resize(edges, (0,0), fx=0.5, fy=0.5)
        small_binary = cv2.resize(binary, (0,0), fx=0.5, fy=0.5)
        cv2.imshow("result_original", small_original)
        cv2.moveWindow('result_original',0,0)
        cv2.imshow("result_processed", small_frame)
        cv2.moveWindow('result_processed',650,500)
        cv2.imshow("result_edges", small_edges)
        cv2.moveWindow('result_edges',1300,0)
        cv2.imshow("result_binary", small_binary)
        cv2.moveWindow('result_binary',650,0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
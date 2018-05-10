import numpy as np
from cv2 import cv2 

def get_road_line(frame_RGB):
    #frame_RGB = cv2.flip(frame_RGB,1) #Flip verticaly the frame
    frame = frame_RGB.copy()
    part_frame = frame[350:720, 0:1280] #Solo obtenemos la seccion del frame con la carretera
    # Convert BGR to HSV
    frame_hsv = cv2.cvtColor(part_frame, cv2.COLOR_BGR2HSV)

    # define range Road Line color in HSV
    # road_line_color = np.uint8([[[109,196,217 ]]])
    # hsv_color = cv2.cvtColor(road_line_color,cv2.COLOR_BGR2HSV)
    # print (hsv_color) #Handmade way to obtain the HSV Color
    lower_road_line_color = np.array([14,100,100])
    upper_road_line_color = np.array([40,255,217])
    mask = cv2.inRange(frame_hsv, lower_road_line_color, upper_road_line_color)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(part_frame,part_frame, mask= mask)

    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    _, binary = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    lines_p = cv2.HoughLinesP(edges,1,np.pi/180,80,minLineLength = 50,maxLineGap = 150) #Método que detecta las líneas

    edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    binary = cv2.cvtColor(binary,cv2.COLOR_GRAY2BGR)
    lines_angles = []
    angles_degrees = []
    try:
            # print (lines_p)
            for line in lines_p: #Print the lines on the Original Frame
                x1,y1,x2,y2 = line[0] #Points to obtain a line
                y1 = y1 + 350 #Plus 350 to adapt to the full frame after the crop
                y2 = y2 + 350
                angle = get_line_angle(x1,y1,x2,y2)
                angles_degrees.append(angle)
                lines_angles.append([[x1,y1,x2,y2], angle]) #Save the angle
            
                cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
                print_angles_frame(x1, y1, x2, y2, angle, frame) #Print the angles on the frame (for debug)

    except TypeError:
        print('En este frame no hay líneas')

    except ValueError:
        print('En este frame no se detectan líneas por el método probabilístico')

    print(lines_angles)
    return frame, angles_degrees

def get_line_angle (x1,y1,x2,y2): # Obtain the angle of the line between the point x1,y1 & x2,y2
    degrees = ((get_line_slope(x1,y1,x2,y2) * 180)/np.pi) #Transform the radians to degrees with 180/pi
    return degrees

def get_line_slope (x1,y1,x2,y2): #Get the slope (m) of the line with the line formula y=x*m + c
    if x1 != x2:
        slope = (y2-y1)/(x2-x1) #Get the slope of the line with the line formula y=x*m + c
    else:
        slope = np.pi/2
    return slope #In Radians

def get_line_displacement (x1,y1,x2,y2): #Get the displacement (c) of the line with the line formula y=x*m + c
    if x1 != x2:
        c = (y1*x2 - y2*x1)/(x2-x1)
    else:
        c = x1
    return c

def print_angles_frame (x1, y1, x2, y2, angle, frame):
    font = cv2.FONT_HERSHEY_PLAIN
    if y1 < y2:
        rnd_y = np.random.randint(y1, high = y2, size = 1) # y1 sould be lower than y2
    else:
        rnd_y = np.random.randint(y2, high = y1, size = 1)

    new_x = (x2-x1) * ((rnd_y-y1)/(y2-y1)) + x1
    cv2.putText(frame, str(np.round(angle,decimals=2)), (new_x + 10, rnd_y), font, 1.5, (0,0,0), 2, cv2.LINE_AA)

def distance_to_left_margin (line): #To get distance we use the point x=0, y=600
    slope, c = line #Line is a list formed by [slope, displacement] of the line formula y = x*m + c
    x = (600 - c)/slope
    return x
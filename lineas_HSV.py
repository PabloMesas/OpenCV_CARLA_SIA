import cv2
import numpy as np

print (cv2.__version__)

img = cv2.imread('./Originales/000130.png')

# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
green = np.uint8([[[109,196,217 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print (hsv_green)
lower_road_line_color = np.array([14,100,100])
upper_road_line_color = np.array([40,255,217])

mask = cv2.inRange(hsv, lower_road_line_color, upper_road_line_color)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(img,img, mask= mask)

cv2.imwrite('./Salida/hasv_1.jpg',hsv)
cv2.imwrite('./Salida/hasv_2.jpg',mask)
cv2.imwrite('./Salida/hasv_3.jpg',res)
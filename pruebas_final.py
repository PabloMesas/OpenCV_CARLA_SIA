from cv2 import cv2
import detection_car_driving as brain

img = cv2.imread('Originales/000355.png')

crazy_lines, degrees_list = brain.get_road_line(img)

for degree in degrees_list:
    print('Degree: ' , degree)


##############Mostrar ventanitas#################################
small_original = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
small_frame = cv2.resize(crazy_lines, (0,0), fx=0.5, fy=0.5)

cv2.imshow("original", small_original)
cv2.moveWindow('original',250,400)

cv2.imshow("processed", small_frame)
cv2.moveWindow('processed',950,400)

##################################################################

while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
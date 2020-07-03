import cv2
import numpy as np
import math

cap = cv2.VideoCapture('../test.mp4')

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

lower_blue = np.array([50, 158, 124])
upper_blue = np.array([150, 255, 255])

window_name = 'Image'
font = cv2.FONT_HERSHEY_SIMPLEX
org = (10, 50)
fontScale = 0.35
color = (255, 0, 0)
thickness = 1
string = "Distance among robots in px : "


def disCal(first, second):
    lenOne = first[0] - second[0]
    lenTwo = first[1] - second[1]
    outPut = math.sqrt(math.pow(lenOne, 2) + math.pow(lenTwo, 2))
    return math.floor(outPut)


while cap.isOpened():
    coordinates = []
    disAmongRob = []
    if not ret:
        break

    # filtering blue color
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    filtered = cv2.bitwise_and(frame1, frame1, mask=mask)

    #  detecting edges
    edges = cv2.Canny(filtered, 100, 200)
    dilated = cv2.dilate(edges, None, iterations=10)
    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    #  drawing a rectangle around detected movements and calculating the centers of the objects
    for contour in contours:
        if cv2.contourArea(contour) < 50 or cv2.contourArea(contour) > 5000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        coordinates = coordinates + [(int(x + w / 2), int(y + h / 2))]
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)

    #  drawing a line among moving objects to give a visual representation of the distance
    if len(coordinates) > 1:
        for element in range(len(coordinates)):
            other = element+1

            while other < len(coordinates):
                other = other + 1
                cv2.line(frame1, coordinates[element], coordinates[other-1], (0, 255, 0), thickness=1, lineType=8)
                disAmongRob = disAmongRob + [disCal(coordinates[element], coordinates[other - 1])]

    frame1 = cv2.putText(frame1, string + str(disAmongRob), org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("frame", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

import cv2
import numpy as np
import math
import selector as s

cap = cv2.VideoCapture('../test.mp4')

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

s.setValues()

print(s.lRob, s.uRob)
print(s.lAr, s.uAr)

lowerRobot = s.lRob
upperRobot = s.uRob

lowerArena = s.lAr
upperArena = s.uAr

robotNumber = 1

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
    rNum = 0
    coordinates = []
    disAmongRob = []
    if not ret:
        break

    # filtering color of robot and arena color
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    maskRobot = cv2.inRange(hsv, lowerRobot, upperRobot)
    maskOfArena = cv2.inRange(hsv, lowerArena, upperArena)
    filteredRobot = cv2.bitwise_and(frame1, frame1, mask=maskRobot)
    filteredArena = cv2.bitwise_and(frame1, frame1, mask=maskOfArena)

    # detecting edges
    edgesOfRobot = cv2.Canny(filteredRobot, 100, 200)
    gray = cv2.cvtColor(filteredArena, cv2.COLOR_BGR2GRAY)
    padded = np.pad(gray, (2, 2), 'constant')
    edgesOfArena = cv2.Canny(padded, 100, 200)
    dilatedRobot = cv2.dilate(edgesOfRobot, None, iterations=10)
    dilatedArena = cv2.dilate(edgesOfArena, None, iterations=2)
    contoursOfRobot, _ = cv2.findContours(dilatedRobot, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contoursOfArena, _ = cv2.findContours(dilatedArena, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    #  drawing a rectangle around Arena
    areas = [cv2.contourArea(c) for c in contoursOfArena]
    max_index = np.argmax(areas)
    cnt = contoursOfArena[max_index]
    (x, y, w, h) = cv2.boundingRect(cnt)
    cv2.rectangle(frame1, (x, y), (x + w-5, y + h-5), (0, 0, 255), 2)

    #  drawing a rectangle around robots and calculating the centers of the objects
    for contour in contoursOfRobot:
        if cv2.contourArea(contour) < 50 or cv2.contourArea(contour) > 5000:
            continue

        rNum = rNum + 1

        (x, y, w, h) = cv2.boundingRect(contour)
        coordinates = coordinates + [(int(x + w / 2), int(y + h / 2))]
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)
        frame1 = cv2.putText(frame1, "robot " + str(rNum), (x + 1, y + 1), font, fontScale, color, thickness, cv2.LINE_AA)

    #  drawing a line among moving objects to give a visual representation of the distance
    if len(coordinates) > 1:
        for element in range(len(coordinates)):
            other = element+1

            while other < len(coordinates):
                other = other + 1
                cv2.line(frame1, coordinates[element], coordinates[other-1], (0, 255, 0), thickness=1, lineType=8)
                disAmongRob = disAmongRob + [disCal(coordinates[element], coordinates[other - 1])]

    #  displaying the distances
    frame1 = cv2.putText(frame1, string + str(disAmongRob), org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("frame", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

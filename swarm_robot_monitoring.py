import cv2
import numpy as np
import math
import selector as s
import testframe as tf

# path of the video  file
path = '../test.mp4'

cap = cv2.VideoCapture(path)

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

tf.testFrame(path)
tf.troubleShooter()

s.setValues()

print(s.lRob, s.uRob)
print(s.lAr, s.uAr)

# for color filtering of the robots
lowerRobot = s.lRob
upperRobot = s.uRob

# for color filtering of the arena
lowerArena = s.lAr
upperArena = s.uAr

# variables defining
robotNumber = 1
border = ()
coordinates = []

window_name = 'Image'
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.35
colorOne = (255, 0, 0)
colorTwo = (0, 0, 255)
stringOne = "Distance among robots in px : "
stringTwo = "Distance from robots to left border in px : "
stringThree = "Distance from robots to top border in px : "


# calculating coordinates of the robots
def coordinatesCal(con):
    global rNum
    global frame1
    outPut = []
    for contour in con:
        if cv2.contourArea(contour) < 50 or cv2.contourArea(contour) > 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)
        rNum = rNum + 1
        frame1 = cv2.putText(frame1, "robot " + str(rNum), (x + 1, y + 1), font, fontScale, colorOne, 1, cv2.LINE_AA)
        outPut = outPut + [(int(x + w / 2), int(y + h / 2))]
    return outPut


# this function calculates the distance between two coordinates.
def disCal(first, second):
    lenOne = first[0] - second[0]
    lenTwo = first[1] - second[1]
    outPut = math.sqrt(math.pow(lenOne, 2) + math.pow(lenTwo, 2))
    return math.floor(outPut)


# drawing line between robots and calculating distance between
def betweenRobs(cods):
    global frame1
    if len(cods) > 1:
        for element in range(len(cods)):
            other = element + 1

            while other < len(cods):
                other = other + 1
                cv2.line(frame1, cods[element], cods[other - 1], (255, 0, 0), thickness=1, lineType=8)
                distance = disCal(cods[element], cods[other - 1])
                xOrg = int((cods[element][0] + cods[other - 1][0]) / 2)
                yOrg = int((cods[element][1] + cods[other - 1][1]) / 2)
                frame1 = cv2.putText(frame1, "px:" + str(distance), (xOrg, yOrg), font, 0.35, colorOne, 1, cv2.LINE_AA)


# this function calculates the distance from left border + display the value
def disToLeft(robot):
    global frame1
    dis = robot[0] - border[0]
    org = (int((robot[0] - border[0]) / 2), robot[1])
    frame1 = cv2.putText(frame1, "px : " + str(dis), org, font, fontScale, colorTwo, 1, cv2.LINE_AA)
    cv2.line(frame1, robot, (border[0], robot[1]), (0, 0, 255), thickness=1, lineType=8)


# this function calculates the distance from bottom border + displaying the value
def disToTop(robot):
    global frame1
    dis = robot[1] - border[1]
    org = (robot[0], int((robot[1] - border[0]) / 2))
    frame1 = cv2.putText(frame1, "px : " + str(dis), org, font, fontScale, colorTwo, 1, cv2.LINE_AA)
    cv2.line(frame1, robot, (robot[0], border[1]), (0, 0, 255), thickness=1, lineType=8)


#  main
while cap.isOpened():
    rNum = 0
    coordinates = []

    if not ret:
        break

    # filtering color of robot and color of the arena
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
    try:
        areas = [cv2.contourArea(c) for c in contoursOfArena]
        max_index = np.argmax(areas)
        cnt = contoursOfArena[max_index]
        (xx, yy, ww, hh) = cv2.boundingRect(cnt)
        cv2.rectangle(frame1, (xx, yy), (xx + ww - 5, yy + hh - 5), (0, 0, 255), 2)
        border = (xx, yy)
    except ValueError:
        pass

    #  drawing a rectangle around robots and calculating the coordinates of the robots
    coordinates = coordinatesCal(contoursOfRobot)

    #  drawing a line among robots objects to give a visual representation of the distance and calculating
    #  and displaying distances
    betweenRobs(coordinates)

    # calculating and displaying distances to border
    list(map(disToLeft, coordinates))
    list(map(disToTop, coordinates))

    cv2.imshow("Swarm Robot Monitoring( Press 'q' to stop)", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

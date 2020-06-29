import cv2
import numpy as np

cap = cv2.VideoCapture('../test.mp4')

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

lower_blue = np.array([78, 158, 124])
upper_blue = np.array([138, 255, 255])

while cap.isOpened():
    if not ret:
        break

    # filtering blue color
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    filtered = cv2.bitwise_and(frame1, frame1, mask=mask)

    #  detecting edges
    edges = cv2.Canny(filtered, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    coordinates = []

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
            other = element + 1

            while other < len(coordinates):
                other = other + 1
                cv2.line(frame1, coordinates[element], coordinates[other - 1], (0, 255, 0), thickness=1, lineType=8)

    cv2.imshow("frame", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

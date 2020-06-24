import cv2

cap = cv2.VideoCapture('../sample2.mp4')

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

while cap.isOpened():
    if not ret:
        break

    #  detecting movements
    edges = cv2.Canny(frame1, 100,200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    coordinates = []

    #  drawing a rectangle around detected movements and calculating the centers of the objects
    for contour in contours:
        if cv2.contourArea(contour) < 50 or cv2.contourArea(contour) > 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        coordinates = coordinates + [(int(x + w / 2), int(y + h / 2))]
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)

    print(len(coordinates))

    #  drawing a line among moving objects to give a visual representation of the distance
    if len(coordinates) > 1:
        for element in range(len(coordinates)):
            other = element + 1

            while other < len(coordinates):
                other = other + 1
                cv2.line(frame1, coordinates[element], coordinates[other - 1], (0, 255, 0), thickness=1, lineType=8)

    cv2.imshow("frame", edges)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

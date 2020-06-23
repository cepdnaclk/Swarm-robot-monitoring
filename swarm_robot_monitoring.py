import cv2

cap = cv2.VideoCapture('../sample3.mp4')

if not cap.isOpened():
    print("Error")

ret, frame1 = cap.read()
_, frame2 = cap.read()

while cap.isOpened():
    if not ret:
        break

    #  detecting movements
    diff = cv2.absdiff(frame1, frame2)
    final = diff
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    coordinates = []

    #  drawing a rectangle around detected movements and calculating the centers of the objects
    for contour in contours:
        if cv2.contourArea(contour) < 50 or cv2.contourArea(contour) > 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        coordinates = coordinates + [(int(x + w / 2), int(y + h / 2))]
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)

    #  drawing a line among moving objects to give a visual representation of the distance
    if len(coordinates) > 1:
        for element in range(len(coordinates)):
            other = element + 1

            while other < len(coordinates):
                print(element, other)
                print(coordinates[element], coordinates[other])
                other = other + 1
                cv2.line(frame1, coordinates[element], coordinates[other - 1], (0, 255, 0), thickness=1, lineType=8)

    cv2.imshow("frame", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

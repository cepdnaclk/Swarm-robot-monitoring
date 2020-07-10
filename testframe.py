import cv2

frame = cv2.imread("../test.jpg")

def testFrame(path):
    global frame
    print(" got the path : ", path)
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Error")

    ret, frame = cap.read()

    while cap.isOpened():

        if not ret:
            break

        cv2.imshow("press 'c' to select a test frame", frame)

        ret, frame = cap.read()

        if cv2.waitKey(20) & 0xFF == ord('c'):
            break

        print(frame)

    cv2.destroyAllWindows()

def troubleShooter():
    cv2.imshow("This will be used as the test frame( press any key to proceed)", frame)
    cv2.waitKey()
    cv2.destroyAllWindows()



import cv2

# sample frame for test purposes.This will update during the run time.
frame = cv2.imread("../test.jpg")

# This function is used to store a frame selected by the user.
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

    cv2.destroyAllWindows()


# This function was original used for troubleshoot purposes and later used to show the selected frame.
def troubleShooter():
    cv2.imshow("This will be used as the test frame( press any key to continue)", frame)
    cv2.waitKey()
    cv2.destroyAllWindows()



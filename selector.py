from tkinter import *
import cv2
import numpy as np

testImg = cv2.imread("../test.jpg")

v1 = v2 = v3 = v4 = v5 = v6 = 0

lRob = np.array([50, 50, 50])
uRob = np.array([100, 100, 100])
lAr = np.array([50, 50, 50])
uAr = np.array([200, 200, 200])

def valuesTest():
    lowerRobot = np.array([v1, v2, v3])
    upperRobot = np.array([v4, v5, v6])
    hsv = cv2.cvtColor(testImg, cv2.COLOR_BGR2HSV)
    maskRobot = cv2.inRange(hsv, lowerRobot, upperRobot)
    filteredRobot = cv2.bitwise_and(testImg, testImg, mask=maskRobot)
    cv2.imshow("test", filteredRobot)
    cv2.waitKey()
    cv2.destroyAllWindows()

def setRobotValues():
    global lRob
    global uRob
    lRob = np.array([v1, v2, v3])
    uRob = np.array([v4, v5, v6])
    print("values for robots are set")
    print(v1, v2, v3, v4, v5, v6)
    print(lRob, uRob)


def setArenaValues():
    global lAr
    global uAr
    lAr = np.array([v1, v2, v3])
    uAr = np.array([v4, v5, v6])
    arenaValues = [v1, v2, v3, v4, v5, v6]
    print("values for arena are set")
    print(v1, v2, v3, v4, v5, v6)
    print(lAr, uAr)


def setValues():

    master = Tk()
    master.geometry("400x500")

    w1 = Scale(master, from_=0, to=255, length=300, background='red', orient=HORIZONTAL)
    w1.pack()
    x = Label(master, text="Channel 1 lower limit")
    x.pack()
    w2 = Scale(master, from_=0, to=255, length=300, background='red', orient=HORIZONTAL)
    w2.pack()
    w2.set(255)
    x = Label(master, text="Channel 1 upper limit")
    x.pack()
    w3 = Scale(master, from_=0, to=255, length=300, background='green', orient=HORIZONTAL)
    w3.pack()
    x = Label(master, text="Channel 2 lower limit")
    x.pack()
    w4 = Scale(master, from_=0, to=255, length=300, background='green', orient=HORIZONTAL)
    w4.pack()
    w4.set(255)
    x = Label(master, text="Channel 2 upper limit")
    x.pack()
    w5 = Scale(master, from_=0, to=255, length=300, background='blue', orient=HORIZONTAL)
    w5.pack()
    x = Label(master, text="Channel 3 lower limit")
    x.pack()
    w6 = Scale(master, from_=0, to=255, length=300, background='blue', orient=HORIZONTAL)
    w6.pack()
    w6.set(255)
    x = Label(master, text="Channel 3 upper limit")
    x.pack()

    def setVs():
        global v1
        global v2
        global v3
        global v4
        global v5
        global v6

        v1 = w1.get()
        v2 = w3.get()
        v3 = w5.get()
        v4 = w2.get()
        v5 = w4.get()
        v6 = w6.get()

        valuesTest()

    Button(master, text='Test For Robots/Arena', bg='yellow', command=setVs).pack()
    Button(master, text='Set For Robots ', bg='orange', command=setRobotValues).pack()
    Button(master, text='Set For Arena ', bg='orange', command=setArenaValues).pack()

    mainloop()


print(lRob, uRob)
print(lAr, uAr)


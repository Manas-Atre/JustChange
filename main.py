import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
import mysql.connector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.9)
keys=[["Like1","Like2","Like3"],
      ["Like4","Like5","Like6"],
      ["Like7","Like8","Like9"]]

finalText=""



mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='manas')
cur=mydb.cursor()


def drawALL(img,buttonlist):

    for button in buttonlist:
        xCoordinate, yCoordinate = button.pos
        buttonWidth, buttonHeight = button.size
        cv2.rectangle(img, button.pos, (xCoordinate + buttonWidth, yCoordinate + buttonHeight), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (xCoordinate + 9, yCoordinate + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img


class LikeButton():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size



buttonlist=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonlist.append(LikeButton([100 * j + 50, 100 * i + 50], key))


class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2


path = "ImagesPNG"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 100, 50], imgType))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    img= drawALL(img,buttonlist)



    #Buttonimg= LikeButton.draw(Buttonimg)






    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

        for button in buttonlist:
            xCoordinate,yCoordinate=button.pos
            buttonWidth,buttonHeight=button.size
            if xCoordinate< lmList[8][0]<xCoordinate+buttonWidth and yCoordinate<lmList[8][1]<yCoordinate+buttonHeight:
                cv2.rectangle(img, button.pos, (xCoordinate + buttonWidth, yCoordinate + buttonHeight), (0, 255, 0),
                              cv2.FILLED)
                cv2.putText(img, button.text, (xCoordinate + 9, yCoordinate + 65), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 255, 255), 2)
                ##Mysql point next line
                finalText += button.text

                if button.text=="Like1":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11001,'grozian',3500)"
                    cur.execute(s)
                elif button.text=="Like2":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11022,'skyy',2500)"
                    cur.execute(s)
                elif button.text=="Like3":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(13003,'Fruu',3000)"
                    cur.execute(s)
                elif button.text=="Like4":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(14404,'dreww',3900)"
                    cur.execute(s)
                elif button.text == "Like5":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11055,'frost',10000)"
                    cur.execute(s)
                elif button.text == "Like6":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11006,'huee',5500)"
                    cur.execute(s)
                elif button.text == "Like7":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11077,'cristian',7777)"
                    cur.execute(s)
                elif button.text == "Like8":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11001,'soul',12000)"
                    cur.execute(s)
                elif button.text == "Like9":
                    s = "INSERT INTO silkaccessories(productid,productname,price) VALUES(11001,'solomid',7500)"
                    cur.execute(s)
                sleep(0.9)

    mydb.commit()
    #cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    #cv2.putText(img,"Like Counter",(60,425),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)



    try:

        for imgObject in listImg:

            # Draw for JPG image
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)

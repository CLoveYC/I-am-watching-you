import cv2

class FaceIn:
    def __init__(self):  # 初始化
        data = {"flag": False, "image": None} #flag:是否有人臉
        self.data = data

    def detectFace(self, img):
        self.data["flag"] = False
        self.data["image"] = img 
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #將圖片轉成灰階
        color = (0, 255, 0)
        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faceRects = face_classifier.detectMultiScale(
            grayImg, scaleFactor=1.25, minNeighbors=3, minSize=(32, 32)) #進行人臉辨識

        if len(faceRects): #如果有人臉
            self.data["flag"] = True
            for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(img, (x, y), (x + h, y + w), color, 2) #為人臉加上框
            self.data["image"] = img

        return self.data #回傳data

import threading, datetime, os
import imutils
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from FaceIn import *
from CaptureImage import *

class CameraEvents:

    thread: threading.Thread
    stopEvent: threading.Event
    root: tk.Tk

    def __init__(self, outputPath): # 初始化
        self.outputPath = outputPath
        self.face_in = FaceIn()
        self.webcam = CaptureImage()

        self.createUI()
        self.frame = None

        self.create_event()
        
    def createUI(self):
        self.root = tk.Tk()
        label = tk.Label(self.root, font='Arial 20', text="輸入相機網址")
        label.pack()
        frame = tk.Frame(self.root) # 將使用者輸入和確認按鈕綁在一起
        entry = tk.Entry(frame, width=30, font='Arial 20') # 使用者輸入
        entry.pack(side="left")
        # 確認按鈕
        enter_button = tk.Button(frame, text="Enter", height=2, width=7,
                                 command=lambda entry=entry: self.set_url(entry))
        enter_button.pack(side="right")
        frame.pack()
        
        # 處理無訊號時輸出的圖片
        self.no_signal = cv2.imread("no_signal.jpg")
        self.no_signal = imutils.resize(self.no_signal, width=600)
        self.no_signal = cv2.cvtColor(self.no_signal, cv2.COLOR_BGR2RGB)
        self.no_signal = Image.fromarray(self.no_signal)
        self.no_signal = ImageTk.PhotoImage(self.no_signal)

        # 及時輸出監控畫面視窗
        self.panel = tk.Label(image=self.no_signal)
        self.panel.pack()
        snapshot_button = tk.Button(self.root, text="Snapshot", command=self.takeSnapshot) # 拍照
        snapshot_button.pack(side="bottom", fill="both", padx=10, pady=10)

    def create_event(self):
        self.stopEvent = threading.Event() # 偵測是否終止的事件
        self.thread = threading.Thread(target=self.videoLoop, args=()) 
        self.thread.start() # 開始顯示畫面
        self.root.wm_title("Camera Events")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose) # 關閉視窗時結束程式

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                try:
                    self.frame = self.webcam.capture_image()
                    image = self.frame.copy() # 複製原始圖像做截圖用
                    image = imutils.resize(image, width=600) # 調大小
                    face = self.face_in.detectFace(image) # 丟到人臉偵測部分
                    if face["flag"]: # 偵測到圖像
                        self.takeSnapshot()
                        image = face["image"] # 原始圖像

                    # 轉成可以用tkinter顯示的圖片
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)

                    self.panel.configure(image=image)
                    self.panel.image = image
                except: # 沒偵測到相機或圖片有問題
                    self.panel.configure(image=self.no_signal)
                    self.panel.image = self.no_signal
                
        except:
            print("[INFO] caught a RuntimeError")
            
    def takeSnapshot(self):
        if self.frame is None:
            print("[INFO] caught a RuntimeError, frame is not defined")
            return
        ts = datetime.datetime.now() # 取時間當檔名
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename)) # 路徑
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(p))
        
    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.root.quit()
        os._exit(0) # 強制關閉視窗

    def set_url(self, entry: tk.Entry):
        url = entry.get()
        entry.delete(0, "end")
        self.webcam.set_url(url)

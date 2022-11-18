import numpy as np
import cv2
import requests

class CaptureImage:
    def __init__(self): #初始化
        self.camera_url = None
    
    def set_url(self,url): #設置(更改)相機網址
        self.camera_url = f"{url}/shot.jpg"
    
    def capture_image(self):
        image_response = requests.get(self.camera_url)#獲取圖片資訊
        image_response.raise_for_status()
        image_arr = np.array(bytearray(image_response.content), dtype=np.uint8)
        image = cv2.imdecode(image_arr, -1) #將圖片轉檔
        return image #回傳圖片

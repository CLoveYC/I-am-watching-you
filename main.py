from CameraEvents import *

print("[INFO] get camera...")
path = os.path.dirname(__file__) + "\Capture_Image" #設定圖片存檔路徑
if not os.path.isdir(path): #如果無資料夾，就創建新資料夾
    os.mkdir(path)

camara_events = CameraEvents(path) 
camara_events.root.mainloop()   #開啟視窗
# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
import cv2
import urllib.request
import numpy as np

# 本來應該要有https，但因為安全性的考量，所以我們在測試時不管安全性問題。
# 手機要裝IP camera
url='http://192.168.184.181:8080/shot.jpg'

class IPCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # 將檔案讀進來轉換為可以處理的型態
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        image=cv2.imdecode(imgNp,-1)
        # 網路傳輸較慢，所以將影像縮小
        image=cv2.resize(image,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_AREA)
        return image
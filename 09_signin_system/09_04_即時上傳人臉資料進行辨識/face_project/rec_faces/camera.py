# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
import cv2

class VideoCamera(object):
    def __init__(self):
        # 利用opencv開啟攝影機
        cap=cv2.VideoCapture(0)
        # cap.set(3,320)
        # cap.set(4,240)
        self.video=cap
        # self.video = cv2.VideoCapture(0)
        # self.video.set(3,320)
        # self.video.set(4,240)
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # 使用jpg當做原始影像格式回傳
        # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        image=cv2.resize(image,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_AREA)
        # ret, jpeg = cv2.imencode('.jpg', image)
        # return jpeg
        return image
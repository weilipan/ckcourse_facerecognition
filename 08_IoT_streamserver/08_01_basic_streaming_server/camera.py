# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
import cv2

class VideoCamera(object):
    def __init__(self):
        # 利用opencv開啟攝影機
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # 使用jpg當做原始影像格式回傳
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
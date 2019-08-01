# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
import math
from sklearn import neighbors
import pickle #用來將python的資料序列化，可用以存檔和讀檔，用以將辨識完的結果存檔或讀檔。 
import cv2
from face_recognition import face_locations, load_image_file, face_encodings,compare_faces,face_distance
from PIL import ImageFont, ImageDraw, Image
import numpy as np
#記錄時間用
import datetime
import time

class FaceRec(object):
    def __init__(self,frame):
        # self.frame = cv2.imdecode(frame)
        self.frame=frame
        self.data= self.readdata('TrainingData')

    def __del__(self):
        del self.data

    def readdata(self,dataname):
        with open(dataname, 'rb') as f:
            return pickle.load(f)

    def predict(self,distance_threshold=0.1):
        data=self.data
        # 讀入需要預測的影像,請記得轉回RGB
        rgb_frame=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        # 定位該影像的人臉位置
        unknown_face_locations = face_locations(rgb_frame)

        if len(unknown_face_locations)==0:# 若找不到任何的人臉，則回傳空的結果,則圖案不會有任何變化。
            # 請記得要再將RGB轉回BGR
            # 呈現影像
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
 
        unknown_face_encodings = face_encodings(rgb_frame,unknown_face_locations)

        # 將已知的人名及特徵取出
        known_faces_names=list(self.data.keys())
        known_faces_encodings=list(self.data.values())
        
        # 輸入中文字用
        pil_im = Image.fromarray(rgb_frame)
        fontPath = "edukai-3.ttf"
        font = ImageFont.truetype(fontPath, 16)
        # 準備畫框及寫上文字
        draw = ImageDraw.Draw(pil_im)

        for (top, right, bottom, left), unknown in zip(unknown_face_locations, unknown_face_encodings):
            name="未知人員"
            #可以有第3個參數(tolerance)用來設定是否要嚴格一點，0.6為預設值，值愈小則愈嚴格
            result = compare_faces(known_faces_encodings, unknown,distance_threshold)
            print(result)
            result=list(map(lambda x:x.all(),result))
            # if True in result:
            if True in result:
                first_match_index = result.index(True) #找出第一個匹配的人臉
                name = known_faces_names[first_match_index] #找到對應的名字

            # 畫臉框
            draw.rectangle([left, top, right, bottom], outline=(0, 0, 255))
            # 畫文字底色
            draw.rectangle([left, bottom, right, bottom+10], fill=(0, 0, 255))
            # 填入文字
            draw.text((left, bottom),  name, font = font, fill = (255, 255, 0))
        
        frame = np.array(pil_im)
        # 請記得要再將RGB轉回BGR
        self.frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        # 呈現影像
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()
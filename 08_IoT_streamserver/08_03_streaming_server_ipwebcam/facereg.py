# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
import math
from sklearn import neighbors
import pickle #用來將python的資料序列化，可用以存檔和讀檔，用以將辨識完的結果存檔或讀檔。 
import cv2
import face_recognition
from face_recognition import face_locations, load_image_file, face_encodings
from PIL import ImageFont, ImageDraw, Image
import numpy as np

class FaceRec(object):
    def __init__(self,frame):
        self.frame = frame
        self.knn_clf= self.readclf('trained_knn_model.clf')

    def __del__(self):
        del self.knn_clf

    def readclf(self,model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    def predict(self,distance_threshold=0.4):
        knn_clf=self.knn_clf
        # 讀入需要預測的影像,請記得轉回RGB
        rgb_frame=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        # 定位該影像的人臉位置
        X_face_locations = face_locations(rgb_frame)
        # 若找不到任何的人臉，則回傳空的結果,則圖案不會有任何變化。
        if len(X_face_locations) == 0:
            return []

        # 將該影像的人臉進行特徵碼的擷取
        faces_encodings = face_encodings(rgb_frame, known_face_locations=X_face_locations)

        # 使用Knn找到最合適的對應人臉
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        print(closest_distances,rgb_frame.shape)
        # 目前的distance_threshold為0.4,要小於等於0.4才算是辨識成功，這個值可以自己調整。
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
        print(are_matches,len(are_matches[0]),len(are_matches[0][0]))
        #我弄不懂怎麼會有480筆資料，導致第50行要用rec.any(),看起來好像是寬和高
        # 回傳結果,姓名，位置，結果
        # print([(name, loc) if rec else ("unknown", loc) for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)])
        return [(name, loc) if rec.any() else ("unknown", loc) for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


    def show_prediction_labels_on_image(self,predictions):
        """
        將預測的結果視覺化.
        :param predictions: 利用KNN預測完的結果
        """
        self.frame= cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(self.frame)
        fontPath = "../../edukai-3.ttf"
        font = ImageFont.truetype(fontPath, 15)
        # 準備畫框及寫上文字
        draw = ImageDraw.Draw(pil_im)

        for name, (top, right, bottom, left) in predictions:
            # 畫臉框
            draw.rectangle([left, top, right, bottom], outline=(0, 0, 255))
            # 畫文字底色
            draw.rectangle([left, bottom, right, bottom+15], fill=(0, 0, 255))
            # 填入文字
            draw.text((left, bottom),  name, font = font, fill = (255, 255, 0))

        frame = np.array(pil_im)
        # 請記得要再將RGB轉回BGR
        self.frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        # 呈現影像
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def result(self):
        predictions = self.predict(self.frame)
        # 在文字命令列中輸出結果
        for name, (top, right, bottom, left) in predictions:
            print("- Found {} at ({}, {})".format(name, left, top))

        return self.show_prediction_labels_on_image(predictions)
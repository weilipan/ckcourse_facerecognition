# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 將相機當成攝影機用，利用while迴圈重複相機的動作就會得到攝影機的結果。
# 06_03是直接使用KNN已訓練好的檔案進行判斷。
import math
from sklearn import neighbors
from os.path import isdir, join, isfile, splitext
import pickle #用來將python的資料序列化，可用以存檔和讀檔，用以將辨識完的結果存檔或讀檔。 
import cv2
import face_recognition
from face_recognition import face_locations, load_image_file, face_encodings, load_image_file
from face_recognition.face_recognition_cli import image_files_in_folder
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# sudo modprobe bcm2835-v4l2
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 1) #改變FPS以降低樹莓派的負擔，但畫面看起來不流暢，如果是用PC就可以喔。

def predict(bgr_frame, model_path=None, distance_threshold=0.4):
    """
    利用訓練好的模型來預測未知的照片
    :bgr_frame: 攝影鏡頭的畫面
    :model_path:用來預測用的模型，與knn_clf必須二擇一，不能兩者皆無。
    :distance_threshold: (optional) 距離閾值，此值愈大，愈容易將未知的人員誤判為已知的人員。(我一直調整到0.4結果才正確)
    :return: 回傳預測完成的結果，此串列包含人臉位置及姓名 [(name, bounding box), ...]，若辨識不出來，則姓名會回傳'未知人員'。
    """
    # 若沒有傳入訓練好的模型，則產生錯誤警告訊息
    if model_path is None:
        raise Exception("必須要傳入訓練好的模型或訓練好的模型檔案路徑（供讀入之用）")

    # 讀入訓練好的模型存放檔
    with open(model_path, 'rb') as f:
        knn_clf = pickle.load(f)

    # 將影像轉換為face_recognition可以使用的rgb
    rgb_img = cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2RGB)
    # 定位該影像的人臉位置
    X_face_locations = face_locations(rgb_img)
    # 若找不到任何的人臉，則回傳空的結果。
    if len(X_face_locations) == 0:
        return []

    # 將該影像的人臉進行特徵碼的擷取
    faces_encodings = face_encodings(rgb_img, known_face_locations=X_face_locations)

    # 使用Knn找到最合適的對應人臉,k值設定為2（這可以自行調整）
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    print('closest_distances:{}'.format(closest_distances))
    # 目前的distance_threshold為0.4,要小於等於0.4才算是辨識成功，這個值可以自己調整。
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    #看看結果為何
    print(are_matches)
    # 回傳結果,姓名，位置，結果
    return [(name, loc) if rec.any() else ("unknown", loc) for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def show_prediction_labels_on_image(bgr_frame, predictions):
    """
    將預測的結果視覺化.
    :bgr_frame: 攝影傳回的影像
    :predictions: 利用KNN預測完的結果
    """
    # BGR轉換為RGB，人臉辨識用
    unknown_image = cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2RGB)

    # 輸入中文字用
    pil_im = Image.fromarray(unknown_image)
    fontPath = "../font/edukai-3.ttf"
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
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    return frame

while True:
    # 每次抓一個畫面
    result, frame = video_capture.read()

    # 將畫面變小
    frame=cv2.resize(frame,None,fx=0.25,fy=0.25,interpolation = cv2.INTER_AREA)
    
    # 臉部辨識
    predictions = predict(frame, model_path="trained_knn_model.clf")
    frame=show_prediction_labels_on_image(frame, predictions)
    
    # 呈現畫面
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
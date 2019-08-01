# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 本範例改寫自如下網址：
# https://github.com/ageitgey/face_recognition/blob/master/examples/web_service_example.py
# 使用python flask web framework進行簡易的網路服務
# 讓使用者透過簡易網路服務上傳照片，並由網路服務回傳辨識結果（json格式）顯示至網頁上。
# 可以用以下語法測試
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# 回傳值:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# Flask檔案上傳範例可參考: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# 使用前請先安裝flask
# $ pip3 install flask
# 以自己當成範本

from flask import Flask, jsonify, request, redirect, render_template, send_file
from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
import pickle
import cv2
import os
import time #建立檔案名稱用
from datetime import datetime
from os import chdir,getcwd,listdir #處理資料夾檔案
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import math
from sklearn import neighbors
from os import listdir,chdir,getcwd

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} #可以接受的副檔名

app = Flask(__name__)

#回傳是否為可接受的檔案格式類型，可以接受才准予上傳進行辨識
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # 確認是否為合法的檔案
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
            # request.url為目前的網址

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # 回傳結果
            return detect_faces_in_image(file)

    # 如果是不合法的檔案，則回傳至index.html
    return render_template('index.html')


#讀取特徵碼
def read_face_encodings():
    # 訓練好的資料二進位檔讀進來
    model_path='trained_knn_model.clf'
    # 讀入訓練好的模型存放檔
    with open(model_path, 'rb') as f:
        return pickle.load(f)
    

def detect_faces_in_image(file_stream):
    knn_clf=read_face_encodings()

    unknown_image=load_image_file(file_stream)

    # 定位該影像的人臉位置
    X_face_locations = face_locations(unknown_image)
    # 若找不到任何的人臉，則回傳空的結果。
    if len(X_face_locations) == 0:
        return []

    # 將該影像的人臉進行特徵碼的擷取
    faces_encodings = face_encodings(unknown_image, known_face_locations=X_face_locations)

    # 使用Knn找到最合適的對應人臉,k值設定為2（這可以自行調整）
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    print('closest_distances:{}'.format(closest_distances))
    # 目前的distance_threshold為0.4,要小於等於0.4才算是辨識成功，這個值可以自己調整。
    are_matches = [closest_distances[0][i][0] <= 0.4 for i in range(len(X_face_locations))]
    #看看結果為何
    print(are_matches)
    # 回傳結果,姓名，位置，結果
    predictions= [(name, loc) if rec.any() else ("unknown", loc) for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    # 輸入中文字用
    pil_im = Image.fromarray(unknown_image)
    fontPath = "../../font/edukai-3.ttf"
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
    timestamp = int(time.mktime(datetime.now().timetuple()))
    filename='static/{}.png'.format(timestamp)
    cv2.imwrite(filename,frame)

    return render_template('result.html', result=filename, ourl=request.url)

#要對外連線，記得要裝http
#sudo apt-get install apache2
#sudo service apache2 restart
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
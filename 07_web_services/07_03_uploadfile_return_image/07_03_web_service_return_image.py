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
    model_save_path='trainingcomplete'
    with open(model_save_path, 'rb') as f:
        return pickle.load(f)

    

def detect_faces_in_image(file_stream):
    known_faces_encodings=[] #存放特徵碼之用
    known_faces_names=[] #存放人名之用
    known_faces=read_face_encodings() #讀入特徵碼
    known_faces_names=list(known_faces.keys())
    known_faces_encodings=list(known_faces.values())

    unknown_image=load_image_file(file_stream)
    bgr_img=cv2.cvtColor(unknown_image,cv2.COLOR_RGB2BGR)

    # 找到該圖片所有人臉的位置與特徵值
    unknown_face_locations = face_locations(unknown_image)
    unknown_face_encodings = face_encodings(unknown_image,unknown_face_locations)
    print('找到的人臉位置：{}\n找到的特徵值：{}'.format(unknown_face_locations,unknown_face_encodings))

    # 輸入中文字用
    pil_im = Image.fromarray(unknown_image)
    fontPath = "../../font/edukai-3.ttf"
    font = ImageFont.truetype(fontPath, 8)
    # 準備畫框及寫上文字
    draw = ImageDraw.Draw(pil_im)

    for (top, right, bottom, left), unknown in zip(unknown_face_locations, unknown_face_encodings):
        name="未知人員"
        #可以有第3個參數(tolerance)用來設定是否要嚴格一點，0.6為預設值，值愈小則愈嚴格
        result = compare_faces(known_faces_encodings, unknown,0.4)
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
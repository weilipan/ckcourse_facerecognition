# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 本範例改寫自如下網址：
# https://github.com/ageitgey/face_recognition/blob/master/examples/web_service_example.py
# 使用python flask web framework進行簡易的網路服務
# 讓使用者透過簡易網路服務上傳照片，並由網路服務回傳辨識結果（json格式）顯示至網頁上。
# Flask檔案上傳範例可參考: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
# 使用前請先安裝flask
# $ pip3 install flask
# 以自己當成範本
# 請改寫範例檔，使得您的網路服務可以擴大到判斷班級有建立臉部檔案的同學。
# 原來只有判斷有沒有人臉和是不是潘老師
# 請你改寫成有沒有人臉，同時照片上有哪些可以判斷出來的人。
# 已提供兩個訓練好的檔案供你使用，看你要用傳統人臉辨識還是使用knn來處理。
# 本範例用傳統方式處理

from flask import Flask, jsonify, request, redirect
from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
import pickle

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} #可以接受的副檔名

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False #處理回傳的中文問題

#回傳是否為可接受的檔案格式類型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # 若上傳的檔案合法
    if request.method == 'POST':
        if 'file' not in request.files: 
            return redirect(request.url) 
            # request.url為目前的網址

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # 若檔案合法則進入辨識階段並回傳結果.
            return detect_faces_in_image(file)

    # 如果不合法則回傳上傳檔案的表單格式，請使用者重新上傳檔案:
    return '''
    <!doctype html>
    <title>上傳一張照片看看有認識的人嗎</title>
    <h1>上傳一張照片看看有沒有認識的人</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="上傳">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # 訓練好的資料二進位檔讀進來
    model_save_path='trainingcomplete'
    with open(model_save_path, 'rb') as f:
        known_faces = pickle.load(f)

    # 將已知的人名及特徵取出
    known_faces_names=list(known_faces.keys())
    known_faces_encodings=list(known_faces.values())

    # 載入上傳的檔案備進行辨識
    img = load_image_file(file_stream)

    # 找到該圖片所有人臉的位置與特徵值
    unknown_face_locations = face_locations(img)
    unknown_face_encodings = face_encodings(img,unknown_face_locations)
    
    face_found = False
    who_found = []

    if len(unknown_face_encodings) > 0: #如果有偵測到人臉
        face_found = True
        for unknown in unknown_face_encodings:
             #可以有第3個參數(tolerance)用來設定是否要嚴格一點，0.6為預設值，值愈小則愈嚴格
            result = compare_faces(known_faces_encodings, unknown,0.4)
            if True in result:
                first_match_index = result.index(True) #找出第一個匹配的人臉
                who_found.append(known_faces_names[first_match_index]) #找到對應的名字

    # 回傳結果呈現在網頁上
    result = {
        "有偵測到人臉嗎?": "{}".format("偵測到人臉" if face_found else "未偵測到人臉") ,
        "辨識出的人員?": "{}".format( who_found if len(who_found)!=0 else "辨識不出來。")
    }
    return jsonify(result)

#要對外連線，記得要裝http
#sudo apt-get install apache2
#sudo service apache2 restart

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
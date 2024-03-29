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

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
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
    <title>上傳一張照片看看是不是潘老師</title>
    <h1>上傳一張照片看看是不是潘老師</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="上傳">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # 事先做好的特徵碼face_recognition.face_encodings(img)，這是潘老師本人的臉部特徵。
    known_face_encoding = [-0.08564568310976028,
     0.042488012462854385, 
     0.028597690165042877, 
     -0.04968660697340965, 
     0.02170371823012829, 
     -0.11953499168157578, 
     -0.04424203559756279, 
     -0.18487617373466492, 
     0.10833730548620224, 
     -0.06825826317071915, 
     0.2772826850414276, 
     -0.06223772466182709, 
     -0.19383710622787476, 
     -0.09727951139211655, 
     -0.004259156063199043, 
     0.1796058565378189, 
     -0.20594052970409393, 
     -0.13727861642837524, 
     -0.04438190162181854, 
     -0.05232200771570206, 
     0.03584790229797363, 
     -0.05062868446111679, 
     0.045781154185533524, 
     0.041338760405778885, 
     -0.053177669644355774, 
     -0.33554938435554504, 
     -0.16953951120376587, 
     -0.08904010057449341,
     0.057096801698207855, 
     0.015077765099704266, 
     -0.012873204424977303, 
     0.06357349455356598, 
     -0.15934982895851135, 
     -0.05893244594335556, 
     0.08143573254346848, 
     0.08984348922967911, 
     0.02072562277317047, 
     -0.09377653896808624, 
     0.21445156633853912, 
     -0.0057470714673399925, 
     -0.11913567781448364, 
     -0.004615578800439835, 
     0.015073500573635101, 
     0.24345950782299042, 
     0.15415111184120178, 
     0.04320712015032768, 
     0.05482465773820877, 
     -0.11513914167881012, 
     0.06979844719171524, 
     -0.15205353498458862, 
     0.016801945865154266, 
     0.1580887883901596, 
     0.02947641722857952, 
     0.07677193731069565, 
     -0.0280710831284523, 
     -0.08300553262233734,
     0.08330290019512177, 
     0.08841918408870697, 
     -0.1683104783296585, 
     0.011688104830682278, 
     0.11029123514890671, 
     -0.13915124535560608,
     -0.0633399486541748, 
     -0.05632025748491287, 
     0.2285354733467102, 
     0.10543828457593918, 
     -0.11941581964492798, 
     -0.16594621539115906, 
     0.12421318143606186, 
     -0.122025266289711, 
     -0.0807454064488411, 
     -0.03298536688089371, 
     -0.18847492337226868, 
     -0.15139366686344147, 
     -0.2802066206932068, 
     0.030629877001047134, 
     0.37023454904556274, 
     0.08693376183509827, 
     -0.17198771238327026, 
     0.10789106786251068, 
     -0.0633167028427124, 
     0.0032390840351581573, 
     0.12772412598133087, 
     0.1251741647720337, 
     -0.030427396297454834, 
     0.0385698638856411, 
     -0.1160162091255188, 
     0.0007312027737498283, 
     0.19483308494091034, 
     -0.06557800620794296, 
     -0.019635183736681938, 
     0.2111915796995163, 
     -0.08501313626766205, 
     0.10440331697463989, 
     0.06404149532318115, 
     0.042207021266222, 
     -0.02695329487323761, 
     0.01904129609465599, 
     -0.10792763531208038, 
     -0.01412595622241497, 
     0.09657064080238342, 
     -0.020388079807162285, 
     0.02789737470448017, 
     0.08753019571304321, 
     -0.11983808875083923, 
     0.0813235342502594, 
     -0.025783902034163475, 
     0.051160506904125214, 
     0.04794862121343613, 
     -0.009650607593357563, 
     -0.06894952058792114, 
     -0.11550334841012955, 
     0.12428467720746994, 
     -0.18646714091300964, 
     0.19117392599582672, 
     0.21865542232990265, 
     0.039108626544475555, 
     0.09872417151927948, 
     0.0965527594089508, 
     0.1212773248553276, 
     -0.03316599130630493, 
     0.0002102591097354889, 
     -0.19894349575042725, 
     -0.011100423522293568, 
     0.04815482720732689, 
     0.07438644021749496, 
     0.032755374908447266, 
     0.004062127321958542]

    # 載入上傳的檔案備進行辨識
    img = face_recognition.load_image_file(file_stream)
    # 取得未知人臉的特徵碼
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_pan = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # 看看是不是潘老師的臉
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0],0.4)
        if match_results[0]:
            is_pan = True

    # 回傳結果呈現在網頁上
    result = {
        "有偵測到人臉嗎?": "{}".format("偵測到人臉" if face_found else "未偵測到人臉") ,
        "是潘老師嗎?": "{}".format("是" if is_pan else "不是")
    }
    return jsonify(result)

#要對外連線，記得要裝http
#sudo apt-get install apache2
#sudo service apache2 restart

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
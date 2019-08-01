# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 本範例整合雲端攝影機與即時人臉辨識，但需要先行訓練好的檔案，這裡是用knn訓練好的檔案，你要自己訓練一個，並將檔案更名為trained_knn_model.clf
# 才能使用本範例
from flask import Flask, render_template, Response
from camera import VideoCamera
from facereg import FaceRec
import time

app = Flask(__name__)
FRAME_RATE = 16 #調整每秒取樣張數

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        time.sleep(1/FRAME_RATE)
        frame = FaceRec(camera.get_frame()).result() 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
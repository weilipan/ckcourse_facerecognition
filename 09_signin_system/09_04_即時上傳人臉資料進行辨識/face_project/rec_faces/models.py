# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
from flask import render_template, Response, Blueprint, url_for, redirect
from face_project.rec_faces.camera import VideoCamera
from face_project.rec_faces.facereg import FaceRec
import time

facerec=Blueprint('facerec',__name__)
FRAME_RATE = 1 #調整每秒取樣張數

@facerec.route('/stream')
def stream():
    return render_template('stream.html')

def gen(camera):
    while True:
        time.sleep(1/FRAME_RATE)
        frame = FaceRec(camera.get_frame()).predict() 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@facerec.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
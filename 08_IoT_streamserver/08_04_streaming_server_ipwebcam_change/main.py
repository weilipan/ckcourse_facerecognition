# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 本範例可以自行更改ipcamera的位置（因為ipcamera會更改ip）
from flask import Flask,render_template,session,flash,redirect,url_for,Response
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import IPAddress
from flask_bootstrap import Bootstrap
from camera import IPCamera
from facereg import FaceRec
import time

app = Flask(__name__)
bootstrap=Bootstrap(app)

app.config['SECRET_KEY']='mykey'

FRAME_RATE = 1 #1 Frames per second

class UrlForm(FlaskForm):
    url=StringField('請輸入手機影像IP位置：',validators=[IPAddress(ipv4=True, ipv6=False, message='IPv4格式錯誤')])
    submit=SubmitField('Submit')

def gen(camera):
    while True:
        time.sleep(1/FRAME_RATE)
        frame = FaceRec(camera.get_frame()).result() #產生判斷物件
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    url=session.get('url')
    return Response(gen(IPCamera(url)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/stream')
def stream():
    url=session.get('url')
    if url is None:
        flash('目前沒有IP位置可供影像辨識之用')
        url=False
    return render_template('stream.html',url=url)

@app.route('/change_url',methods=['GET','POST'])
def change_url():
    form=UrlForm()
    if form.validate_on_submit():
        session['url']=form.url.data
        url=session.get('url')
        print(url)
        flash('目前的IP位置為：{}!'.format(url))
        return redirect(url_for('change_url'))
    return render_template('change_url.html',form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

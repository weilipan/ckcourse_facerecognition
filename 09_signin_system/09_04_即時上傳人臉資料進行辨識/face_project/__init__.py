# face_project/__init__.py
import os
# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))

from face_project.add_faces.views import add_forms
from face_project.rec_faces.models import facerec


app.register_blueprint(add_forms)
app.register_blueprint(facerec)
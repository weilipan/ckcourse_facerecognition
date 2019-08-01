# add_faces/views.py
# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
from flask import render_template,url_for,flash,redirect,request,Blueprint
from face_project.add_faces.forms import AddForm
from face_project.add_faces.pic_encoding import FaceEncode

add_forms = Blueprint('add_forms',__name__)

@add_forms.route('/add_pic',methods=['GET','POST'])
def add_pic():
    form=AddForm()

    if form.validate_on_submit():
        face_encode=FaceEncode(
        username=form.username.data,
        picture=form.picture.data,
        dataname='TrainingData')
        msg=face_encode.encodings()
        flash(msg)
        return redirect(url_for('add_forms.add_pic',form=form))
    return render_template('add_faces.html',form=form)

    

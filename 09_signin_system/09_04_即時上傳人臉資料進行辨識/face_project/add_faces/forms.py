# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

class AddForm(FlaskForm):
    username=StringField('請輸入人名：:',validators=[DataRequired()])
    picture = FileField('上傳辨識的照片：', validators=[FileAllowed(['jpg', 'png'])])
    submit=SubmitField('上傳照片')
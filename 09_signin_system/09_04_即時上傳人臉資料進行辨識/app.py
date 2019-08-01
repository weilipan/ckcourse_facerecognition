# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# app.py
from face_project import app
from flask import render_template

@app.route('/')
def index():
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)
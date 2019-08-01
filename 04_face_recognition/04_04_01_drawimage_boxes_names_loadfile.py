# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 人臉辨識套件基本運用：定義已知人臉的特徵值,所有已知人臉圖像皆置於train資料夾（請自行蒐集），
# 需要測試的影像置於test資料夾，利用os來走訪資料夾
# 判斷完成的結果請置於result資料夾
# 直接由traincomplete檔讀入訓練結果，節省時間。

from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
from os import chdir,getcwd,listdir #處理資料夾檔案
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import pickle

# 寫成二進位檔讀進來
model_save_path='trainingcomplete'
with open(model_save_path, 'rb') as f:
    known_faces = pickle.load(f)
#載入想要辨識的照片
bgr_img=cv2.imread('test/unknown.jpg')

# BGR轉換為RGB，人臉辨識用
unknown_image = cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGB)

# 找到該圖片所有人臉的位置與特徵值
unknown_face_locations = face_locations(unknown_image)
unknown_face_encodings = face_encodings(unknown_image,unknown_face_locations)

# 將已知的人名及特徵取出
known_faces_names=list(known_faces.keys())
known_faces_encodings=list(known_faces.values())

# 輸入中文字用
pil_im = Image.fromarray(unknown_image)
fontPath = "../font/edukai-3.ttf"
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
#第一個參數是視窗標題，第二個則是read()取得的影像
cv2.imshow('frame',frame)

#將影像存成png檔
cv2.imwrite('result/04_04.png',frame)
cv2.waitKey(0) #等待按下任意按鍵
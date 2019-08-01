# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 將相機當成攝影機用，利用while迴圈重複相機的動作就會得到攝影機的結果。
from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import pickle

# sudo modprobe bcm2835-v4l2
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 1) #改變FPS以降低樹莓派的負擔，但畫面看起來不流暢，如果是用PC就可以喔。

def frame_recongition(bgr_img):
    # 訓練好的資料二進位檔讀進來
    model_save_path='trainingcomplete'
    with open(model_save_path, 'rb') as f:
        known_faces = pickle.load(f)

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
    # 將結果回傳
    return frame

while True:
    # 每次抓一個畫面
    result, frame = video_capture.read()

    # 將畫面變小
    frame=cv2.resize(frame,None,fx=0.25,fy=0.25,interpolation = cv2.INTER_AREA)
    
    # 臉部辨識
    frame=frame_recongition(frame) 
    
    # 呈現畫面
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
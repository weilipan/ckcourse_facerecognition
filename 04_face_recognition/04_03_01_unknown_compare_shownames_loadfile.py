# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 人臉辨識套件基本運用：定義已知人臉的特徵值,所有已知人臉圖像皆置於train資料夾（請自行蒐集），
# 需要測試的影像置於test資料夾，利用os來走訪資料夾
# 判斷完成的結果請置於result資料夾
# 直接由traincomplete檔讀入訓練結果，節省時間。

from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
import cv2
import pickle

# 寫成二進位檔讀進來
model_save_path='trainingcomplete'
with open(model_save_path, 'rb') as f:
    known_faces = pickle.load(f)

# 將已知的人名及特徵取出
known_faces_names=list(known_faces.keys())
known_faces_encodings=list(known_faces.values())
    
#載入想要辨識的照片
bgr_img=cv2.imread('test/unknown.jpg')

# BGR轉換為RGB
unknown_image = cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGB)

# 找到該圖片所有人臉的位置與特徵值
unknown_face_locations = face_locations(unknown_image)
unknown_face_encodings = face_encodings(unknown_image,unknown_face_locations)

for unknown in unknown_face_encodings:
    name="未知人員"
    #可以有第3個參數(tolerance)用來設定是否要嚴格一點，0.6為預設值，值愈小則愈嚴格
    result = compare_faces(known_faces_encodings, unknown,0.4)
    if True in result:
        first_match_index = result.index(True) #找出第一個匹配的人臉
        name = known_faces_names[first_match_index] #找到對應的名字
    print(name) #名字印出來
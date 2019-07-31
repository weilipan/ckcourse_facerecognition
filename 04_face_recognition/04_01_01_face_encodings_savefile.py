# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 人臉辨識套件基本運用：定義已知人臉的特徵值,所有已知人臉圖像皆置於train資料夾（請自行蒐集），
# 需要測試的影像置於test資料夾，利用os來走訪資料夾
# 判斷完成的結果請置於result資料夾
# 將04_01_face_encodings.py的結果存成traincomplete檔，以利後續使用。

from face_recognition import face_locations, face_encodings, load_image_file
from os import chdir,getcwd,listdir #處理資料夾檔案
import pickle #另存新檔之用

traidir='train'
chdir(traidir) #指定目錄至train資料夾
print(getcwd()) # 看看目前的路徑
print(listdir())# 列出所有的檔案名稱

# 建立字典檔來處理已知人名與臉部特徵
known_faces=dict()
for filename in listdir():
     image=load_image_file(filename)
     name=filename.split('.')[0] #取出名字
     known_faces[name]=face_encodings(image)[0] 
     #取出特徵值，因為一張照片確定只有一個人臉，所以使用[0]來取得
print(known_faces) #印出來看看對不對

# 寫成二進位檔存起來
chdir('..')
model_save_path='trainingcomplete'
with open(model_save_path, 'wb') as f:
    pickle.dump(known_faces, f)

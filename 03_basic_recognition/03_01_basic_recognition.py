# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 人臉辨識套件基本運用
# 請自行新增"test.jpg"檔
import cv2 #載入opencv套件
from face_recognition import face_locations

# 利用opencv讀入檔案
bgr_img=cv2.imread('test.jpg')
# 檔案縮小為1/16
bgr_img=cv2.resize(bgr_img,None,fx=0.25,fy=0.25,interpolation = cv2.INTER_AREA)

# 將BGR轉成RGB讓face_recognition可以使用
rgb_img = cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGB)

# 將人臉座標位置標定出來。
face_locations = face_locations(rgb_img)

# 看看印出什麼資料
print(face_locations)
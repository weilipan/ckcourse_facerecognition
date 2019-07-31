# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 人臉辨識套件基本運用：將找到的人臉在圖像上框出來
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

# 看看印出什麼資料，因為回傳的是list含tuple的座標資料，所以使用for來走訪並印出
for face_location in face_locations:
    top,right,bottom,left=face_location
    cv2.rectangle(bgr_img,(left,top),(right,bottom),(255,0,0),1)
    blurimage=bgr_img[top:bottom, left:right]
    blurimage = cv2.GaussianBlur(blurimage, (99, 99), 30)
    bgr_img[top:bottom, left:right]=blurimage

cv2.imshow('opencv image',bgr_img)
#將影像存成png檔
cv2.imwrite('03_04.png',bgr_img)
cv2.waitKey(0) #等待按下任意按鍵
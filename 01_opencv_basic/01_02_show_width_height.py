# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 找影像的高、寬和頻道

import cv2 #載入opencv套件

#因為只接了相機模組，所以選擇第一個設備
cap=cv2.VideoCapture(0)

#ret會回傳True/False表示是否成功
#frame則會回傳當下的影像
ret ,frame=cap.read()
height, width, channels = frame.shape #讀出高、寬和頻道數
print(height,width,channels)


#第一個參數是視窗標題，第二個則是read()取得的影像
cv2.imshow('frame',frame)
#將影像存成png檔
cv2.imwrite('01_02.png',frame)
cap.release() #釋放資源
cv2.waitKey(0) #等待按下任意按鍵
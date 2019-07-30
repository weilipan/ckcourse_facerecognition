# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 本單元將學習如何開啟攝影機並將目前的畫面呈現出來
# 執行時請先在本機端開啟xming ，
# 接著在ssh中將v4l2(video for linux version 2)設備開啟:sudo modprobe bcm2835-v4l2

import cv2 #載入opencv套件

#因為只接了相機模組，所以選擇第一個設備
cap=cv2.VideoCapture(0)

#ret會回傳True/False表示是否成功
#frame則會回傳當下的影像
ret ,frame=cap.read()

#第一個參數是視窗標題，第二個則是第12行取得的影像
cv2.imshow('frame',frame)
#將影像存成png檔
cv2.imwrite('01_01.png',frame)
cap.release() #釋放資源
cv2.waitKey(0) #等待按下任意按鍵
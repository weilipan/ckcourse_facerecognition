# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 利用opencv畫出長方形

import cv2 #載入opencv套件

# 因為只接了相機模組，所以選擇第一個設備
cap=cv2.VideoCapture(0)

# ret會回傳True/False表示是否成功
# frame則會回傳當下的影像
ret ,frame=cap.read()
height, width, channels = frame.shape #讀出高、寬和頻道數，用以計算長方形要畫在哪裡
# 畫長方形，給定左上角和右下角，因為整張影像的原點(0,0)預設在左上角。
# 往左及往下x,y座標都是遞增，目前想要將長方形畫在底部。
# cv2.rectangle(影像, 左上角頂點座標, 右下角頂點座標, 顏色（BGR）, 線條寬度（-1則為填滿）)
cv2.rectangle(frame, (50, height-100), (width-50, height-50), (255, 0, 0), 1)
#第一個參數是視窗標題，第二個則是read()取得的影像
cv2.imshow('frame',frame)
#將影像存成png檔
cv2.imwrite('01_03.png',frame)
cap.release() #釋放資源
cv2.waitKey(0) #等待按下任意按鍵
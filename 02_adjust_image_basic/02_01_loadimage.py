# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 利用opencv開啟一張圖檔並秀出來
import cv2
import numpy as np

img=cv2.imread('01_05.png')

cv2.imshow('loadimage',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
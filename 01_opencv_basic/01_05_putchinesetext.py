# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 放入正體中文文字

import cv2 #載入opencv套件
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# 因為只接了相機模組，所以選擇第一個設備
cap=cv2.VideoCapture(0)

# ret會回傳True/False表示是否成功
# frame則會回傳當下的影像
ret ,frame=cap.read()
height, width, channels = frame.shape #讀出高、寬和頻道數，用以計算長方形要畫在哪裡

# 將BGR轉成RGB讓pillow套件可以使用
cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
pil_im = Image.fromarray(cv2_im)

text="臺北市立建國高級中學資訊科潘威歷老師"
# 指定 ttf 字體檔,目前是教育部標準楷書字形檔,請記得將字形檔放在專案資料夾中
fontPath = "../edukai-3.ttf"
font = ImageFont.truetype(fontPath, 30)

# 準備畫框及寫上文字
draw = ImageDraw.Draw(pil_im)
# 畫框
# ImageDraw.rectangle([左上x,左上y,右下x,右下y], fill=None, outline=None)
draw.rectangle([30, height-100, width-30, height-50], outline=(0, 0, 255))
# 畫填滿框
draw.rectangle([30, height-50, width-30, height-20], fill=(0, 0, 255))
# draw.text(文字左上角座標,  文字, 字型, 顏色)
draw.text((30, height-50),  text, font = font, fill = (255, 255, 0))

pil_im.save('01_05.png') #利用pillow存檔

# 轉回opencv格式圖像
frame = np.array(pil_im)
# 請記得要再將RGB轉回BGR
frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
#第一個參數是視窗標題，第二個則是read()取得的影像
cv2.imshow('frame',frame)

#將影像存成png檔
# cv2.imwrite('01_05.png',frame)
cap.release() #釋放資源
cv2.waitKey(0) #等待按下任意按鍵
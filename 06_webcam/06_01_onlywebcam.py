# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# 將相機當成攝影機用，利用while迴圈重複相機的動作就會得到攝影機的結果。
import cv2

# sudo modprobe bcm2835-v4l2
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 16)
#改變FPS以降低樹莓派的負擔，但畫面看起來不流暢，如果是用PC就可以喔。

while True:
    # 每次抓一個畫面
    result, frame = video_capture.read()

    # 將畫面變小
    frame=cv2.resize(frame,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_AREA)
    
    # 呈現畫面
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
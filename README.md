# ckcourse_facerecognition
建中資訊科潘威歷老師:人臉辨識課程
2019.08.26

◎基礎模擬環境建置教學：
因為樹莓派跑不動機器學習（如果量大的話），所以只好又回來使用windows。
windows要使用face recognition，第一個會遇到的問題是dlib裝不起來。
這時候要配合anaconda來處理，但目前的dlib版本只有支援到python3.6，但是最新版的anaconda已經到3.7了。
所以要教大家來安裝。
1.開啟anaconda Prompt
2.先將路徑移至我們要測試的資料夾。(cd 資料夾路徑)
3.建立測試環境： facerec是資料夾名稱，因為dlib目前只支援到python3.6，但最新版的anaconda都已經是python3.7了，所以要用虛擬環境處理。
conda create --name facerec python=3.6 請記得按y
4.啟動虛擬環境
activate facerec
（若要解除虛擬環境，請使用deactivate facerec）
5.看一下環境
conda info --envs

6.安裝虛擬環境的相關套件
已經整理好的套件檔可以用下列指令安裝
pip install -r requirements.txt

pip freeze > requirements.txt


◎單元一：基礎opencv教學
設備需求
本單元將學習如何開啟攝影機並將目前的畫面呈現出來，
執行時請先在本機端開啟xming ，
接著在ssh中將v4l2(video for linux version 2)設備開啟:sudo modprobe bcm2835-v4l2

# ckcourse_facerecognition
建中資訊科潘威歷老師:人臉辨識課程

【前情提要】
因為樹莓派跑不動機器學習（如果量大的話），所以只好又回來使用windows。
windows要使用face recognition，第一個會遇到的問題是dlib裝不起來。
這時候要配合anaconda來處理，但目前的dlib版本只有支援到python3.6，但是最新版的anaconda已經到3.7了。
所以要教大家來安裝。

【模擬環境建置步驟】
1. 開啟anaconda Prompt
2. 先將路徑移至我們要測試的資料夾
3. 建立測試環境： facerec是資料夾名稱，因為dlib目前只支援到python3.6，但最新版的anaconda都已經是python3.7了，所以要用虛擬環境處理。
   conda create --name facerec python=3.6  請記得y
4. 啟動虛擬環境
   activate facerec （若要離開虛擬環境，請使用deactivate facerec）
5. 看一下環境
   conda info --envs
6. 將dlib抓到該目錄 這個步驟很重要 看一下下面的介紹
   http://maxlai.cc/2018/08/24/windows-python36-quickly-install-face-recognition/
   （還是要安裝visual studio 2015以上版本，請選擇C/C++桌面套件和python套件，不然下面的步驟會出現錯誤。）
   dlib-19.8.1-cp36-cp36m-win_amd64.whl這個檔要先下載(下載網址：https://pypi.org/simple/dlib/) 
   接著進入上述檔案所在位置。
   pip install dlib-19.8.1-cp36-cp36m-win_amd64.whl
   pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
   pip install -U scikit-learn
   pip install opencv-contrib-python
   pip install face_recognition 
7. 已經整理好的套件檔可以用下列指令安裝 requirements.txt
   pip install -r requirements.txt
8. 虛擬環境的相關套件 pip freeze > requirements.txt











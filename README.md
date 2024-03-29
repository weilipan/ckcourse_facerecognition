# ckcourse_facerecognition
建中資訊科潘威歷老師:人臉辨識課程

# 【模擬環境建置步驟】
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
   pip install scikit-learn==0.20.3
   pip install opencv-contrib-python
   pip install face_recognition 
7. 已經整理好的套件檔可以用下列指令安裝 requirements.txt
   pip install -r requirements.txt
8. 虛擬環境的相關套件 pip freeze > requirements.txt

# 【相關所需硬體】
1. 簡配：含前鏡頭的筆電。
2. 小全配：電腦主機+網路攝影機。
3. 大全配：樹莓派+相機模組+筆電。
4. 超值全餐：樹莓派+相機模組+筆電+手機。

![](https://i.imgur.com/WeT3O7a.png)



# 單元一 opencv基本操作
1. 學會如何啟動相機。
2. 學會如何擷取影像。
3. 學會如何畫框。

![](https://i.imgur.com/SmBJnr2.png)
 
4. 學會如何於影像中置入文字。
5. 學會如何於影像中置入中文字。
![](https://i.imgur.com/l5PwmAN.png)

# 單元二 如何調整影像
1. 學會如何載入影像至程式中。
2. 學會如何調整影像大小。（圖像過大有時會造成樹莓派跑不動）

# 單元三 基礎人臉辨識操作
1. 熟悉face recognition套件操作。

2. 學會如何取得人臉位置。
3. 學會如何框出人臉位置。
4. 學會如何找出人臉特徵值。
5. 學會利用opencv變更影像（如馬賽克）。

![](https://i.imgur.com/puy9hAY.png)



# 單元四 進階人臉辨識操作
> 需要訓練的人臉資料請自行置於train資料夾（請注意每張相片只能有一個人臉，超過不予訓練）

> 用來測試結果的影像請置於test資料夾。

> 完成人臉辨識的影像資料會置於result資料夾。

> 訓練完成的資料會存成單獨檔案，檔名為trainingcomplete。

1. 學會如何取得特徵值。
2. 學會如何將上述取得的特徵值另存檔案以利後續操作。
3. 學會如何進行比對。
4. 將比對後的資料以文字訊息呈現出來。
5. 將辨識後的結果（姓名、文字）直接與影像結合呈現出來。

# 【樹莓派KNN環境建置步驟】
1. 請確定opencv已安裝好了（自行上網搜尋安裝方式，我自己是看這篇[https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/](https://)）。
2. KNN需要使用scikit-learn套件，使用前需要先安裝。

> 如果沒有pip3，請用語法先行安裝：sudo apt-get remove python3-pip; sudo apt-get install python3-pip
> 
> 如果套件有衝突，請用下方語法再裝一次
> 
> pip3 uninstall -y numpy scipy pandas scikit-learn
> 
> sudo apt update
> 
> sudo apt install python3-numpy python3-scipy python3-matplotlib python3-pandas python3-sklearn

# 單元五 KNN人臉辨識操作
> 為了加強判斷精準度，我們導入KNN機器學習演算法。

> train資料夾放置的是每個人訓練用的照片，資料夾名稱建議可設定為人名，該人名資料夾中就放置該人員的相關照片（可放多張照片）用以訓練。

> 用來測試結果的影像請置於test資料夾。

> 訓練完成的資料會存成單獨檔案，檔名為trained_knn_model.clf

1. 學會如何蒐集大家的人臉資料，可利用各式數位教學平台進行蒐集。
2. 學會如何利用KNN演算法進行訓練。
3. 學會利用已訓練好的KNN演算法進行判斷。
4. 將辨識後的結果（姓名、文字）直接與影像結合呈現出來。

![](https://i.imgur.com/Uk73aOT.png)



# 單元六 AR擴增實境基礎實作
1. 啟動攝影機。
2. 每拍一張影像便進行人臉辨識，利用攝影機造成即時辨識人名的效果（基礎AR擴增實境的效果）。
3. 可自行選擇要直接使用face recognition套件或利用KNN演算法訓練好的資料進行處理。

![](https://i.imgur.com/YNwFN1j.png)

# 單元七 人臉辨識網路服務
1. 利用python flask web framework套件，啟動網路服務。
2. 使用者上傳影像檔至網路伺服器，由伺服器進行辨識後回傳辨識結果。
3. 將辨識結果即時與原影像結果後回傳至網頁呈現。

# 單元八 物聯網、人臉辨識基礎實作
1. 利用手機的便利性與機動性（雲端攝影機），即時將手機所擷取至的影像回傳至伺服器端進行人臉辨識。
2. 學會如何將手機影像回傳至伺服器，由網頁即時呈現出來。
3. 學會如何將手機影像回傳至伺服器，伺服器進行人臉辨識後將結果即時呈現於網頁。

![](https://i.imgur.com/S93AZYe.png)



# 單元九 課堂即時人臉辨識點名系統
> 本單元使用到flask 和 sqlite進行資料庫整合，為較進階實作，可直接於課堂上進行人臉辨識點名
![](https://i.imgur.com/gJwyYr4.png)



















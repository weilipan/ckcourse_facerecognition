"""
# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
前面的範例皆是使用傳統HOG的方式進行人臉辨識，接下來我們要使用機器學習來辨識，這次使用的演算去是KNN。
我們將已知的大量已知人臉的資料讓機器進行學習，學習完成後，利用學習完成後的結果進行未知照片的辨識。
和傳統的方式一樣，只是中間學習的方式不同。
關於KNN演算法的說明，請參閱：https://zh.wikipedia.org/wiki/%E6%9C%80%E8%BF%91%E9%84%B0%E5%B1%85%E6%B3%95
請注意：無論是分類還是回歸，衡量鄰居的權重都非常有用，使較近鄰居的權重比較遠鄰居的權重大。例如，一種常見的加權方案是給每個鄰居權重賦值為1/ d，其中d是到鄰居的距離。

此程式的使用方式:
1. 將已知的照片放入照片資料夾中，同時依照不同人員建置不同的子資料夾，並將人員照片置於其中，以用做為機器學習之用。
2. 呼叫train方法進行訓練。（若想要將訓練結果儲存下來，請記得給定'model_save_path'參數，這樣就可以重複使用訓練而不必每次都要重新訓練一次） 
3. 呼叫predict方式，回傳訓練完成的結果。
請注意這個範例會使用到scikit-learn套件，使用前請先安裝
安裝語法如後（將其他有關的也裝一裝）：
如果沒有pip3，請用語法先行安裝：sudo apt-get remove python3-pip; sudo apt-get install python3-pip
如果套件有衝突，請用下方語法再裝一次
pip3 uninstall -y numpy scipy pandas scikit-learn
sudo apt update
sudo apt install python3-numpy python3-scipy python3-pandas python3-sklearn 
"""
import math
from sklearn import neighbors
from os import listdir
from os.path import isdir, join, isfile, splitext
import pickle #用來將python的資料序列化，可用以存檔和讀檔，用以將辨識完的結果存檔或讀檔。 
import cv2
import face_recognition
from face_recognition import face_locations, load_image_file, face_encodings, load_image_file
from face_recognition.face_recognition_cli import image_files_in_folder

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    """
    利用大量資料訓練knn
    :model_save_path: (optional) 將訓練好的模型儲存起來所使用的路徑
    :n_neighbors: (optional) KNN演算法的K值,選取最近的K個鄰居當做參考。
    :knn_algo: (optional) knn演算法的選擇，可參照https://scikit-learn.org/stable/modules/neighbors.html
    :verbose: verbosity of training #這個參數用來展示訓練的細部過程，若為True，則將過程訊息皆顯示出來。
    :return: 回傳knn訓練好的模型
    """
    
    # 訓練用的x值,y值串列
    X = []
    y = []

    # 將每個已知人員的人臉資料讀進來

    for class_dir in listdir(train_dir):
        if not isdir(join(train_dir, class_dir)):
            #如果目前檔案名稱不是資料夾，則進行下一次的迴圈，繼續找下一個子資料夾
            continue

        # 進到子資料夾中，將目前已知人員的所有照片讀進來進行辨識
        for img_path in image_files_in_folder(join(train_dir, class_dir)):
            image = load_image_file(img_path) #讀入檔案
            face_bounding_boxes = face_locations(image) #抓出人臉位置

            if len(face_bounding_boxes) != 1:
                # 如果該判斷該照片中並非只包含1個人臉的情況，跳過這張照片不判讀。
                if verbose: #若verbose為True（表示需要顯示目前的處理情形），則印出下列的訊息。
                    print("目前這張照片 {} 不適合做為訓練之用，原因是: {}".format(img_path,
                     "本照片沒有人臉" if len(face_bounding_boxes) < 1 else "本照片人數為2人以上"))
            else:
                # 將判讀的結果納入訓練集X中
                print("開始納入資料集")
                X.append(face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                # 對應的人名（資料夾名稱）納入訓練集y中
                y.append(class_dir)
            print(img_path,X,y)

    # 決定要使用幾個鄰居做為權重之用，就是要最近的幾個鄰居做為參照-也就是KNN演算法的K值。
    if n_neighbors is None: #如果傳入的參數沒有設定
        n_neighbors = int(round(math.sqrt(len(X)))) #則設定為長度開方平再四捨五入取整數，這段可以自己改。
        if verbose: #如果verbose為True，則印出本段處理的訊息。
            print("自動選擇的鄰居數為{}".format(n_neighbors))

    # 建立KNN分類器，傳入K值，選擇演算法為BallTree，weights為distance（根據距離給予不同的權重，另外還有uniform代表一樣比重）
    # 詳細說明請參照https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    
    # 這行就訓練完成。
    knn_clf.fit(X, y)

    # 如果有指定好檔名，則將訓練好的模型存起來
    if model_save_path is not None:
        #利用下列語法存成二進位檔
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    return knn_clf #回傳訓練好的模型。

if __name__ == "__main__":
    # 訓練分類器並將訓練好的模型儲存起來
    # 如果已經訓練過也儲存起來
    print("訓練 KNN 分類器...")
    traindir='train' #訓練資料夾的位置
    classifier = train(traindir, model_save_path="trained_knn_model.clf", n_neighbors=1)
    print("訓練完成!")
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

def predict(X_img_path, model_path=None, distance_threshold=0.4):
    """
    利用訓練好的模型來預測未知的照片
    :X_img_path: 未知照片的檔案路徑
    :model_path:用來預測用的模型，與knn_clf必須二擇一，不能兩者皆無。
    :distance_threshold: (optional) 距離閾值，此值愈大，愈容易將未知的人員誤判為已知的人員。(我一直調整到0.4結果才正確)
    :return: 回傳預測完成的結果，此串列包含人臉位置及姓名 [(name, bounding box), ...]，若辨識不出來，則姓名會回傳'未知人員'。
    """
    # 若該路徑不是檔案，或不是可接受的檔案類型，則產生錯誤警告訊息
    if not isfile(X_img_path) or splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("不正確的檔案名稱: {}".format(X_img_path))
    # 若沒有傳入訓練好的模型，則產生錯誤警告訊息
    if model_path is None:
        raise Exception("必須要傳入訓練好的模型或訓練好的模型檔案路徑（供讀入之用）")

    # 讀入訓練好的模型存放檔
    with open(model_path, 'rb') as f:
        knn_clf = pickle.load(f)

    # 讀入需要預測的影像
    X_img = load_image_file(X_img_path)
    # 定位該影像的人臉位置
    X_face_locations = face_locations(X_img)
    # 若找不到任何的人臉，則回傳空的結果。
    if len(X_face_locations) == 0:
        return []

    # 將該影像的人臉進行特徵碼的擷取
    faces_encodings = face_encodings(X_img, known_face_locations=X_face_locations)

    # 使用Knn找到最合適的對應人臉,k值設定為2（這可以自行調整）
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    print('closest_distances:{}'.format(closest_distances))
    # 目前的distance_threshold為0.4,要小於等於0.4才算是辨識成功，這個值可以自己調整。
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    #看看結果為何
    print(are_matches)
    # 回傳結果,姓名，位置，結果
    return [(name, loc) if rec.any() else ("unknown", loc) 
    for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
    '''
    上面那段的意思就是下面這一大串
    result=[]
    for name, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches):
        if rec.any():
            result.append((name, loc))
        else:
            result.append(("unknown", loc))
    return result
    '''
if __name__ == "__main__":
    # 使用訓練好的分類器模型進行未知影像的預測，樹莓派如果跑不動，建議先放一張就好或照片尺寸和解析度下降
    testdir='test'
    for image_file in listdir(testdir):
        full_file_path = join(testdir, image_file)

        print("正在尋找 {} 圖片中的人臉".format(full_file_path))

        # 使用訓練好的模型找出圖片中所有的人臉
        # 可以使用訓練好的模型檔案或訓練好的模型實體來進行預測,和183行對應
        predictions = predict(full_file_path, model_path="trained_knn_model.clf")

        # 在文字命令列中輸出結果
        for name, (top, right, bottom, left) in predictions:
            print("- 辨識出 {} ，人臉位置左上角座標位置為({}, {})，右下角座標位置為({}, {})".format(name, left, top, right, bottom))
# 製作日期:20190729
# 版本：V2.0
# 製作人員:建國高中資訊科潘威歷老師
# # add_faces/pic_encoding.py

from face_recognition import face_locations, face_encodings, load_image_file
from PIL import Image
import os.path #處理資料夾檔案
import pickle #另存新檔之用

class FaceEncode(object):
    def __init__(self,username,picture,dataname):
        self.username=username
        self.picture=picture
        self.dataname=dataname
        self.data=None

    def encodings(self):
        # 開啟檔案
        image=load_image_file(self.picture)
        pil_im = Image.fromarray(image)
        
        encoding_face=face_encodings(image)
        if len(encoding_face)==1:
            # 將特徵寫入資料庫
            if os.path.isfile(self.dataname): #如果檔案已存在
                with open(self.dataname,'rb') as f:
                    self.data=pickle.load(f) #開啟檔案後

                self.data[self.username]=encoding_face #將特徵值寫入
                print(self.data)
                with open(self.dataname,'wb') as f: #寫入檔案
                    pickle.dump(self.data,f)

            else: # 如果檔案不存在
                self.data={self.username:encoding_face}
                print(self.data)
                with open(self.dataname,'wb') as f: #寫入檔案
                    pickle.dump(self.data,f)

            filename=self.picture.filename 
            ext_type=filename.split('.')[-1]
            storage_filename=self.username+'.'+ext_type
            print(storage_filename)
            filepath=os.path.join('static','training_pics',storage_filename)
            pil_im.save(filepath)
            return '人臉辨識資料庫已建檔完成！'

        elif len(encoding_face)==0:
            return '找不到人臉喔，請重新上傳'
        else:
            return '該影像中超過1張以上人臉，無法編碼，請重新上傳只含1張人臉的資料。'

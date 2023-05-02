import cv2
import time
import os
import shutil
import bchlib

#設定BCH方程式
BCH_POLYNOMIAL = 65533
BCH_BITS = 16
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

h = 720
w = 1280




# 創建資料夾，若已存在便刪除後重建
def creatdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)



def VTF(Vpath):

    # 分離:原始檔案名稱、有效影格數、最後一幀寫入多少bits
    try:
        filename,frame_num,last_frame_pnum=str(Vpath.split("/")[-1])[:-4].split(",")
        frame_num=int(frame_num)
        last_frame_pnum=int(last_frame_pnum)
    except:
        return "FileError"

    # 將影片轉為影格
    creatdir("C:/ISG/VideoToFiles/images/"+filename)
    videoCapture = cv2.VideoCapture(Vpath)
    success, frame=videoCapture.read()
    t=0
    while success:
        cv2.imwrite("C:/ISG/VideoToFiles/images/"+filename+"/"+str(t)+".png",frame)
        success, frame=videoCapture.read()
        t+=1
    videoCapture.release()

    #################################################################
    # 讀取影格內含資料，重建原始檔案
    compre=2 # 1bits 占用2*2個 pixel

    folder_path = "C:/ISG/files"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    with open("C:/ISG/files/"+filename, "wb") as file:

        # 讀取圖片
        for num in range(frame_num):

            bits=""
            image1 = "C:/ISG/VideoToFiles/images/"+filename+"/"+str(num)+".png"

            img1 = cv2.imread(image1) # 讀取圖片pixels

            bits_c=0
            # 讀取一幀圖片中有效bits(包括糾錯碼)
            for y in range(0,w,compre):
                for x in range(0,h,compre):
                    if bits_c>229320: #有效bit
                        break

                    sum=0 # 計算2*2 pixel 的平均值
                    for i in range(compre):
                        for j in range(compre):
                            sum=sum+int(img1[x+i, y+j][2])

                    if sum < (128*compre*compre):
                        bits=bits+"0"
                    else:
                        bits=bits+"1"
                    
                    bits_c+=1
        

            # 將包含糾錯碼的bits(4095)，解碼為原始bits(4065)
            if num==(frame_num-1):# 若為最後一幀特別處理
                datas=b''
                ft=int(last_frame_pnum/(4095*8))+1
                last_ft_byte_len=int((int(last_frame_pnum)-(ft-1)*4095*8)/8)
                for i in range(ft):
                    if i==(ft-1):# 最後一個資料單位
                        int_bits=int(bits[i*4095*8:i*4095*8+last_ft_byte_len*8],2)
                        bytes_bits=bytearray(int_bits.to_bytes(length=last_ft_byte_len, byteorder='little'))
                        data, ecc = bytes_bits[:-bch.ecc_bytes], bytes_bits[-bch.ecc_bytes:]
                        bch.decode_inplace(data, ecc)
                        datas=datas+data

                    else:

                        int_bits=int(bits[i*4095*8:i*4095*8+4095*8],2)
                        bytes_bits=bytearray(int_bits.to_bytes(length=4095, byteorder='little'))
                        data, ecc = bytes_bits[:-bch.ecc_bytes], bytes_bits[-bch.ecc_bytes:]
                        bch.decode_inplace(data, ecc)
                        datas=datas+data

            else:
                datas=b''
                for i in range(7):
                    int_bits=int(bits[i*4095*8:i*4095*8+4095*8],2)
                    bytes_bits=bytearray(int_bits.to_bytes(length=4095, byteorder='little'))
                    data, ecc = bytes_bits[:-bch.ecc_bytes], bytes_bits[-bch.ecc_bytes:]
                    bch.decode_inplace(data, ecc)
                    datas=datas+data

            file.write(datas)
    shutil.rmtree("C:/ISG/VideoToFiles/images/"+filename)


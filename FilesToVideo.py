import cv2
import os
import shutil
from PIL import Image
import bchlib
import os


w = 1280  # x
h = 720  # y
frameSize = (w, h)
framerate = 30
# 一幀可寫入1280*720 pixels

# 設定BCH方程式
BCH_POLYNOMIAL = 65533
BCH_BITS = 16
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
# 根據參數，4065bytes 數據之糾錯碼大小為 30bytes




# 創建資料夾，若已存在便刪除後重建
def creatdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
        

# 將檔案寫入圖片
def FTV(filepath):
    
    compre=2 # 1bits 占用2*2個 pixel

    file_name = filepath.split("/")[-1]
    path = "C:/ISG/FilesToVideo/images/"
    if not os.path.exists(path+file_name):
        os.makedirs(path+file_name)
    

    # 以二進製讀入檔案
    with open(filepath, "rb") as f:
        tt = (255, 255, 255)#0
        ff = (0, 0, 0)#1

        t = 0 # 影格數
        status=""
        while True:
            bits=""
            # 一個寫入單位為 4095bytes int((1280*720)/(4095*8*4))=7 可寫入7個單位
            for i in range(7):
                file = f.read(4065)

                if not file: # 檢測資料讀取狀態
                    status="end"
                    break

                ecc = bch.encode(file) # 糾錯碼
                
                file_bytes=file+ecc
                file_int = int.from_bytes(file_bytes, byteorder='little')
                file_bits = bin(file_int)[2:].zfill(len(file_bytes)*8)

                bits = bits+file_bits


                last_frame_pnum=len(bits) # 紀錄最後一幀寫入多少bits
            
            

            # 創建圖片
            image1 = Image.new(mode="RGB", size=(w, h)) # 預設為全黑圖片
            img1=image1.load()
            bn=0
            for x in range(0,w,compre):
                for y in range(0,h,compre):
                    try:
                        k = bits[bn]
                    except:
                        break

                    # 1 bits 以 2*2 pixel block寫入圖片
                    if k == "1":
                        for i in range(compre):
                            for j in range(compre):
                                img1[x+i, y+j] = tt
                    else:
                        for i in range(compre):
                            for j in range(compre):
                                img1[x+i, y+j] = ff
                    bn+=1
            
            image1.save(path+file_name+"/"+str(t)+".png")
            t += 1
            
            
            if status=="end": # 讀取結束
                break
        
        # 若影格數小於幀數，補足至一秒
        if t<framerate:
            k=30-t
            image = Image.new(mode="RGB", size=(w, h)) # 預設為全黑圖片
            for i in range(k):
                image.save(path+file_name+"/"+str(t+i)+".png")


    ###################################################################
    # 將影格轉為影片

    # vedio_name包括: 原始檔案名稱、有效影格數、最後一幀寫入多少bits
    vedio_name = file_name+","+str(t)+","+str(last_frame_pnum)
    
    # 設定編碼器
    out = cv2.VideoWriter('C:/ISG/FilesToVideo/videos/'+vedio_name+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), framerate, frameSize)
    
    if t<framerate:
        k=30
    else:
        k=t
    # k=影格數
    for filenum in range(k):
        img = cv2.imread('C:/ISG/FilesToVideo/images/'+file_name+"/"+str(filenum)+'.png')
        out.write(img)
    out.release()
    shutil.rmtree(path+file_name)
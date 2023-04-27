import numpy as np
import cv2
import glob
import time
import os
import shutil
from PIL import Image


w = 1280  # x
h = 720  # y
frameSize = (w, h)

n="WinMerge-2.16.28-Setup.exe"
file_path = "C:/Users/william/Downloads/"+n

def creatdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
        


def FTP(filepath):
    
    compre=4

    file_name = filepath.split("/")[-1]
    path = "C:/ISG/FilesToVideo/images/"
    creatdir(path+file_name)
    


    with open(filepath, "rb") as f:
        tt = (255, 255, 255)
        ff = (0, 0, 0)
        t = 0

        while True:
            file = f.read(int(115200/compre))
            if not file:
                break
            file_int = int.from_bytes(file, byteorder='little')
            file_bits = bin(file_int)[2:].zfill(len(file)*8)

            if len(file_bits) < 921600:
                last_frame_pnum = len(file_bits)


            print("now is "+str(t)+".png")
            image = Image.new(mode="RGB", size=(w, h))
            img=image.load()
            bn=0
            for x in range(w):
                for y in range(0,h,compre):
                    try:
                        k = file_bits[bn]
                    except:
                        break
                    if k == "1":
                        for i in range(compre):
                            img[x, y+i] = tt
                    # img[x, y+1]=tt
                    # img[x, y+2] = tt
                    # img[x, y+3]=tt
                    # img[x, y+4] = tt
                    # img[x, y+5]=tt
                    # img[x, y+6] = tt
                    # img[x, y+7]=tt
                    else:
                        for i in range(compre):
                            img[x, y+i] = ff
                    # img[x, y+1] = ff
                    # img[x, y+2] = ff
                    # img[x, y+3]=ff
                    # img[x, y+4] = ff
                    # img[x, y+5] = ff
                    # img[x, y+6] = ff
                    # img[x, y+7]=ff
                    bn+=1
            
            image.save(path+file_name+"/"+str(t)+".png")
            t += 1
        
        if t<30:
            k=30-t
            image1 = Image.new(mode="RGB", size=(w, h))
            for i in range(k):
                image1.save(path+file_name+"/"+str(t+i)+".png")
                

        return file_name,last_frame_pnum,t


def PTV(file_name,last_frame_pnum,t):
    vedio_name = file_name+","+str(t)+","+str(last_frame_pnum)
    creatdir('C:/ISG/FilesToVideo/videos/'+file_name)
    out = cv2.VideoWriter('C:/ISG/FilesToVideo/videos/'+file_name+"/"+vedio_name+'.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, frameSize)
    if t<30:
        k=30
    else:
        k=t
    for filenum in range(k):
        print(filenum)
        img = cv2.imread('C:/ISG/FilesToVideo/images/'+file_name+"/"+str(filenum)+'.png')
        out.write(img)
    out.release()
    # shutil.rmtree('C:/ISG/FilesToVideo/images/'+file_name)

file_name,last_frame_pnum,t=FTP(file_path)
PTV(file_name,last_frame_pnum,t)
print("done")

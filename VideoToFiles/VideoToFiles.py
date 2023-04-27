import glob
import cv2
import time
import numpy as np
from PIL import Image
import os
import shutil

h = 720
w = 1280
states=""



filepath="C:/ISG/VideoToFiles/videos/WinMerge 2 16 28 Setup .exe,68,468928.mp4"

try:
    file_name,framenum,lastframepnum=str(filepath.split("/")[-1])[:-4].split(",")
    framenum=int(framenum)
    lastframepnum=int(lastframepnum)
except:
    states="FileError"

def creatdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)

def VTP(Vpath,filename):
    creatdir("C:/ISG/VideoToFiles/images/"+filename)
    videoCapture = cv2.VideoCapture(Vpath)
    success, frame=videoCapture.read()
    t=0
    while success:
        cv2.imwrite("C:/ISG/VideoToFiles/images/"+filename+"/"+str(t)+".png",frame)
        success, frame=videoCapture.read()
        print(t)
        t+=1
    videoCapture.release()



def PTF(filename,frame_num,last_frame_pnum):
    with open("C:/ISG/files/"+filename, "wb") as file:
        for num in range(frame_num):
            bits=""
            images = "C:/ISG/VideoToFiles/images/"+filename+"/"+str(num)+".png"
            print("here is "+str(num)+'.png')
            img = cv2.imread(images)
            for y in range(w):
                for x in range(0,h,1):
                    k=int(img[x, y][2])
                    # +int(img[x+1,y][2])+int(img[x+2,y][2])+int(img[x+3,y][2])+int(img[x+4,y][2])+int(img[x+5,y][2])+int(img[x+6,y][2])+int(img[x+7,y][2])
                    if (k) < 128:
                        bits=bits+"0"
                    else:
                        bits=bits+"1"
        

            if num==(frame_num-1):
                int_bits=int(bits[:last_frame_pnum],2)        
                bytes_bits=int_bits.to_bytes(length=int(last_frame_pnum/8), byteorder='little')
                print(int(last_frame_pnum/8))
            else:
                int_bits=int(bits,2) 
                bytes_bits=int_bits.to_bytes(length=int(len(bits)/8), byteorder='little')
                # print(int(len(bits)/8))
            file.write(bytes_bits)

if states=="FileError":
    print("FileError")
else:
    VTP(filepath,file_name)
    PTF(file_name,framenum,lastframepnum)
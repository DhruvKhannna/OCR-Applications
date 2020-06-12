#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import sys
import pytesseract
import wand
import os
import csv
import shutil
import os, subprocess
from wand.image import Image as wi
import subprocess
import matplotlib.image as mpimg
import numpy as np


path='C:/Python Scripts/OCR/PDF'
try:
    os.mkdir('Converted')
except:
    "Folder Already Exist"
os.chdir('C:/Python Scripts/OCR/PDF')
listing = os.listdir(path)
listing
for listt in listing:
    if listt.endswith('.pdf'):
        path2='C:/Python Scripts/OCR/PDF/Converted'
        os.chdir('C:/Python Scripts/OCR/PDF/Converted')
        i=1
        j=1
        extra_char=["_",""]
        z=0
        try:
            os.mkdir(listt.replace('.pdf',''))
            os.chdir('C:/Python Scripts/OCR/PDF')
            pdf=wi(filename=listt,resolution=600)
            pdf_image=pdf.convert("jpeg")
            #print('check1')
            for img in pdf_image.sequence:
                page=wi(image=img)
                path3 = os.path.join(path2,listt.replace('.pdf',''))
                os.chdir(path3)
                #page.save(filename=str(listt.replace('.pdf',''))+'page'+str(i)+'.jpg')
                page.save(filename=str((chr(i+96)+str(j)+extra_char[z]+'.jpg')))
                #print('check2')
                #print((chr(i+96)+str(j)+'.jpg'))
                j+=1
                if j>=9:
                    i+=1 
                    if i>=25:
                        z=1
                    #print('check3')
                    j=1

        except:
            i+=1
        #------------------second part------------------------
        Total=[]
        Name=[]
        path4='C:/Python Scripts/OCR/PDF/Converted'
        save_path='C:/Python Scripts/OCR/Final'
        config = ('-l eng --oem 1 --psm 3')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Dhruv\AppData\Local\Tesseract-OCR\tesseract.exe'
        path5 = os.path.join(path4,listt.replace('.pdf',''))
        listing3 = os.listdir(path5)    
        #print(listing3)
        Total.append(len(listing3))
        name_of_file = listt.replace('.pdf','')
        Name.append(listt)

        completeName = os.path.join(save_path, name_of_file+".txt")   
        file1 = open(completeName, "w")
        #sort_listing3=listing3.sort()
        for file in listing3:
            try:
                im = cv2.imread(path5+ "\\" + file)
                # Run tesseract OCR on image
                text=pytesseract.image_to_string(im, config=config)
            except:
                im = cv2.imdecode(np.fromfile(path5+ "\\" + file, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                # Run tesseract OCR on image
                text=pytesseract.image_to_string(im, config=config)
            #im=mpimg.imread(path5+ "\\" + file)
            #im = cv2.resize(im, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            #im = cv2.GaussianBlur(im, (5, 5), 0)
            
            
            with open('C:/Python Scripts/Ocr wrong word-Modified.csv','rt')as f:
                data = csv.reader(f)
                for row in data:
                    text=text.replace(row[0],row[1])  
            file1.write(text)
            file1.write('\n\n\n')
            file1.write('-----------------------------Next Page----------------------------------')
            file1.write('\n\n\n')
        file1.close()
        #os.close(path5)
        shutil.move(os.path.join(path,listt),save_path)


        os.chdir(r'C:\Python Scripts\OCR\PDF\Converted')
        remove_items=os.listdir()
        if len(remove_items)>2:
            try:
                shutil.rmtree(os.path.join(path2,remove_items[0]))
            except:
                shutil.rmtree(os.path.join(path2,remove_items[1]))
                
        del_dir2 = r'C:\Python Scripts\OCR\PDF\Converted'
        pObj2 = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir2, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
        rTup2 = pObj2.communicate()
        rCod2 = pObj2.returncode



        del_dir = r'C:\Users\Dhruv\AppData\Local\Temp'
        pObj = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
        rTup = pObj.communicate()
        rCod = pObj.returncode
        if rCod == 0:
            print('Success: Cleaned Windows Temp Folder')
        else:
            print('Fail: Unable to Clean Windows Temp Folder')
print('all file are successfully coverted')


# In[ ]:





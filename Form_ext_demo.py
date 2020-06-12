#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3
from IPython.display import Image, display
from trp import Document
from PIL import Image as PImage, ImageDraw
import time
from IPython.display import IFrame
import pandas as pd


# In[2]:


import cv2
import sys
import pytesseract
import wand
import os
from wand.image import Image as wi


path='D:/Python Scripts/OCR/PDF'
os.chdir('D:/Python Scripts/OCR/PDF')
listing = os.listdir(path)
listing
for listt in listing:
    path2='D:/Python Scripts/OCR/PDF/Converted'
    os.chdir('D:/Python Scripts/OCR/PDF/Converted')
    i=1
    j=1
    extra_char=["_",""]
    z=0
    try:
        os.mkdir(listt.replace('.pdf',''))
        os.chdir('D:/Python Scripts/OCR/PDF')
        pdf=wi(filename=listt,resolution=300)
        pdf_image=pdf.convert("jpeg")
        #print('check1')
        for img in pdf_image.sequence:
            page=wi(image=img)
            path3 = os.path.join(path2,listt.replace('.pdf',''))
            os.chdir(path3)
            #page.save(filename=str(listt.replace('.pdf',''))+'page'+str(i)+'.jpg')
            page.save(filename=str(listt+'.jpg'))
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


# In[41]:


# Document
s3BucketName = "bucker name here"
documentName = "document name in jpg format here"

ACCESS_KEY='access key here'
SECRET_KEY='secret key here'


# In[ ]:



client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
response = client.analyze_document(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    },
    FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

for page in doc.pages:
    # Print fields
    print("Fields:")
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))

    # Get field by key
    print("\nGet Field by Key:")
    key = "Phone Number:"
    field = page.form.getFieldByKey(key)
    if(field):
        print("Key: {}, Value: {}".format(field.key, field.value))

    # Search fields by key
    print("\nSearch Fields:")
    key = "address"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        print("Key: {}, Value: {}".format(field.key, field.value))


# In[2]:


keyz=[]
valuez=[]
df=pd.DataFrame(columns=["X","Y"])


# In[6]:


def PDF2TXT(doc_name):
    s3BucketName = "starboy"
    documentName = doc_name
	ACCESS_KEY='access key here'
	SECRET_KEY='secret key here'

    client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    response = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        },
        FeatureTypes=["FORMS"])

    #print(response)

    doc = Document(response)

    for page in doc.pages:
        # Print fields
        print("Fields:")
        for field in page.form.fields:
            tab=print("Key: {}, Value: {}".format(field.key, field.value))
            #print(field.key)
            ##valuez.append(field.value)
    

        # Get field by key
        print("\nGet Field by Key:")
        key = "Fax, "
        field = page.form.getFieldByKey(key)
        if(field):
            print("Key: {}, Value: {}".format(field.key, field.value))

        # Search fields by key
        print("\nSearch Fields:")
        key = "Excise Regn No."
        fields = page.form.searchFieldsByKey(key)
        for field in fields:
            print("Key: {}, Value: {}".format(field.key, field.value))
    #df.append(pd.DataFrame({"XX":keyz,"XY":valuez}))






#!/usr/bin/env python
# coding: utf-8

# In[2]:


#pip install boto3


# In[14]:


# Detects text in a document stored in an S3 bucket. 
import boto3
import sys
from time import sleep
import math
import pandas as pd


if __name__ == "__main__":

    bucket='bucker name here'
    ACCESS_KEY='access key here'
    SECRET_KEY='secret key here'
    
    client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    
    s3 = boto3.resource('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    your_bucket = s3.Bucket(bucket)

    extracted_data = []
    for s3_file in your_bucket.objects.all():
        print(s3_file)
        
        # use textract to process s3 file
        response = client.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': s3_file.key}})
        
        blocks=response['Blocks']

        for block in blocks:
                if block['BlockType'] != 'PAGE':
                    print('Detected: ' + block['Text'])
                    print('Confidence: ' + "{:.2f}".format(block['Confidence']) + "%")
                    
                    # Example case where you want to extract words with #
                    if("#" in block['Text']):
                        words = block['Text'].split()
                        for word in words:
                               if("#" in word):
                                    extracted_data.append({"word" : word, "file" : s3_file.key, "confidence": "{:.2f}".format(block['Confidence']) + "%"})
        
        # sleep 2 seconds to prevent ProvisionedThroughputExceededException
        sleep(2)

    df = pd.DataFrame(extracted_data)
    df = df.drop_duplicates()
    df.to_csv('output.csv')


# In[15]:


extracted_data


# In[9]:


s3_file.key


# In[10]:





# In[ ]:





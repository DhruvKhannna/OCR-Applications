#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import boto3
import sys
from time import sleep
import math
import pandas as pd

bucket='bucket name here'
ACCESS_KEY='please paste your access key here'
SECRET_KEY='please paste your secret key here'

client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

s3 = boto3.resource('s3',
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)

your_bucket = s3.Bucket(bucket)

extracted_data = []
for s3_file in your_bucket.objects.all():
    print(s3_file.key)
    
def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    })

    return response["JobId"]

def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

def getJobResults(jobId):

    pages = []

    time.sleep(5)

    client = boto3.client('textract',region_name='us-east-1', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    response = client.get_document_text_detection(JobId=jobId)
    
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages


# Document
s3BucketName = "starboy"
documentName = "2nd license renewal & coterm of CIGNA SWIFT.pdf"

jobId = startJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(isJobComplete(jobId)):
    response = getJobResults(jobId)

#print(response)

# Print detected text
os.chdir(r'C:\Users\Dhruv')
fileName='xdxfile.txt'
with open(fileName, 'w') as document:
    for resultPage in response:
        for item in resultPage["Blocks"]:
            
            if item["BlockType"] == "LINE":

                print ('\033[94m' +  item["Text"] + '\033[0m')
                document.write(item["Text"] )
                document.write('\n')

# Detect columns and print lines
columns = []
lines = []
for resultPage in response:
    for item in resultPage["Blocks"]:
          if item["BlockType"] == "LINE":
            column_found=False
            for index, column in enumerate(columns):
                bbox_left = item["Geometry"]["BoundingBox"]["Left"]
                bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
                bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]/2
                column_centre = column['left'] + column['right']/2

                if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                    #Bbox appears inside the column
                    lines.append([index, item["Text"]])
                    column_found=True
                    break
            if not column_found:
                columns.append({'left':item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
                lines.append([len(columns)-1, item["Text"]])

lines.sort(key=lambda x: x[0])
fileName='xdxfile22.txt'
with open(fileName, 'w') as document:
    for line in lines:
        print (line[1])
        document.write(line[1])
        document.write('\n')


#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os,io,re
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
from google.protobuf import json_format
from google.cloud import vision_v1p2beta1

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'Gogle-vision-API.json'

client=vision.ImageAnnotatorClient()
#client = vision_v1p2beta1.ImageAnnotatorClient()
batch_size=1
mime_type='application/pdf'
feature=vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
blob_2=list(bucket.list_blobs())
#pdf='2nd license renewal & coterm of CIGNA SWIFT.pdf'
for blob2 in blob_2:
    pdf=blob2.name
    if pdf.endswith('pdf'):
        print(pdf)
        gcs_source_uri='gs://star_boy/'+pdf


        gcs_source=vision.types.GcsSource(uri=gcs_source_uri)
        input_config=vision.types.InputConfig(gcs_source=gcs_source,mime_type=mime_type)
        gcs_destination_uri='gs://star_boy/results/pdf_result'+pdf+" "
        print(gcs_destination_uri)


        gcs_destination=vision.types.GcsDestination(uri=gcs_destination_uri)
        output_config=vision.types.OutputConfig(gcs_destination=gcs_destination,batch_size=batch_size)

        async_request=vision.types.AsyncAnnotateFileRequest(features=[feature],input_config=input_config,output_config=output_config)
        #operation=client.async_batch_annotation_files(requests=[async_request])
        operation=client.async_batch_annotate_files(requests=[async_request])
        operation.result(timeout=180)


        storage_client=storage.Client()
        match=re.match(r'gs://([^/]+)/(.+)',gcs_destination_uri)
        print(match)
        bucket_name=match.group(1)
        print(bucket_name)
        prefix=match.group(2)
        print(prefix)
        bucket=storage_client.get_bucket(bucket_name)


        #list object with the given prefix
        blob_list=list(bucket.list_blobs(prefix=prefix))


        filenm=pdf+'.txt'
        with open(filenm,'w') as f:

            for blob in blob_list:
                #print(blob.name)
                output=blob
                json_string=output.download_as_string()
                response=json_format.Parse(json_string,vision.types.AnnotateFileResponse())
                first_page_response=response.responses[0]
                annotation=first_page_response.full_text_annotation
                print(u'full text:')
                print(annotation.text)
                f.write(annotation.text)
                f.write('\n')


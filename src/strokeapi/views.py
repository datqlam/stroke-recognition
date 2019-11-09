from django.shortcuts import render
from django.http import (
    HttpResponseBadRequest
)

# Create your views here.
from rest_framework import views
from rest_framework.response import Response

import tensorflow as tf

from keras.models import load_model
from keras.preprocessing import image
import cv2
from numpy import array
import io
from PIL import Image
import json

import base64

from .serializers import StrokeApiSerializer


print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

new_model = load_model('src/lib/models/data.h5', compile=False)

def isBase64(sb):
    try:
        if isinstance(sb, str):
        # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


class StrokeApiView(views.APIView):
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    def get(self, request):
        
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        req = self.request
        print(req.query_params.get('query'))
        print(request)
        
        
        strokeApiResponseData = [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        results = StrokeApiSerializer(strokeApiResponseData, many=True).data
        return Response(results)

class PredictSentimentApiView(views.APIView):
    print("iiiiiiiiiiiiiiiiiiiiiiiii")
    
    global graph
    graph = tf.get_default_graph()
    
    
    
    
    def get(self, request):
        
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        req = self.request
        
        if request.META.get('CONTENT_TYPE', '').lower() == 'application/json' and len(request.body) > 0:
            try:
                body_data = json.loads(request.body)
            except Exception as e:
                return HttpResponseBadRequest(json.dumps({'error': 'Invalid request: {0}'.format(str(e))}), content_type="application/json")
        else:
            return HttpResponseBadRequest(json.dumps({'error': 'Invalid content type: shoud be application/json or body data is empty'}), content_type="application/json")
        
        
        img_base64 = body_data["data"]
        
        if not isBase64(img_base64):
            return HttpResponseBadRequest(json.dumps({'error': 'Image should be base64 encoded'}), content_type="application/json")
        
        
        
#         img_path = 'src/lib/data/images - 2019-08-23T131005.363.jpg'
        
#         with open('src/lib/data/images - 2019-08-23T131005.363.jpg','rb') as img_file:
#             my_string = base64.b64encode(img_file.read())
#             utf8_string = my_string.decode('utf-8')
            
#             print(utf8_string)
        
#         with open('src/lib/data/outimage.jpg', 'wb') as fh:
#             fh.write(base64.b64decode(utf8_string))
        
        buf = io.BytesIO(base64.b64decode(img_base64))
        img = Image.open(buf)
        
        img_cvt = cv2.cvtColor(array(img), cv2.COLOR_BGR2GRAY)
        img_cvt = cv2.resize(img_cvt,(50,50))
        img_cvt = img_cvt.reshape((1, 50 * 50))
        img_cvt = img_cvt.astype('float32') / 255
               
        with graph.as_default():
            preds = new_model.predict(img_cvt)
        
#         print(*preds, sep = ", ") 
        
        results = {'prediction': preds}
        return Response(results)
    

    

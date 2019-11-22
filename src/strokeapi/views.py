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
import json

from strokeapi import util

new_model = load_model('src/lib/models/data.h5', compile=False)

class PredictApiView(views.APIView):
    
    global graph
    graph = tf.get_default_graph()
    
    def post(self, request):
        
        req = self.request
        
        if request.META.get('CONTENT_TYPE', '').lower() == 'application/json' and len(request.body) > 0:
            try:
                body_data = json.loads(request.body)
            except Exception as e:
                return HttpResponseBadRequest(json.dumps({'error': 'Invalid request: {0}'.format(str(e))}), content_type="application/json")
        else:
            return HttpResponseBadRequest(json.dumps({'error': 'Invalid content type: shoud be application/json or body data is empty'}), content_type="application/json")
        
        img_base64 = body_data["data"]
       
        if not util.isBase64(img_base64):
            return HttpResponseBadRequest(json.dumps({'error': 'Image should be base64 encoded'}), content_type="application/json")
        
        img_cvt = util.preProcessImageData(img_base64);
               
        with graph.as_default():
            preds = new_model.predict(img_cvt)
        
        results = {'prediction': preds}
        return Response(results)

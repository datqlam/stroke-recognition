from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.response import Response

from .serializers import StrokeApiSerializer

import pickle
import numpy as np
from strokeapi.models import NLPModel

print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

model = NLPModel()

clf_path = 'src/lib/models/SentimentClassifier.pkl'
with open(clf_path, 'rb') as f:
    model.clf = pickle.load(f)
    
vec_path = 'src/lib/models/TFIDFVectorizer.pkl'
with open(vec_path, 'rb') as f:
    model.vectorizer = pickle.load(f)




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
    def get(self, request):
        
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        req = self.request
        user_query = req.query_params.get('query')
        print(req.query_params.get('query'))
        print(request)
        
        # vectorize the user's query and make a prediction
        uq_vectorized = model.vectorizer_transform(np.array([user_query]))
        prediction = model.predict(uq_vectorized)
        pred_proba = model.predict_proba(uq_vectorized)
        
        # Output either 'Negative' or 'Positive' along with the score
        if prediction == 0:
            pred_text = 'Negative'
        else:
            pred_text = 'Positive'

        # round the predict proba value and set to new variable
        confidence = round(pred_proba[0], 3)
        
        strokeApiResponseData = [{"likes": pred_text, "comments": confidence}]
        results = {'prediction': pred_text, 'confidence': confidence}
        return Response(results)
    

    

from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.response import Response

from .serializers import StrokeApiSerializer

class StrokeApiView(views.APIView):

    def get(self, request):
        strokeApiResponseData = [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        results = StrokeApiSerializer(strokeApiResponseData, many=True).data
        return Response(results)
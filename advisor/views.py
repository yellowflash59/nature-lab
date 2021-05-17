from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from rest_framework.response import Response
from django.shortcuts import redirect,get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
import requests
import json
# Create your views here.

@api_view(['Get'])
def advisor_list(request):
    product = Advisor.objects.all()

    if request.method == "GET":
        serializer = AdvisorSerializer(product,many = True)
        return Response(serializer.data)

@api_view(['POST'])
def advisor_create(request):
    if request.method == 'POST':
        serializer = AdvisorSerializer(data = request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
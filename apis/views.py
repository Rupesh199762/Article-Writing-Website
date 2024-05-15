from django.shortcuts import render
from .serializers import ArticleSerializer
from rest_framework import viewsets
from authentication.models import ACModel

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ACModel.objects.all()
    serializer_class = ArticleSerializer
# Create your views here.

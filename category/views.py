from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def category_page(request):
    return HttpResponse('Category page')
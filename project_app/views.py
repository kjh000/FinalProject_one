from django.shortcuts import render

# Create your views here.

def mainFunc(request):
    return render(request,'main.html')

def findFunc(request):
    return render(request,'finder.html')
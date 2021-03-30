from django.http import HttpResponse
from django.shortcuts import render 

def dashboard (request):
    return render(request,'dashboard.html')

def rating (request):
    return render(request,'rating.html')

def registerMember (request):
    return render(request,'registerMember.html')

def registerMusicStore (request):
    return render(request,'registerMusicStore.html')

def profile (request):
    return render(request,'profile.html')

def profileMusicStore (request):
    return render(request,'profileMusicStore.html')

def scoreRating (request):
    return render(request,'scoreRating.html')

def productList (request):
    return render(request,'productList.html')

def userApproveList (request):
    return render(request,'userApproveList.html')    
    
    
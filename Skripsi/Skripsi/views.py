from django.http import HttpResponse
from django.shortcuts import render 
from register.models import user
from django.contrib import messages
import datetime

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

def token (request):
    return render(request,'token-send.html')  

def verifyEmail (request, auth_token):
    webRender = ''
    try:
        profile_obj = user.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if (profile_obj.roleId == 'Reg_User'):
                profile_obj.status = 'Verified'
                webRender = 'verified.html'
            else :
                profile_obj.status = 'AdminPending'
                webRender = 'verifiedMusicStore.html'
                
            profile_obj.verified_at = datetime.date.today()
            profile_obj.save()
            # messages.success(request, 'Your Account Has Been Verified')
        else:
            return render(request,'verifiedError.html')
    except Exception as e:
        print (e)   

    return render(request,webRender)


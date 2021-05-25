from django.http import HttpResponse
from django.shortcuts import render, redirect 
from register.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from .forms import LoginForm
from product.models import *

def dashboard (request):
    isLogin = request.POST.get('isLogin')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    

    #hot item
    hotItems = Product.objects.select_related('brandId').order_by('-visitCount')[:8]
    newReleaseAcoustic = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Acoustic")[:6]
    newReleaseElectric = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Electric")[:6]
    newReleasePercussion = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Percussion")[:6]
    newReleaseKeys = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Keys & Midi")[:6]
    newReleaseRecordingKit = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Recording Kit")[:6]
    newReleaseSoundSystem = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Sound System")[:6]
    newReleaseAccessories = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="Accessories")[:6]
    newReleaseDAW = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName="DAW & Plugins")[:6]

    context = {
        'hotItems': hotItems,
        'newReleaseAcoustic': newReleaseAcoustic,
        'newReleaseElectric': newReleaseElectric,
        'newReleasePercussion': newReleasePercussion,
        'newReleaseKeys': newReleaseKeys,
        'newReleaseRecordingKit': newReleaseRecordingKit,
        'newReleaseSoundSystem': newReleaseSoundSystem,
        'newReleaseAccessories': newReleaseAccessories,
        'newReleaseDAW': newReleaseDAW,
    }
    return render(request,'dashboard.html', context)

def user_logout (request):
    logout (request)
    return redirect ('dashboard')

def profile (request):
    return render(request,'profile.html')

def profileMusicStore (request):
    return render(request,'profileMusicStore.html')


def productList (request):
    isLogin = request.POST.get('isLogin')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)

    return render(request,'productList.html')   

def token (request):
    return render(request,'token-send.html')  

def verifyEmail (request, auth_token):
    webRender = ''
    try:
        profile_obj = User.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if (profile_obj.roleId == 'Reg_User'):
                profile_obj.status = 'Verified'
                webRender = 'verified.html'
            else :
                profile_obj.status = 'AdminPending'
                webRender = 'verifiedMusicStore.html'
                
            profile_obj.verified_at = datetime.date.today()
            profile_obj.save()
        else:
            return render(request,'error.html')
    except Exception as e:
        print (e)   

    return render(request,webRender)
    
def loginAccount (request):
        email = request.POST.get('userEmail')
        password = request.POST.get('userPassword')

        username = User.objects.filter(email = email).values_list(
            'userName', flat=True
            ).first()

        user_data = User.objects.filter(userName = username).values() # buat nembak 1 data

            # test = user_data.values_list('userName', flat=True).first() -------->buat ngambil salah satu data di user_data 

        user = authenticate(request, username = username, password=password)
        
        if user is not None:
            
            if user_data.values_list('status', flat=True).first() == 'Pending':
               messages.error(request, 'please verify your account first')
               return redirect ('dashboard')
            
            elif user_data.values_list('status', flat=True).first() == 'AdminPending':
               messages.error(request, 'Please wait for admin to approve your account')
               return redirect ('dashboard')

            else:
               login (request,user)
               return redirect ('dashboard') 

        else:
            messages.error(request, 'We cannot find an account with that email address')

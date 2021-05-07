from django.http import HttpResponse
from django.shortcuts import render, redirect 
from register.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from .forms import LoginForm

def dashboard (request):
    web = 'dashboard.html'
    
    login_form = LoginForm()
    context = {
        'form': login_form
    }
    
    if request.method != 'POST':
        return render(request,'dashboard.html', context)
    else: 
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
               messages.success(request, 'please verify your account first')
            else:
               login (request,user)
               return redirect ('dashboard') 

        else:
            messages.success(request, 'email is Taken')
            


    return render(request,web,context)
    
def user_logout (request):
    logout (request)
    return redirect ('dashboard')

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
    


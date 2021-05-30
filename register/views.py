from django.shortcuts import redirect, render
from django.contrib import messages
from register.models import User, MusicStoreData
from datetime import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator
from .forms import UserForm, MusicStoreForm, RejectionReason
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import allowed_users
from Skripsi.views import countUserPending, sendMailAfterRegis, weakPassword


def registerMember (request):
    if request.method != 'POST':
        regis_form = UserForm()
        context = {
            'form': regis_form
        }
        return render(request,'registerMember.html', context)
    else :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('confirm_pass')

        web_direct = ''

        try: 
            if User.objects.filter(userName = username).first():
                messages.success(request, 'Username is Taken')
                return redirect ('regularUser')

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('regularUser')
            
            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('regularUser')

            if (conf_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('regularUser')

            token = str (uuid.uuid4())
            
            profile_obj = User.objects.create(
                userName = username,
                email = email, 
                password = make_password(password),
                roleId = 'Reg_User',
                description = '',
                status = 'Pending',
                dtm_crt = datetime.now(),
                verified_at = None,
                auth_token = token
            )

            profile_obj.save()

            regisUserAuth(profile_obj)

            domain = get_current_site(request).domain

            sendMailAfterRegis (domain, profile_obj ,'verification', '')
            web_direct = 'token-send.html'
            return render(request,'token-send.html') 

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)

def registerMusicStore (request):
    if request.method != 'POST':
        regis_form = MusicStoreForm()
        context = {
            'form': regis_form
        }
        return render(request,'registerMusicStore.html', context)
    else:
        musicStoreName = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('confirm_pass')
        msPicture = request.FILES['musicStorePicture']
        msPicture.name = musicStoreName+'.jpg'
        msPicture2 = request.FILES['musicStorePicture2']
        msPicture2.name = musicStoreName+'2.jpg'
        msPicture3 = request.FILES['musicStorePicture3']
        msPicture3.name = musicStoreName+'3.jpg'
        description = request.POST.get('description')

        web_direct = ''

        try: 
            if User.objects.filter(userName = musicStoreName).first():
                messages.success(request, 'Music Store Name is Taken')
                return redirect ('musicStore')

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('musicStore')

            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('musicStore')

            if (conf_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('musicStore')

            token = str (uuid.uuid4())

            profile_obj = User.objects.create(
                userName = musicStoreName,
                email = email, 
                password = make_password(password),
                roleId = 'Mus_Store',
                description = description,
                status = 'Pending',
                dtm_crt = datetime.now(),
                verified_at = None,
                auth_token = token
            )

            profile_obj.save()
            
            mStore_obj = MusicStoreData.objects.create(
                userID = profile_obj,
                address = address,
                musicStorePicture = msPicture,
                musicStorePicture2 = msPicture2,
                musicStorePicture3 = msPicture3,
            ) 
            mStore_obj.save()

            regisUserAuth(profile_obj)



            domain = get_current_site(request).domain

            sendMailAfterRegis (domain, profile_obj, 'verification', '')
            web_direct = 'token-send.html'

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)

def regisUserAuth(userRegis):

    userAuth = auth_user.objects.create(
        username = userRegis.userName,
        email = userRegis.email,
        password = userRegis.password  
    )

    userAuth.save()

    getgroupId = Group.objects.get(name = userRegis.roleId)

    userAuth.groups.add(getgroupId)

@login_required
@allowed_users(allowed_roles=['Admin'])
def musicStorePendingList (request):

    qux = MusicStoreData.objects.select_related('userID').filter(userID__status="AdminPending", userID__verified_at__isnull= False)[:8]

    context = {
        'obj': qux,
        'userPending': countUserPending(request)
    }
    return render(request,'userApproveList.html', context)    

@login_required
@allowed_users(allowed_roles=['Admin'])
def musicStoreApproval (request,auth_token):

    qux = MusicStoreData.objects.select_related('userID').get(userID__auth_token=auth_token)

    context = {
        'obj': qux,
        'userPending': countUserPending(request)
    }
    return render(request,'musicStoreApproval.html', context)    

@login_required
@allowed_users(allowed_roles=['Admin'])
def approve (request,auth_token):
    webRender = ''
    try:
        profile_obj = User.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.status = 'Verified'
            profile_obj.save()

            domain = get_current_site(request).domain
            sendMailAfterRegis (domain, profile_obj, 'admin_approve','')

            webRender = 'success.html'
        else:
            return render(request,'error.html')
    except Exception as e:
        print (e)   

    return render(request,webRender)

@login_required
@allowed_users(allowed_roles=['Admin'])
def reject (request,auth_token):
    webRender=''
    if request.method != 'POST':
        rejectionForm = RejectionReason()
        context = {
            'form': rejectionForm,
            'userPending': countUserPending(request)

        }
        return render(request,'rejectionReason.html', context)
    else :
        rejectionReason = request.POST.get('reason')
        try:
            profile_obj = User.objects.filter(auth_token = auth_token).first()
            if profile_obj:
                
                domain = get_current_site(request).domain
                sendMailAfterRegis (domain, profile_obj, 'admin_reject',rejectionReason)

                userAuth = auth_user.objects.get(username = profile_obj.userName)
                userAuth.groups.clear()
                userAuth.delete()

                profile_obj.delete()

                webRender = 'success.html'
            else:
                return render(request,'error.html')
        except Exception as e:
            print (e) 
        
    return render(request,webRender)
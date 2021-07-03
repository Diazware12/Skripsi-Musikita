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
from Skripsi.views import checkChar, countReport, countUserPending, sendMail, weakPassword, make_square
from PIL import Image
import os
from django.core.paginator import Paginator
import imghdr

def registerMember (request):
    if request.method != 'POST':
        regis_form = UserForm()
        context = {
            'form': regis_form,
            'role': 'Member'
        }
        return render(request,'registerMember.html', context)
    else :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('confirm_pass')

        web_direct = ''

        try: 
            if username == '':
                raise Exception("required field Empty")
            if email == '':
                raise Exception("required field Empty")
            if password == '':
                raise Exception("required field Empty")
            if conf_pass == '':
                raise Exception("required field Empty")

            if len(username) > 20:
                messages.success(request, 'User Name has to be less than or equal 20 characters')
                return redirect ('regularUser')

            if len(email) > 60:
                messages.success(request, 'Email has to be less than or equal 60 characters')
                return redirect ('regularUser')

            if len(password) > 60:
                messages.success(request, 'Password too long')
                return redirect ('regularUser')

            if checkChar (username) == False:
                messages.success(request, 'Name cannot contain / , # , and ?')
                return redirect ('regularUser')

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

            sendMail (domain, profile_obj ,'verification', '')
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
        contact = request.POST.get('contact')
        msPicture = request.FILES['musicStorePicture']
        msPicture.name = musicStoreName+'.jpg'
        msPicture2 = request.FILES['musicStorePicture2']
        msPicture2.name = musicStoreName+'2.jpg'
        msPicture3 = request.FILES['musicStorePicture3']
        msPicture3.name = musicStoreName+'3.jpg'
        description = request.POST.get('description')

        web_direct = ''

        try: 

            if musicStoreName == '':
                raise Exception("required field Empty")
            if address == '':
                raise Exception("required field Empty")
            if email == '':
                raise Exception("required field Empty")
            if password == '':
                raise Exception("required field Empty")
            if conf_pass == '':
                raise Exception("required field Empty")
            if contact == '':
                raise Exception("required field Empty")
            if msPicture == '' or msPicture == None:
                raise Exception("required field Empty")
            if msPicture2 == '' or msPicture2 == None:
                raise Exception("required field Empty")
            if msPicture3 == '' or msPicture3 == None:
                raise Exception("required field Empty")
            if description == '':
                raise Exception("required field Empty")

            if checkChar (musicStoreName) == False:
                messages.success(request, 'Name cannot contain / , # , and ?')
                return redirect ('musicStore')

            if len(musicStoreName) > 20:
                messages.success(request, 'Music Store Name has tobe less than or equal 20 characters')
                return redirect ('musicStore')

            if len(email) > 60:
                messages.success(request, 'Email has to be less than or equal 60 characters')
                return redirect ('musicStore')

            if len(password) > 60:
                messages.success(request, 'Password too long')
                return redirect ('musicStore')  

            if len(contact) > 16:
                messages.success(request, 'contact too long')
                return redirect ('musicStore')    

            if imageDetector(msPicture) == False or imageDetector(msPicture2) == False or imageDetector(msPicture3) == False:
                messages.success(request, 'Image Format must be jpeg or png')
                return redirect ('musicStore')    

            if not contact.isdigit():
                messages.success(request, 'contact must be numeric')
                return redirect ('musicStore')  

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
                contact = contact
            ) 
            mStore_obj.save()

            img1 = Image.open(mStore_obj.musicStorePicture.path)
            img1 = make_square(img1)
            img1.save(mStore_obj.musicStorePicture.path)

            img2 = Image.open(mStore_obj.musicStorePicture2.path)
            img2 = make_square(img2)
            img2.save(mStore_obj.musicStorePicture2.path)

            img3 = Image.open(mStore_obj.musicStorePicture3.path)
            img3 = make_square(img3)
            img3.save(mStore_obj.musicStorePicture3.path)

            regisUserAuth(profile_obj)

            domain = get_current_site(request).domain

            sendMail(domain, profile_obj, 'verification', '')
            web_direct = 'token-send.html'

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)

def registerAdmin (request,code):
    if code != "@dm!n$$%":
        return HttpResponse('You are not allowed to view this page')
    if request.method != 'POST':
        regis_form = UserForm()
        context = {
            'form': regis_form,
            'role': 'Admin'
        }
        return render(request,'registerMember.html', context)
    else :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('confirm_pass')

        web_direct = ''

        try: 
            if username == '':
                raise Exception("required field Empty")
            if email == '':
                raise Exception("required field Empty")
            if password == '':
                raise Exception("required field Empty")
            if conf_pass == '':
                raise Exception("required field Empty")

            if User.objects.filter(userName = username).first():
                messages.success(request, 'Username is Taken')
                return redirect ('registerAdmin')

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('registerAdmin')
            
            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('registerAdmin')

            if (conf_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('registerAdmin')

            token = str (uuid.uuid4())

            profile_obj = User.objects.create(
                userName = username,
                email = email, 
                password = make_password(password),
                roleId = 'Admin',
                description = '',
                status = 'Verified',
                dtm_crt = datetime.now(),
                verified_at = datetime.now(),
                auth_token = token
            )

            profile_obj.save()

            regisUserAuth(profile_obj)

            return redirect('dashboard') 

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

def imageDetector(image):

    format = False
    name = imghdr.what(image)
    if imghdr.what(image) == 'jpeg':
        format = True
    elif imghdr.what(image) == 'jpg':
        format = True
    elif imghdr.what(image) == 'png':
        format = True


    return format

@login_required
@allowed_users(allowed_roles=['Admin'])
def musicStorePendingList (request):

    pendingList = MusicStoreData.objects.select_related('userID').filter(userID__status="AdminPending", userID__verified_at__isnull= False)[:8]

    if pendingList:
        paginator = Paginator(pendingList,8)
        page_number = request.GET.get('page', 1)
        getReviewListByPage = paginator.get_page(page_number)

        if getReviewListByPage.has_next():
            next_url = f'?page={getReviewListByPage.next_page_number()}'
        else:
            next_url = ''

        if getReviewListByPage.has_previous():
            prev_url = f'?page={getReviewListByPage.previous_page_number()}'
        else:
            prev_url = ''
    else:
        getReviewListByPage = pendingList.none()
        next_url = ''
        prev_url = ''

    context = {
        'obj': getReviewListByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }
    return render(request,'userApproveList.html', context)    

@login_required
@allowed_users(allowed_roles=['Admin'])
def musicStoreApproval (request,auth_token):

    qux = MusicStoreData.objects.select_related('userID').get(userID__auth_token=auth_token)

    context = {
        'obj': qux,
        'userPending': countUserPending(request),
        'reportUser': countReport(request)
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
            sendMail (domain, profile_obj, 'admin_approve','')

            webRender = 'success.html'
        else:
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)
    except Exception as e:
        print (e)   

    return render(request,webRender)

@login_required
@allowed_users(allowed_roles=['Admin'])
def reject (request,auth_token,context):
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

                musicStore = MusicStoreData.objects.select_related('userID').get(userID__userName = profile_obj.userName)
                if os.path.exists(musicStore.musicStorePicture.name) and os.path.exists(musicStore.musicStorePicture2.name) and os.path.exists(musicStore.musicStorePicture3.name):
                    os.remove(musicStore.musicStorePicture.name)
                    os.remove(musicStore.musicStorePicture2.name)
                    os.remove(musicStore.musicStorePicture3.name)
                else:
                    pass


                domain = get_current_site(request).domain
                sendMail (domain, profile_obj, 'admin_reject',rejectionReason)

                userAuth = auth_user.objects.get(username = profile_obj.userName)
                userAuth.groups.clear()
                userAuth.delete()

                profile_obj.delete()

                webRender = 'success.html'
            else:
                context = {
                    'message': 'error'
                }
                return render(request,'error.html', context)
        except Exception as e:
            print (e) 
        
    return render(request,webRender)
import uuid
from carousel.models import CarouselImage
from django.db.models.fields import DecimalField
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from register.models import User,MusicStoreData
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import  EmailMessage
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.sites.shortcuts import get_current_site
from product.models import *
from review.models import Report
from .forms import ForgotPasswordForm
from django.db.models import Count
import re
from PIL import Image

def dashboard (request):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)
    
    #carousel
    carousels = CarouselImage.objects.filter(status=True)

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
        'carousels':carousels,
        'hotItems': hotItems,
        'newReleaseAcoustic': newReleaseAcoustic,
        'newReleaseElectric': newReleaseElectric,
        'newReleasePercussion': newReleasePercussion,
        'newReleaseKeys': newReleaseKeys,
        'newReleaseRecordingKit': newReleaseRecordingKit,
        'newReleaseSoundSystem': newReleaseSoundSystem,
        'newReleaseAccessories': newReleaseAccessories,
        'newReleaseDAW': newReleaseDAW,
        'userPending': countUserPending(request),
        'reportUser': countReport(request)
    }
    return render(request,'dashboard.html', context)

def user_logout (request):
    logout (request)
    return redirect ('dashboard')

def productList (request):
    return render(request,'productList.html')  

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
                
            profile_obj.verified_at = datetime.now()
            profile_obj.save()
        else:
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)
    except Exception as e:
        print (e)   

    return render(request,webRender)

def loginAccount (request):
        email = request.POST.get('userEmail')
        password = request.POST.get('userPassword')

        username = auth_user.objects.filter(email = email).values_list(
            'username', flat=True
            ).first()

            # test = user_data.values_list('userName', flat=True).first() -------->buat ngambil salah satu data di user_data 

        user = authenticate(request, username = username, password=password)
        
        if user is not None:

            checkUser = auth_user.objects.get(username = username)

            if checkUser.groups.filter(name='Brand').exists():
                getBrand = Brand.objects.get (brandName = username)
                if getBrand.status != 'Verified':
                    messages.error(request, 'you need to register your account brand first')
                    return redirect ('dashboard')

                else:
                    login (request,user)
                    return redirect ('dashboard') 
            else:
                user_data = User.objects.filter(userName = username).values() # buat nembak 1 data
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
            messages.error(request, 'We cannot find an account with that email address or that password')

def sendMailAfterRegis (domain, user, context, additional_msg):
    subject = ''
    messages = ''
    
    nameList = None
    nameReceipent = []
    
    if (context == 'verification'):
        subject = 'Your Account Need To Be Verified'
        activate_url = 'http://' + domain + '/verify/' + user.auth_token
        messages = 'hi ' + user.userName + ' please verify this account\n' + activate_url
    elif (context == 'admin_approve'):
        subject = 'Your Account Has Been Verified by Admin'
        messages = 'hi ' + user.userName + ',\n\n' + 'Your Music Store\'s account has been verified by admin.\n' + 'Now you can login using your account\n' + 'http://' + domain 
    elif (context == 'admin_reject'):   
        subject = 'Your Account Has Been Rejected by Admin'               
        messages = 'hi ' + user.userName + ',\n\n' + 'Unfortunately Your Music Store\'s account has been Rejected by admin because:\n\n' + additional_msg + '\n\nPlease make a new music store\'s account based on the admin\'s note\n' +'http://' + domain
    elif (context == 'admin_delete'):   
        subject = 'Your Account Has Been Deleted by Admin'               
        messages = 'hi ' + user.userName + ',\n\n' + 'Unfortunately Your account has been Deleted by admin because:\n\n' + additional_msg + '\n\nPlease make a new music store\'s account based on the admin\'s note\n' +'http://' + domain
    elif (context == 'forgot_password'):  
        subject = 'Reset Your Password' 
        activate_url = 'http://' + domain + '/forgot_Pass/' + user.auth_token              
        messages = 'hi ' + user.userName + ',\n\n' + 'Please click the link down below to reset your password\n\n' + activate_url
    elif (context == 'approve_report'):
        subject = 'Your Review has been reported'              
        messages = additional_msg
    elif (context == 'reject_report'):
        nameList = user
        subject = 'Your Report has been rejected by admin'              
        messages = additional_msg
    elif (context == 'brand_invitation'):
        register_url = 'http://' + domain + '/brand/registerBrand/' + user[1]
        subject = 'You invited to Our Community'
        nameReceipent.append(user[0])
        messages = additional_msg +"\n\n"+register_url


    email_from = settings.EMAIL_HOST_USER
    if nameReceipent:
        receipent_list = nameReceipent
    elif nameList == None:
        receipent_list = [user.email]
    else:
        receipent_list = nameList
    email = EmailMessage(
        subject,
        messages,
        email_from,
        receipent_list
    )

    email.send(fail_silently=False)
    # number = 1

def forgotPassword (request):
    email = request.POST.get('userEmail')

    username = User.objects.filter(email = email).values_list(
        'userName', flat=True
        ).first()

    if username is None:
        messages.error(request, 'We cannot find an account with that email address or that password')
    else:
        user = User.objects.get(userName = username)
        domain = get_current_site(request).domain
        sendMailAfterRegis(domain, user, 'forgot_password', '')
        messages.error(request, 'We already send you email to reset your password')

def forgotPasswordForm (request,auth_token):
    getUser = User.objects.get(auth_token = auth_token)
    if request.method != 'POST':
        forgot_pass_form = ForgotPasswordForm()
        context = {
            'form': forgot_pass_form,
            'username': getUser.userName
        }
        return render(request,'forgotPassword.html', context)
    else :
        password = request.POST.get('userPassword')
        conf_pass = request.POST.get('confUserPassword')

        web_direct = 'success.html'

        try: 
            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('regularUser')

            if (conf_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('regularUser')

            getUser.password = make_password(password)
            getUser.save()

            userAuth = auth_user.objects.get(username = getUser.userName)
            userAuth.password = make_password(password)
            userAuth.save()

            return redirect ('dashboard')

        except Exception as e:
            print(e)
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)

    return render(request,web_direct)

def countUserPending(request):
    obj = MusicStoreData.objects.select_related('userID').filter(
            userID__status='AdminPending',
            userID__roleId='Mus_Store').count()
    return obj

def countReport(request):
    obj = Report.objects.values(
          'reviewId').annotate(dcount=Count('reviewId'
          )).order_by().count()

    return obj

def weakPassword (password):
    if (password == "\n" or password == " "):
        return "Password cannot be a newline or space!"
    
    if (9 <= len(password) <= 20):
        if re.search(r'(.)\1\1',password): 
            return "Weak Password: Same character repeats three or more times in a row"
        
        if re.search(r'(..)(.*?)\1', password):
            return "Weak password: Same string pattern repetition"
   
        else:
            return "True"
    else:
        return "Password length must be 9-20 characters!"

def numIndicator (number):

    finalNum = None
    try:
        if number != None or number != '':
            if isinstance(number, int):
                finalNum = number
            elif isinstance(number, float):
                finalNum = number
            else:
                num_array = number.split ('.')
                if num_array[1] == "0" or num_array[1] == "00":
                    finalNum = int(num_array[0])
                else: 
                    finalNum = float(number)
        else:
            finalNum = None
        
        return finalNum
        
    except Exception as e:
        finalNum = None

        return finalNum

def make_square(img):
    fill_color=(255, 255, 255)

    img.load() 

    x, y = img.size
    size = max(x,y)
    new_img = Image.new('RGB', (size, size), fill_color)
    if img.mode == 'RGBA':
        new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)), mask=img.split()[3])
    else :
        new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)))
    return new_img
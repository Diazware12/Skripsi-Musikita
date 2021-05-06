from django.shortcuts import redirect, render
from django.contrib import messages
from register.models import User, MusicStoreData
import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.core.mail import  EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator
import re
from .forms import UserForm, MusicStoreForm

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
                dtm_crt = datetime.date.today(),
                verified_at = None,
                auth_token = token
            )

            profile_obj.save()

            domain = get_current_site(request).domain

            sendMailAfterRegis (domain, profile_obj)
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
        msPicture = request.POST.get('musicStorePicture')
        description = request.POST.get('description')

        web_direct = ''

        try: 
            if User.objects.filter(userName = musicStoreName).first():
                messages.success(request, 'Music Store Name is Taken')
                return redirect ('musicStore/')

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('musicStore/')

            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('regularUser')

            if (conf_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('regularUser')

            token = str (uuid.uuid4())

            profile_obj = User.objects.create(
                userName = musicStoreName,
                email = email, 
                password = make_password(password),
                roleId = 'Mus_Store',
                description = description,
                status = 'Pending',
                dtm_crt = datetime.date.today(),
                verified_at = None,
                auth_token = token
            )

            profile_obj.save()

            msId = profile_obj.userID

            
            mStore_obj = MusicStoreData.objects.create(
                userID = msId,
                address = address,
                musicStorePicture = msPicture
            ) 
            mStore_obj.save()

            domain = get_current_site(request).domain

            sendMailAfterRegis (domain, profile_obj)
            web_direct = 'token-send.html'

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)


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

def sendMailAfterRegis (domain, user):
    subject = 'Your Account Need To Be Verified'
    # message = 'test body'

    activate_url = 'http://' + domain + '/verify/' + user.auth_token
    messages = 'hi ' + user.userName + ' please verify this account\n' + activate_url

    email_from = settings.EMAIL_HOST_USER
    receipent_list = [user.email]
    email = EmailMessage(
        subject,
        messages,
        email_from,
        receipent_list
    )

    email.send(fail_silently=False)
    # number = 1
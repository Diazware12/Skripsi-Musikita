from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from register.models import user, MusicStoreData
import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.core.mail import  EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator


def registerMember (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            if user.objects.filter(userName = username).first():
                messages.success(request, 'Username is Taken')
                return redirect ('regularUser/')

            if user.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('regularUser/')

            token = str (uuid.uuid4())

            profile_obj = user.objects.create(
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
            return render(request,'token-send.html') 

        except Exception as e:
            print(e)

    return render(request,'registerMember.html')

def registerMusicStore (request):
    if request.method == 'POST':
        musicStoreName = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        msPicture = request.POST.get('musicStorePicture')
        description = request.POST.get('description')

        try: 
            if user.objects.filter(userName = musicStoreName).first():
                messages.success(request, 'Music Store Name is Taken')
                return redirect ('musicStore/')

            if user.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('musicStore/')

            token = str (uuid.uuid4())

            profile_obj = user.objects.create(
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
            return render(request,'token-send.html') 

        except Exception as e:
            print(e)


    return render(request,'registerMusicStore.html')





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
    number = 1

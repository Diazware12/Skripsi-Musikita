from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from register.models import user
import datetime
from django.contrib.auth.hashers import make_password, check_password
import uuid

def registerRegUser (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is Taken')
                return redirect ('regularUser/')

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('regularUser/')

            usr_obj = User.objects.create(username = username, email = email)
            usr_obj.set_password(password)

            profile_obj = user.objects.create(
                userName = username,
                email = email, 
                password = make_password(password),
                roleId = 'Reg_User',
                description = '',
                status = 'Pending',
                dtm_crt = datetime.date.today(),
                verified_at = None,
                auth_token = str (uuid.uuid4)
            )
            profile_obj.save()
            return redirect ('success/')

        except Exception as e:
            print(e)
from django.http import HttpResponse
from django.shortcuts import redirect,render
from register.models import User
from django.contrib import messages
from review.models import Review
from django.db import connection
from Skripsi.views import loginAccount, countUserPending, forgotPassword, numIndicator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User as auth_user
from Skripsi.decorator import allowed_users
import os
from django.core.paginator import Paginator

# Create your views here.
def profilePage(request,userName):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    try:   
        getUser = User.objects.get(userName=userName)
        reviewList = Review.objects.select_related('productId','userID').order_by('-dtm_crt').filter(userID__userName = getUser.userName)

        userStatsData = []
        with connection.cursor() as cursor:
            raw_sql =""" 
                            with  
                                stats as(
                                    select 
                                        (select count(*) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            where u.userID = """+str(getUser.userID)+""" and r.rating <= 10 and r.rating >=8
                                        ) as positive,
                                        (
                                            select count(*) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            where u.userID = """+str(getUser.userID)+""" and r.rating < 8 and r.rating >=5
                                        ) as mixed,
                                        (
                                            select count(*) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            where u.userID = """+str(getUser.userID)+""" and r.rating < 5 and r.rating >=0
                                        ) as negative
                                        , u.userID as UserID
                                        from review_review as r
                                        join register_user as u on r.userID_id = u.userID
                                        where u.userID = """+str(getUser.userID)+"""
                                ),
                                maxMin as( 
                                    select (select max(r.rating) from review_review as r
                                    join register_user as u on u.userID = r.userID_id
                                    join product_product as p on p.productId = r.productId_id
                                    where u.userID = """+str(getUser.userID)+"""
                                    order by r.dtm_crt desc) as highRate,
                                    
                                    (
                                        select p.productName from review_review as r
                                        join register_user as u on u.userID = r.userID_id
                                        join product_product as p on p.productId = r.productId_id
                                        where r.rating = (
                                            select max(r.rating) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            join product_product as p on p.productId = r.productId_id
                                            where u.userID = """+str(getUser.userID)+"""
                                        ) and u.userID = """+str(getUser.userID)+"""
                                        order by r.dtm_crt desc
                                        limit 1
                                    ) as highRateName,
                                    
                                    (select min(r.rating) from review_review as r
                                    join register_user as u on u.userID = r.userID_id
                                    join product_product as p on p.productId = r.productId_id
                                    where u.userID = """+str(getUser.userID)+"""
                                    order by r.dtm_crt desc) as minRate,
                                    
                                    (
                                        select p.productName from review_review as r
                                        join register_user as u on u.userID = r.userID_id
                                        join product_product as p on p.productId = r.productId_id
                                        where r.rating = (
                                            select min(r.rating) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            join product_product as p on p.productId = r.productId_id
                                            where u.userID = """+str(getUser.userID)+"""
                                        ) and u.userID = """+str(getUser.userID)+"""
                                        order by r.dtm_crt desc
                                        limit 1
                                    
                                    ) as minRateName,
                                    
                                    u.userID as UserID
                                    from review_review as r
                                    join register_user as u on r.userID_id = u.userID
                                    where u.userID = """+str(getUser.userID)+"""
                                )
                                select distinct (positive), mixed, negative, highRate, highRateName, minRate, minRateName
                                from stats join maxMin using (UserID)
                        """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                userStatsData.append({
                    "positive": qux[0],
                    "mixed": qux[1],
                    "negative": qux[2],
                    "highestRate":numIndicator (qux[3]),
                    "highestRateName":qux[4],
                    "lowestRate":numIndicator (qux[5]),
                    "lowestRateName":qux[6]
                })

        getReviewListByPage = None
        if reviewList:
            paginator = Paginator(reviewList,4)
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
            getReviewListByPage = Review.objects.none()
            next_url = ''
            prev_url = ''


        context = {
            'userData': userStatsData,
            'obj':getReviewListByPage,
            'User':getUser,
            'userPending': countUserPending(request),
            'next_page_url': next_url,
            'prev_page_url': prev_url
        }

        return render(request,'profile.html', context)
    except Exception as e:
        print(e)
        context = {
            'message': "User "+ userName +" Not Found"
        }
        return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def editProfilePicture (request,userName):
    error = 0
    try:
        getUser = User.objects.get(userName=userName)
        web_direct = None
        if request.user.username != getUser.userName:
            return HttpResponse('You are not allowed to view this page')
        elif request.method != 'POST':
            context = {
                'User': getUser,
                'context': 'profilePicture'
            }
            return render(request,'profileEdit.html', context)
        else:

            if os.path.exists(getUser.profilePicture.name):
                os.remove(getUser.profilePicture.name)
            else:
                pass

            profilePic = request.FILES['profilePicture']
            profilePic.name = userName+'.jpg'
            error = 1

            getUser.profilePicture = profilePic
            getUser.save()

            web_direct = 'success.html'

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': "User "+ userName +" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)

    return render(request,web_direct)

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def editUserData (request,userName):
    
    error = 0
    try:
        getUser = User.objects.get(userName=userName)

        if request.user.username != getUser.userName:
            return HttpResponse('You are not allowed to view this page')
        elif request.method != 'POST':
            context = {
                'User': getUser,
                'context': 'userData'
            }
            return render(request,'profileEdit.html', context)
        else:
            name = request.POST.get('userName')
            description = request.POST.get('description')
            error = 1
            if name == '':
                raise Exception("Username Empty")

            if User.objects.filter(userName = name).first():
                if (request.user.username == name):
                    pass
                else:
                    messages.success(request, 'User Name is Taken')
                    return redirect ('editUserData', userName = userName)

            getUser.userName = name
            getUser.description = description
            getUser.save()

            getUserAuth = auth_user.objects.get(username=userName)
            getUserAuth.username = name
            getUserAuth.save()

            return redirect ('profilePage', userName = getUserAuth.username)

    except Exception as e:
        print(e)
        if error == 0:
            context = {
                'message': "User "+ userName +" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)

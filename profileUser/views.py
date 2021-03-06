from profileUser.filters import userFilters
from django.contrib.sites.shortcuts import get_current_site
from register.forms import RejectionReason
from django.http import HttpResponse
from django.shortcuts import redirect,render
from register.models import MusicStoreData, User
from django.contrib import messages
from review.models import Review
from django.db import connection
from Skripsi.views import checkChar, countReport, loginAccount, countUserPending, forgotPassword, numIndicator, sendMail
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
    error = 0
    try:   
        getUser = User.objects.get(userName=userName)
        reviewList = Review.objects.select_related('productId','userID').order_by('-dtm_crt').filter(userID__userName = getUser.userName)
        error = 1
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
                                        select b.brandName from review_review as r
                                        join register_user as u on u.userID = r.userID_id
                                        join product_product as p on p.productId = r.productId_id
                                        join product_brand as b on p.brandId_id = b.brandId
                                        where r.rating = (
                                            select max(r.rating) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            join product_product as p on p.productId = r.productId_id
                                            where u.userID = """+str(getUser.userID)+"""
                                        ) and u.userID = """+str(getUser.userID)+"""
                                        order by r.dtm_crt desc
                                        limit 1
                                    ) as highRateBrand,
                                    
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
                                    
                                    (
                                    select min(r.rating) from review_review as r
                                    join register_user as u on u.userID = r.userID_id
                                    join product_product as p on p.productId = r.productId_id
                                    where u.userID = """+str(getUser.userID)+"""
                                    order by r.dtm_crt desc) as minRate,
                                    
									(
                                        select b.brandName from review_review as r
                                        join register_user as u on u.userID = r.userID_id
                                        join product_product as p on p.productId = r.productId_id
                                        join product_brand as b on p.brandId_id = b.brandId
                                        where r.rating = (
                                            select min(r.rating) from review_review as r
                                            join register_user as u on u.userID = r.userID_id
                                            join product_product as p on p.productId = r.productId_id
                                            where u.userID = """+str(getUser.userID)+"""
                                        ) and u.userID = """+str(getUser.userID)+"""
                                        order by r.dtm_crt desc
                                        limit 1
                                    ) as minRateBrand,
                                    
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
                                select distinct (positive), mixed, negative, highRate, highRateBrand, highRateName, minRate, minRateBrand, minRateName
                                from stats join maxMin using (UserID)
                        """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                userStatsData.append({
                    "positive": qux[0],
                    "mixed": qux[1],
                    "negative": qux[2],
                    "highestRate":numIndicator (qux[3]),
                    "highRateBrand":qux[4],
                    "highestRateName":qux[5],
                    "lowestRate":numIndicator (qux[6]),
                    "lowestRateBrand":qux[7],
                    "lowestRateName":qux[8]
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

        if getUser.roleId == 'Mus_Store':
            getUser = MusicStoreData.objects.select_related('userID').get(userID__userName=userName)

        context = {
            'userData': userStatsData,
            'obj':getReviewListByPage,
            'User':getUser,
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
            'next_page_url': next_url,
            'prev_page_url': prev_url
        }

        return render(request,'profile.html', context)
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
        context = None
        getUser = User.objects.get(userName=userName)

        if request.user.username != getUser.userName:
            return HttpResponse('You are not allowed to view this page')

        if getUser.roleId == "Mus_Store":
           getUser = MusicStoreData.objects.select_related('userID').get(userID__userName=userName)
           context = 'music store'
        else:
           context = 'user data'

        if request.method != 'POST':
            context = {
                'User': getUser,
                'context': context
            }
            return render(request,'profileEdit.html', context)
        else:
            if context == 'user data':
                name = request.POST.get('userName')
                description = request.POST.get('description')
                error = 1
                if name == '':
                    raise Exception("Username Empty")

                if len(name) > 20:
                    messages.success(request, 'Store Name has tobe less than or equal 20 characters')
                    return redirect ('editUserData', userName = userName)

                if User.objects.filter(userName = name).first():
                    if (request.user.username == name):
                        pass
                    else:
                        messages.success(request, 'User Name is Taken')
                        return redirect ('editUserData', userName = userName)
                
                if checkChar (name) == False:
                    messages.success(request, 'Name cannot contain / , # , and ?')
                    return redirect ('editUserData', userName = userName)

                getUser.userName = name
                getUser.description = description
                getUser.save()

                getUserAuth = auth_user.objects.get(username=userName)
                getUserAuth.username = name
                getUserAuth.save()

                return redirect ('profilePage', userName = getUserAuth.username)
            else:
                name = request.POST.get('userName')
                address = request.POST.get('address')
                contact = request.POST.get('contact')
                description = request.POST.get('description')
                error = 1

                if name == '':
                    raise Exception("Username Empty")
                if address == '':
                    raise Exception("Username Empty")
                if contact == '':
                    raise Exception("Username Empty")



                if User.objects.filter(userName = name).first():
                    if (request.user.username == name):
                        pass
                    else:
                        messages.success(request, 'User Name is Taken')
                        return redirect ('editUserData', userName = userName)

                if len(name) > 20:
                    messages.success(request, 'Store Name has tobe less than or equal 20 characters')
                    return redirect ('editUserData', userName = userName)                            
    
                if checkChar (name) == False:
                    messages.success(request, 'Name cannot contain / , # , and ?')
                    return redirect ('editUserData', userName = userName)

                if len(contact) > 16:
                    messages.success(request, 'contact too long')
                    return redirect ('editUserData', userName = userName)

                if not contact.isdigit():
                    messages.success(request, 'contact must be numeric')
                    return redirect ('editUserData', userName = userName)                        
                
                getUser.address = address
                getUser.contact = contact
                getUser.save()
                
                getUserData = User.objects.get(userName = getUser.userID.userName)
                getUserData.userName = name
                getUserData.description = description
                getUserData.save()

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

@login_required
@allowed_users(allowed_roles=['Admin'])
def userControl (request):

    getAllUser = userFilters(
        request.GET,
        User.objects.order_by('userName').all()
    )
    
    getAllUsersByPage = None
    if getAllUser:
        paginator = Paginator(getAllUser.qs,4)
        page_number = request.GET.get('page', 1)
        getAllUsersByPage = paginator.get_page(page_number)

        if getAllUsersByPage.has_next():
            next_url = getAllUsersByPage.next_page_number()
        else:
            next_url = ''

        if getAllUsersByPage.has_previous():
            prev_url = getAllUsersByPage.previous_page_number()
        else:
            prev_url = ''
    else:
        getAllUsersByPage = User.none()
        next_url = ''
        prev_url = ''

    context = {
        'filter':getAllUser,
        'obj':getAllUsersByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }

    return render(request,'usercontrol.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def deleteUser (request,auth_token):
    if request.method != 'POST':
        rejectionForm = RejectionReason()
        context = {
            'form': rejectionForm,
            'userPending': countUserPending(request)
        }
        return render(request,'deletionReason.html', context)
    else :
        rejectionReason = request.POST.get('reason')
        try:
            profile_obj = User.objects.get(auth_token = auth_token)
            if profile_obj:    
                if profile_obj.roleId == 'Mus_Store':   
                    musicStore = MusicStoreData.objects.select_related('userID').get(userID__userName = profile_obj.userName)
                    if os.path.exists(musicStore.musicStorePicture.name) and os.path.exists(musicStore.musicStorePicture2.name) and os.path.exists(musicStore.musicStorePicture3.name):
                        os.remove(musicStore.musicStorePicture.name)
                        os.remove(musicStore.musicStorePicture2.name)
                        os.remove(musicStore.musicStorePicture3.name)
                    else:
                        pass
                else:
                    if os.path.exists(profile_obj.profilePicture.name):
                        os.remove(profile_obj.profilePicture.name)
                    else:
                        pass


                domain = get_current_site(request).domain
                sendMail (domain, profile_obj, 'admin_delete',rejectionReason)

                userAuth = auth_user.objects.get(username = profile_obj.userName)
                userAuth.groups.clear()
                userAuth.delete()

                profile_obj.delete()

                webRender = 'success.html'
                return redirect('usercontrol')
            else:
                raise Exception("User Empty")

        except Exception as e:
            print (e) 
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)
            
        
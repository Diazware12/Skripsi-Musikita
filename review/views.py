from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .forms import ReviewForm, ReportForm
from .models import Review, HelpfulData, Report
from product.models import Product
from register.models import User
from datetime import datetime
from django.db import connection

from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import allowed_users

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def reviewProduct (request, productName, brand):
    error = 0
    try:
        product = Product.objects.select_related('brandId').get(productName=productName,brandId__brandName=brand) #
        userAuthName = request.user.username
        user = User.objects.get(userName = userAuthName)

    
        if Review.objects.filter(productId=product,userID=user).first():
            return HttpResponse('You are not allowed to view this page')
        if request.method != 'POST':
            review_form = ReviewForm()
            context = {
                'form': review_form,
                'Brand': brand,
                'productName': productName
            }
            return render(request,'scoreRating.html', context)
        else :

            rate = request.POST.get('rate')
            reviewTitle = request.POST.get('reviewTitle')
            reviewDescription = request.POST.get('reviewDescription')
            error = 1
            
            if rate == None:
                messages.success(request, 'you need to fill-in the rate')
                return redirect ('reviewProduct', brand=brand, productName=productName)

            if reviewTitle == '' or reviewDescription == '':
                raise Exception("required field Empty")

            if len(reviewDescription) < 75:
                messages.success(request, 'review need to be equal or more than 75 character')
                return redirect ('reviewProduct', brand=brand, productName=productName)
                
            rating_obj = Review.objects.create(
                productId = product,
                userID = user,
                dtm_crt = datetime.now(),
                title = reviewTitle,
                description = reviewDescription,
                rating = rate
            )
            rating_obj.save()

            putReviewAvg(rating_obj)

            return redirect ('showProduct', brand=brand, productName=productName)

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)

def putReviewAvg(rating):
    average = 0
    with connection.cursor() as cursor:
        raw_sql =""" 
                    with 
                        avgUser as(
                            select 
                                FORMAT (avg(r.rating), 1) as user_avg,
                                p.productId as productId
                            from review_review as r
                            join register_user as u on r.userID_id = u.userID
                            join product_product as p on r.productId_id = p.productId
                            where u.roleId like "%Reg_User%" and p.productId= """+str(rating.productId.productId)+"""),

                        avgMusStore as(
                        select 
                            FORMAT (avg(r.rating), 1) as Mus_store_avg,
                            p.productId as productId
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Mus_Store%" and p.productId= """+str(rating.productId.productId)+""")
                        
                    select user_avg, Mus_store_avg, ((user_avg + Mus_store_avg)/2) as bothAvg 
                    from avgUser join avgMusStore using (productId)
                """            
        cursor.execute(raw_sql)

        for qux in cursor.fetchall():
            average = float(qux[2])

        avgUpdate = Product.objects.get(productId=rating.productId.productId)
        if average != None:
            if average == 0.00:
                avgUpdate.avgScore = None
            else:
                avgUpdate.avgScore = average
            avgUpdate.dtm_upd = datetime.now()
            avgUpdate.save()

    return 'success'

def updateReviewAvg(product):
    average = 0
    with connection.cursor() as cursor:
        raw_sql =""" 
                    with 
                        avgUser as(
                            select 
                                FORMAT (avg(r.rating), 1) as user_avg,
                                p.productId as productId
                            from review_review as r
                            join register_user as u on r.userID_id = u.userID
                            join product_product as p on r.productId_id = p.productId
                            where u.roleId like "%Reg_User%" and p.productId= """+str(product.productId)+"""),

                        avgMusStore as(
                        select 
                            FORMAT (avg(r.rating), 1) as Mus_store_avg,
                            p.productId as productId
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Mus_Store%" and p.productId= """+str(product.productId)+""")
                        
                    select user_avg, Mus_store_avg, ((user_avg + Mus_store_avg)/2) as bothAvg 
                    from avgUser join avgMusStore using (productId)
                """            
        cursor.execute(raw_sql)

        for qux in cursor.fetchall():
            average = float(qux[2])

        avgUpdate = Product.objects.get(productId=product.productId)
        if average != None:
            if average == 0.00:
                avgUpdate.avgScore = None
            else:
                avgUpdate.avgScore = average
            
            avgUpdate.dtm_upd = datetime.now()
            avgUpdate.save()

    return 'success'

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def updateReview (request, productName, brand, user_select, action):
    error = 0
    try:
        product = Product.objects.select_related('brandId').get(productName=productName,brandId__brandName=brand) #
        userAuthName = request.user.username
        user = User.objects.get(userName = userAuthName)

        getReview = Review.objects.select_related('productId','userID').get(productId=product,userID=user)
        if request.user.username != getReview.userID.userName:
            return HttpResponse('You are not allowed to view this page')
        if request.method != 'POST':
            backButton = None
            if action == 'ratingReview':
                backButton = 'ratingReview'
            else:
                backButton = 'profilePage'

            context = {
                'review': getReview,
                'brand': brand,
                'productName': productName,
                'User': user,
                'backButton': backButton
            }
            return render(request,'scoreRatingEdit.html', context)
        else :

            rate = request.POST.get('rate')
            reviewTitle = request.POST.get('reviewTitle')
            reviewDescription = request.POST.get('reviewDescription')
            error = 1
            
            if rate == None:
                messages.success(request, 'you need to fill-in the rate')
                return redirect ('updateReview', brand=brand, productName=productName, user_select=user_select, action='ratingReview')

            if reviewTitle == '' or reviewDescription == '':
                raise Exception("required field Empty")

            if len(reviewDescription) < 75:
                messages.success(request, 'review need to be equal or more than 75 character')
                return redirect ('updateReview', brand=brand, productName=productName, user_select=user_select, action='ratingReview')

            getReview.rating = rate    
            getReview.title = reviewTitle
            getReview.description = reviewDescription    
            getReview.dtm_crt = datetime.now()

            getReview.save()

            putReviewAvg(getReview)

            if action == 'ratingReview':
                return redirect ('showProduct', brand=brand, productName=productName)
            else:
                return redirect ('profilePage', userName=user_select)
            

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store','Admin'])
def deleteReview(request, productName, brand, user_select, action):
    error = 0
    try:
        product = Product.objects.select_related('brandId').get(productName=productName,brandId__brandName=brand) #
        userAuth = request.user
        user = User.objects.get(userName = userAuth.username)

        getUserReview = User.objects.get(userName = user_select)

        getReview = Review.objects.select_related('productId','userID').get(productId=product,userID=getUserReview.userID)
        if userAuth.groups.filter(name='Admin').exists():
            pass
        elif userAuth.username != user.userName:
            return HttpResponse('You are not allowed to view this page')
        
        getReview.delete()

        updateReviewAvg(product)

        if action == 'ratingReview':
            return redirect ('showProduct', brand=brand, productName=productName)
        else:
            return redirect ('profilePage', userName=user_select)

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': 'error'
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)
    

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def feedback (request, productName, brand, feedback, user):
    getProduct = Product.objects.select_related(
                        'brandId').get(
                        productName = productName,
                        brandId__brandName = brand)

    getReview = Review.objects.select_related('userID').get(
                    productId = getProduct.productId,
                    userID__userName = user
                )

    username = None
    userSubmitHelpful = None
    getUser = request.user.username
    if getUser != '':
        username = request.user.username
        userSubmitHelpful = User.objects.get(userName = username)
    else:
        username = ''

    getHelpfulData = HelpfulData.objects.filter(reviewId=getReview,userID=userSubmitHelpful)
    if getHelpfulData:
        messages.success(request, 'You Already Submit Yout Response for This Review Before')
        return redirect ('showProduct', brand=brand, productName=productName)
    else:
        if feedback == "helpful" :
            getReview.helpful += 1
            getReview.save()

            helpObject = HelpfulData.objects.create(
                reviewId = getReview,
                userID = userSubmitHelpful
            )
            helpObject.save()
            messages.success(request, 'success')
        else : 
            getReview.notHelpful += 1
            getReview.save()

            helpObject = HelpfulData.objects.create(
                reviewId = getReview,
                userID = userSubmitHelpful
            )
            helpObject.save()
            messages.success(request, 'success')

    return redirect ('showProduct', brand=brand, productName=productName)

@login_required
@allowed_users(allowed_roles=['Reg_User','Mus_Store'])
def reportReview (request, productName, brand, user):
    error = 0
    try:
        getProduct = Product.objects.select_related(
                            'brandId').get(
                            productName = productName,
                            brandId__brandName = brand)

        obj = Review.objects.select_related('userID').get(
                    productId = getProduct.productId,
                    userID__userName = user
                )
        web_direct = None
        if request.method != 'POST':
            form = ReportForm()
            context = {
                'form': form,
                'obj': obj,
                'productName': getProduct.productName,
                'brand': getProduct.brandId.brandName
            }
            return render(request,'reportView.html', context)
        else :
            reason = request.POST.get('reportReason')
            error = 1

            if reason == '' or reason == None:
                raise Exception("required field Empty")

            getUser = User.objects.get(userName = request.user.username)
                
            report_obj = Report.objects.create(
                reviewId = obj,
                userID = getUser,
                reason = reason
            )
            report_obj.save()

            return redirect('showProduct', brand=brand, productName=productName)

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)
 
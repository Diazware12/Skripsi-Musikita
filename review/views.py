from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ReviewForm
from .models import Review, HelpfulData
from product.models import Product
from register.models import User
import datetime
from django.db import connection

from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import is_User

@login_required
@user_passes_test(is_User)
def reviewProduct (request, productName, brand):
    web_direct = ''
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
        
        product = Product.objects.get(productName=productName) #
        userAuthName = request.user.username
        user = User.objects.get(userName = userAuthName) #

        try: 
            if rate == '':
                messages.success(request, 'you need to fill-in the rate')
                return redirect ('reviewProduct', brand=brand, productName=productName)
            
            rating_obj = Review.objects.create(
                productId = product,
                userID = user,
                dtm_crt = datetime.date.today(),
                title = reviewTitle,
                description = reviewDescription,
                rating = rate
            )
            rating_obj.save()

            putReviewAvg(rating_obj)

            return redirect ('showProduct', brand=brand, productName=productName)

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)

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
            avgUpdate.avgScore = average
            avgUpdate.save()

    return 'success'

@login_required
@user_passes_test(is_User)
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
    
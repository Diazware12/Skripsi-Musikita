from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from product.models import Product
from register.models import User
import datetime

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

            return redirect ('showProduct', brand=brand, productName=productName)

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)
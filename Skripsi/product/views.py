from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from django.conf import settings
from product.models import Product
import datetime

def addProduct (request):
    if request.method != 'POST':
        form = ProductForm()
        context = {
            'form': form
        }
        return render(request,'addProduct.html', context)
    else :
        productName = request.POST.get('productName')
        description = request.POST.get('description')
        videoUrl = request.POST.get('videoUrl')
        productPicture = request.POST.get('productPicture')

        web_direct = ''

        try: 
            if Product.objects.filter(productName=productName).first():
                messages.success(request, 'Product is already exist')
                web_direct = 'success.html'

            product_obj = Product.objects.create(
                subCategoryId = 1,
                brandId = 1,
                productName = productName,
                description = description,
                videoUrl = videoUrl,
                minPrice = 0,
                maxPrice = 0,
                dtm_crt = datetime.date.today(),
                productIMG = productPicture
            )

            product_obj.save()
            web_direct = 'success.html'

        except Exception as e:
            print(e)
            web_direct = 'error.html'

    return render(request,web_direct)

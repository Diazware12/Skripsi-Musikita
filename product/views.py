from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import ProductForm
from django.conf import settings
from product.models import Product, Category, SubCategory, Brand
import datetime

def addProduct (request):
    if request.method != 'POST':
        ddCategory = Category.objects.all()
        ddSubCategory = SubCategory.objects.all()
        form = ProductForm()
        context = {
            'form': form,
            'category': ddCategory,
            'subCategory': ddSubCategory,
        }
        return render(request,'addProduct.html', context)
    else :
        productName = request.POST.get('productName') 
        brand = request.POST.get('productBrand') 
        category = request.POST.get('category')
        subCategory = request.POST.get('subCategory')
        description = request.POST.get('description')
        videoUrl = request.POST.get('videoUrl')
        productPicture = request.POST.get('productPicture')

        web_direct = ''

        brand_Id = Brand.objects.filter(brandName = brand).values_list(
                        'brandId', flat=True
                      ).first()

        category_Id = Category.objects.filter(categoryName = category).values_list(
                        'categoryId', flat=True
                      ).first()

        subCategory_Id = SubCategory.objects.filter(
                            subCategoryName = subCategory, 
                            categoryId = category_Id
                        ).values_list(
                            'subCategoryId', 
                            flat=True
                        ).first()
        
        try: 
            # if Product.objects.filter(productName=productName).first():
            #     messages.success(request, 'Product is already exist')
            #     web_direct = 'success.html'

            product_obj = Product.objects.create(
                categoryId = category_Id,
                subCategoryId = subCategory_Id,
                brandId = brand_Id,
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

def getJsonCategoryData (request):
    catValue = list(Category.objects.values())
    return JsonResponse ({
        'data':catValue 
    })

def getJsonSubCategoryData (request, *args, **kwargs):
    selected_category = kwargs.get('cat')

    cat_Id = Category.objects.filter(
                    categoryName = selected_category
            ).values_list('categoryId', flat=True
            ).first()

    print(cat_Id)

    subCat_models = list(
        SubCategory.objects.filter(categoryId=cat_Id).values()
    )

    return JsonResponse ({
        'data':subCat_models 
    })
    

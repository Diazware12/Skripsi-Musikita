from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import ProductForm
from django.conf import settings
from product.models import Product, Category, SubCategory, Brand
import datetime
from PIL import Image
from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import is_Admin


@login_required
@user_passes_test(is_Admin)
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
        productPicture = request.FILES['productPicture']
        productPicture.name = productName+'.jpg'
        web_direct = ''

        brand_Id = Brand.objects.get(brandName = brand)

        category_Id = Category.objects.get(categoryName = category)

        subCategory_Id = SubCategory.objects.get(
                            subCategoryName = subCategory, 
                            categoryId = category_Id
                        )
        
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
            img = Image.open(product_obj.productIMG.path)
            img = make_square(img)
            img.save(product_obj.productIMG.path)
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
    
def make_square(img):
    x, y = img.size
    size = max(x,y)
    fill_color=(255, 255, 255)
    new_img = Image.new('RGB', (size, size), fill_color)
    new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)))
    return new_img
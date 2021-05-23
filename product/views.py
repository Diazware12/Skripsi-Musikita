from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import ProductForm
from django.conf import settings
from product.models import Product, Category, SubCategory, Brand
import datetime
from PIL import Image
from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import is_Admin
from Skripsi.views import loginAccount
from review.models import Review
from django.db import connection

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
            if Product.objects.select_related('brandId').filter(productName=productName,brandId__brandName=brand_Id.brandName).first():
                messages.success(request, 'Product is already exist')
                return redirect ('addProduct')

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
    fill_color=(255, 255, 255)

    img.load() # required for png.split()

    #rbgimage = Image.new("RGB", img.size, fill_color)
    #rbgimage.paste(img, mask=img.split()[3]) # 3 is the alpha channel

    x, y = img.size
    size = max(x,y)
    new_img = Image.new('RGB', (size, size), fill_color)
    if img.mode == 'RGBA':
        new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)), mask=img.split()[3])
    else :
        new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)))
    return new_img

def showProduct (request, productName, brand):
    isLogin = request.POST.get('isLogin')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    
    user_review = Review.objects.select_related('userID','productId').filter(userID__roleId="Reg_User",productId__productName=productName)
    ms_review = Review.objects.select_related('userID','productId').filter(userID__roleId="Mus_Store",productId__productName=productName)

    obj = Product.objects.select_related('brandId').get(productName = productName, brandId__brandName=brand)

    ratingResults = []

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
                            where u.roleId like "%Reg_User%" and p.productId= """+str(obj.productId)+"""),

                        avgMusStore as(
                        select 
                            FORMAT (avg(r.rating), 1) as Mus_store_avg,
                            p.productId as productId
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Mus_Store%" and p.productId= """+str(obj.productId)+"""),
                        
                        statsUser as (
                            select 
                            FORMAT((
                                (select count(*) from review_review as r
                                join register_user as u on r.userID_id = u.userID
                                where u.roleId like "%Reg_User%" and productId_id = """+str(obj.productId)+""" and r.rating <= 10 and r.rating >=8)
                                /(count(u.userID))
                                *100
                            ),0) as positive_user,
                            FORMAT((
                                (select count(*) from review_review as r
                                join register_user as u on r.userID_id = u.userID
                                where u.roleId like "%Reg_User%" and productId_id = """+str(obj.productId)+""" and r.rating < 8 and r.rating >=5)
                                /(count(u.userID))
                                *100
                            ),0) as mixed_user,
                            FORMAT((
                                (select count(*) from review_review as r
                                join register_user as u on r.userID_id = u.userID
                                where u.roleId like "%Reg_User%" and productId_id = """+str(obj.productId)+""" and r.rating < 5 and r.rating >=0)
                                /(count(u.userID))
                                *100
                            ),0) as negative_user,
                            p.productId as productId
                            from review_review as r
                            join register_user as u on r.userID_id = u.userID
                            join product_product as p on r.productId_id = p.productId
                            where u.roleId like "%Reg_User%" and p.productId = """+str(obj.productId)+"""
                        ),

                        statsMusStore as (
                            select 
                                FORMAT((
                                    (select count(*) from review_review as r
                                    join register_user as u on r.userID_id = u.userID
                                    where u.roleId like "%Mus_Store%" and productId_id = """+str(obj.productId)+""" and r.rating <= 10 and r.rating >=8)
                                    /(count(u.userID))
                                    *100
                                ),0) as positive_ms,
                                FORMAT((
                                    (select count(*) from review_review as r
                                    join register_user as u on r.userID_id = u.userID
                                    where u.roleId like "%Mus_Store%" and productId_id = """+str(obj.productId)+""" and r.rating < 8 and r.rating >=5)
                                    /(count(u.userID))
                                    *100
                                ),0) as mixed_ms,
                                FORMAT((
                                    (select count(*) from review_review as r
                                    join register_user as u on r.userID_id = u.userID
                                    where u.roleId like "%Mus_Store%" and productId_id = """+str(obj.productId)+""" and r.rating < 5 and r.rating >=0)
                                    /(count(u.userID))
                                    *100
                                ),0) as negative_ms,
                                p.productId as productId
                                from review_review as r
                                join register_user as u on r.userID_id = u.userID
                                join product_product as p on r.productId_id = p.productId
                                where u.roleId like "%Mus_Store%" and p.productId = """+str(obj.productId)+"""
                        )    
                        
                    select user_avg, Mus_store_avg, positive_user, mixed_user, negative_user, positive_ms, mixed_ms, negative_ms
                    from avgUser join avgMusStore using (productId)
                    join statsUser using (productId)
                    join statsMusStore using (productId)      
                """            
        cursor.execute(raw_sql)

        for qux in cursor.fetchall():
            ratingResults.append({
                "userAvg": qux[0],
                "musStoreAvg": qux[1],
                "positive_user": qux[2],
                "mixed_user": qux[3],
                "negative_user": qux[4],
                "positive_music": qux[5],
                "mixed_music": qux[6],
                "negative_music": qux[7]
            })

    context = {
        'obj': obj,
        'user_review': user_review,
        'ms_review': ms_review,
        'rateSum': ratingResults
    }

    return render(request,'rating.html', context)

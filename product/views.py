from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import ProductForm
from django.conf import settings
from product.models import Product, Category, SubCategory, Brand
from datetime import datetime
from PIL import Image
from django.contrib.auth.decorators import login_required, user_passes_test
from Skripsi.decorator import allowed_users
from review.models import Review
from django.db import connection
import requests
import os
from Skripsi.views import loginAccount, countUserPending, forgotPassword, numIndicator
from django.core.paginator import Paginator

@login_required
@allowed_users(allowed_roles=['Admin'])
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

        brand_Id = Brand.objects.get(brandName = brand)

        category_Id = Category.objects.get(categoryName = category)

        subCategory_Id = SubCategory.objects.get(
                            subCategoryName = subCategory, 
                            categoryId = category_Id
                        )
        
        try:
            if productName == '' or brand == '' or category == '' or subCategory == '' or description == '' or videoUrl == '':
                raise Exception("required field Empty")

            if Product.objects.select_related('brandId').filter(productName=productName,brandId__brandName=brand_Id.brandName).first():
                messages.success(request, 'Product is already exist')
                return redirect ('addProduct')

            if len(description) < 75:
                messages.success(request, 'description need to be equal or more than 75 character')
                return redirect ('addProduct')

            req = requests.head(videoUrl)
            if req.status_code == 404:
                messages.success(request, 'video Url\'s not valid')
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
                dtm_crt = datetime.now()
            )

            product_obj.save()
            web_direct = 'success.html'

            return redirect ('addProductPicture', brand=brand_Id.brandName, productName=product_obj.productName)

        except Exception as e:
            print(e)
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def addEditProduct (request,context,productName,brand):
    error = 0
    try:
        getProduct = Product.objects.select_related('brandId').get(
            brandId__brandName=brand,
            productName=productName)

        if request.method != 'POST':
            ddCategory = Category.objects.all()
            ddSubCategory = SubCategory.objects.all()
            product = getProduct
            form = ProductForm()
            context = {
                'form':form,
                'product': product,
                'category': ddCategory,
                'subCategory': ddSubCategory,
            }
            return render(request,'addProductEdit.html', context)
        else :
            productName = request.POST.get('productName') 
            brand = request.POST.get('productBrand') 
            category = request.POST.get('category')
            subCategory = request.POST.get('subCategory')
            description = request.POST.get('description')
            videoUrl = request.POST.get('videoUrl')
            error = 1

            brand_Id = Brand.objects.get(brandName = brand)

            category_Id = Category.objects.get(categoryName = category)

            subCategory_Id = SubCategory.objects.get(
                                subCategoryName = subCategory, 
                                categoryId = category_Id
                            )

            if productName == '' or brand == '' or category == '' or subCategory == '' or description == '' or videoUrl == '':
                raise Exception("required field Empty")
            
            if len(description) < 75:
                messages.success(request, 'description need to be equal or more than 75 character')
                return redirect ('editProduct',productName=productName,brand=brand)
                
            req = requests.head(videoUrl)
            if req.status_code == 404:
                messages.success(request, 'video Url\'s not valid')
                return redirect ('editProduct',productName=productName,brand=brand)

            getProduct.categoryId=category_Id
            getProduct.subCategoryId = subCategory_Id
            getProduct.brandId = brand_Id
            getProduct.productName = productName
            getProduct.description = description
            getProduct.videoUrl = videoUrl
            getProduct.minPrice = 0
            getProduct.maxPrice = 0
            getProduct.dtm_upd = datetime.now()
            getProduct.save()

            if (context == "editAddProduct"):
                return redirect ('addProductPicture', brand=brand_Id.brandName, productName=getProduct.productName)

    except Exception as e:
        print(e)

        context = None
        if error == 0:            
            context = {
                'message': "product "+productName+" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        
        return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def getJsonCategoryData (request):
    catValue = list(Category.objects.values())
    return JsonResponse ({
        'data':catValue 
    })

@login_required
@allowed_users(allowed_roles=['Admin'])
def getJsonCategoryDataEdit (request,context,brand,productName):
    catValue = list(Category.objects.values())
    return JsonResponse ({
        'data':catValue 
    })

@login_required
@allowed_users(allowed_roles=['Admin'])
def getJsonSubCategoryDataEdit (request,context,brand,productName, *args, **kwargs):
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

@login_required
@allowed_users(allowed_roles=['Admin'])
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

@login_required
@allowed_users(allowed_roles=['Admin'])
def addEditPicture (request,productName,brand):
    web_direct = ''
    if request.method != 'POST':
        context = {
            'brand': brand,
            'productName': productName,
        }
        return render(request,'addProductPicture.html',context)
    else:
        productPicture = request.FILES['productPicture']
        productPicture.name = productName+'.jpg'    
        
        getProduct = Product.objects.select_related(
                            'brandId').get(
                            productName = productName,
                            brandId__brandName = brand)

        if os.path.exists(str(getProduct.productIMG)):
            os.remove(str(getProduct.productIMG))
        else:
            pass

        getProduct.productIMG = productPicture
        getProduct.save()

        web_direct = 'success.html'
        
    return render(request,web_direct)

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
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    try:
        user_review = Review.objects.select_related('userID','productId').filter(userID__roleId="Reg_User",productId__productName=productName)[:5]
        ms_review = Review.objects.select_related('userID','productId').filter(userID__roleId="Mus_Store",productId__productName=productName)[:5]
        obj = Product.objects.select_related('brandId').get(productName = productName, brandId__brandName=brand)

        ratingUserScore = []
        ratingMusicStore = []
        userAvg = None
        musStoreAvg = None
        with connection.cursor() as cursor:
            raw_sql =""" 
                        with                         
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
                            )
                        select positive_user, mixed_user, negative_user
                        from statsUser  
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                ratingUserScore.append({
                    "positive_user": qux[0],
                    "mixed_user": qux[1],
                    "negative_user": qux[2]
                })

        with connection.cursor() as cursor:
            raw_sql =""" 
                        with                         
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
                            
                        select positive_ms, mixed_ms, negative_ms
                        from statsMusStore 
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                ratingMusicStore.append({
                    "positive_music": qux[0],
                    "mixed_music": qux[1],
                    "negative_music": qux[2]
                })

        with connection.cursor() as cursor:
            raw_sql ="""            
                        select 
                            FORMAT (avg(r.rating), 1) as user_avg
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Reg_User%" and p.productId="""+str(obj.productId)+"""
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                userAvg = numIndicator (qux[0])
            
        with connection.cursor() as cursor:
            raw_sql ="""            
                        select 
                            FORMAT (avg(r.rating), 1) as Mus_store_avg
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Mus_Store%" and p.productId="""+str(obj.productId)+"""
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                musStoreAvg = numIndicator (qux[0]) 

        username = None
        review_available = None
        messages = None
        getUser = request.user.username
        if getUser != '':
            username = request.user.username
            
            adminRoleCheck = request.user.groups.filter(name='Admin').exists()
            if adminRoleCheck == False:
                obj.visitCount = obj.visitCount+1
                obj.save()

            checkReview = Review.objects.select_related(
                            'userID','productId'
                        ).filter(userID__userName=username,productId__productName=productName)
            if not checkReview:
                review_available = "enabled"
            else:
                review_available = "disabled"
                messages = "You cannot submit another review again"

        else:
            review_available = "disabled" 
            messages = "You Need To Login First"

        otherProduct = Product.objects.order_by('-avgScore')[:6]

        context = {
            'obj': obj,
            'user_review': user_review,
            'ms_review': ms_review,
            'ratingUserScore': ratingUserScore,
            'ratingMusicStore': ratingMusicStore,
            'userAvg': userAvg,
            'musStoreAvg': musStoreAvg,
            'reviewStatus': review_available,
            'messageModal': messages,
            'userPending': countUserPending(request),
            'otherProduct': otherProduct,
            'showMore': ''
        }

        return render(request,'rating.html', context)
    except Exception as e:
        print(e)
        context = None
        context = {
            'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
        }

        return render(request,'error.html', context)

def showMoreReview (request, productName, brand, showMore):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    try:

        obj = Product.objects.select_related('brandId').get(productName = productName, brandId__brandName=brand)

        ratingUserScore = []
        ratingMusicStore = []
        userAvg = None
        musStoreAvg = None
        with connection.cursor() as cursor:
            raw_sql =""" 
                        with                         
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
                            )
                        select positive_user, mixed_user, negative_user
                        from statsUser  
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                ratingUserScore.append({
                    "positive_user": qux[0],
                    "mixed_user": qux[1],
                    "negative_user": qux[2]
                })

        with connection.cursor() as cursor:
            raw_sql =""" 
                        with                         
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
                            
                        select positive_ms, mixed_ms, negative_ms
                        from statsMusStore 
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                ratingMusicStore.append({
                    "positive_music": qux[0],
                    "mixed_music": qux[1],
                    "negative_music": qux[2]
                })

        with connection.cursor() as cursor:
            raw_sql ="""            
                        select 
                            FORMAT (avg(r.rating), 1) as user_avg
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Reg_User%" and p.productId="""+str(obj.productId)+"""
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                userAvg = numIndicator (qux[0])
            
        with connection.cursor() as cursor:
            raw_sql ="""            
                        select 
                            FORMAT (avg(r.rating), 1) as Mus_store_avg
                        from review_review as r
                        join register_user as u on r.userID_id = u.userID
                        join product_product as p on r.productId_id = p.productId
                        where u.roleId like "%Mus_Store%" and p.productId="""+str(obj.productId)+"""
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                musStoreAvg = numIndicator (qux[0]) 

        username = None
        review_available = None
        messages = None
        getUser = request.user.username
        if getUser != '':
            username = request.user.username
            
            adminRoleCheck = request.user.groups.filter(name='Admin').exists()
            if adminRoleCheck == False:
                obj.visitCount = obj.visitCount+1
                obj.save()

            checkReview = Review.objects.select_related(
                            'userID','productId'
                        ).filter(userID__userName=username,productId__productName=productName)
            if not checkReview:
                review_available = "enabled"
            else:
                review_available = "disabled"
                messages = "You cannot submit another review again"

        else:
            review_available = "disabled" 
            messages = "You Need To Login First"
        otherProduct = Product.objects.order_by('-avgScore')[:6]

        reviewList = None
        if showMore == 'Music Store':
            reviewList = Review.objects.select_related('userID','productId').filter(userID__roleId="Mus_Store",productId__productName=productName) 
        else:
            reviewList = Review.objects.select_related('userID','productId').filter(userID__roleId="Reg_User",productId__productName=productName)
        
        if reviewList:
            paginator = Paginator(reviewList,6)
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
            'obj': obj,
            'review': getReviewListByPage,
            'ratingUserScore': ratingUserScore,
            'ratingMusicStore': ratingMusicStore,
            'userAvg': userAvg,
            'musStoreAvg': musStoreAvg,
            'reviewStatus': review_available,
            'messageModal': messages,
            'userPending': countUserPending(request),
            'otherProduct': otherProduct,
            'showMore': showMore,
            'next_page_url': next_url,
            'prev_page_url': prev_url
        }

        return render(request,'rating.html', context)
    except Exception as e:
        print(e)
        context = None
        context = {
            'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
        }

        return render(request,'error.html', context)

def viewProductByCategory(request, categoryName):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)
        
    productList = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName=categoryName)[:12]
    getProductListByPage = None
    if productList:
        paginator = Paginator(productList,4)
        page_number = request.GET.get('page', 12)
        getProductListByPage = paginator.get_page(page_number)

        if getProductListByPage.has_next():
            next_url = f'?page={getProductListByPage.next_page_number()}'
        else:
            next_url = ''

        if getProductListByPage.has_previous():
            prev_url = f'?page={getProductListByPage.previous_page_number()}'
        else:
            prev_url = ''
    else: 
        getProductListByPage = Product.objects.none()
        next_url = ''
        prev_url = ''

    try:
        Category.objects.get(categoryName=categoryName)
    except:
        context = {
            'message': "There is no category \""+ categoryName +"\" available"
        }

        return render(request,'error.html', context)
        
    context={
        'productList': getProductListByPage,
        'categoryName': categoryName,
        'userPending': countUserPending(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }
    return render(request,'productListByCategory.html', context)

def viewProductBySubCategory(request, categoryName, subCategoryName):
    error = 0
    try:
        productList = Product.objects.order_by('-dtm_crt').select_related('subCategoryId','brandId').filter(subCategoryId__subCategoryName=subCategoryName,categoryId__categoryName=categoryName)[:12]
        SubCategory.objects.select_related('categoryId').get(subCategoryName=subCategoryName,categoryId__categoryName=categoryName)
        error = 1
        context={
            'productList': productList,
            'categoryName': categoryName,
            'subCategoryName': subCategoryName,
            'userPending': countUserPending(request)
        }
    except:
        context = None
        if error == 0:
            context = {
                'message': "There is no category \""+ categoryName +"\" or subcategory \""+ subCategoryName +"\" available"
            }
        else:
            context = {
                'message': 'error'
            }

        return render(request,'error.html', context)

    return render(request,'productListByCategory.html', context)

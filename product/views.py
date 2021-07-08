from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import EditorForm, ProductForm
from product.models import Product, Category, SubCategory, Brand
from datetime import datetime
from django.contrib.auth.decorators import login_required
from Skripsi.decorator import allowed_users
from review.models import Review
from django.db import connection
import os
from Skripsi.views import checkChar, countReport, loginAccount, countUserPending, forgotPassword, numIndicator
from django.core.paginator import Paginator

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def addProduct (request):
    ddCategory = Category.objects.all()
    ddSubCategory = SubCategory.objects.all()
    error = None
    msg = None
    if request.method != 'POST':
        form = ProductForm()
        context = {
            'form': form,
            'category': ddCategory,
            'subCategory': ddSubCategory,
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
        }
        return render(request,'addProduct.html', context)
    else :
        productName = request.POST.get('productName') 
        brand = request.POST.get('productBrand') 
        category = request.POST.get('category')
        subCategory = request.POST.get('subCategory')
        description = request.POST.get('description')
        videoUrl = request.POST.get('videoUrl')
        
        try:
            error = 1
            brand_Id = Brand.objects.get(brandName = brand)

            category_Id = Category.objects.get(categoryName = category)

            subCategory_Id = SubCategory.objects.get(
                                subCategoryName = subCategory, 
                                categoryId = category_Id
                            )

            if productName == '':
                raise Exception("required field Empty")
            if brand == '':
                raise Exception("required field Empty")
            if category == '':
                raise Exception("required field Empty")
            if subCategory == '':
                raise Exception("required field Empty")
            if description == '':
                raise Exception("required field Empty")
            if videoUrl == '':
                raise Exception("required field Empty")

            checkUsr = request.user
            if checkUsr.groups.filter(name='Brand').exists():
                if brand != checkUsr.username:
                    raise Exception("forbidden")
            else:
                pass
            
            error = 2
            if checkChar (productName) == False:
                msg = 'Name cannot contain / , # , ?, \", and \' '
                raise Exception("forbidden")
            
            if len(productName) > 70:
                msg = 'Product Name has tobe less than or equal 70 characters'
                raise Exception("forbidden")

            if Product.objects.select_related('brandId').filter(productName=productName,brandId__brandName=brand_Id.brandName).first():
                msg = 'Product is already exist'
                raise Exception("forbidden")

            if checkYoutubeUrl (videoUrl) == False:
                msg = 'url not valid'
                raise Exception("forbidden")

            if len(description) < 75:
                msg = 'description need to be equal or more than 75 character'
                raise Exception("forbidden")

            product_obj = Product.objects.create(
                categoryId = category_Id,
                subCategoryId = subCategory_Id,
                brandId = brand_Id,
                productName = productName,
                description = description,
                videoUrl = videoUrl,
                dtm_crt = datetime.now()
            )

            product_obj.save()
            web_direct = 'success.html'

            return redirect ('addProductPicture', brand=brand_Id.brandName, productName=product_obj.productName)

        except Exception as e:
            print(e)
            if error == 1:
                context = {
                    'message': 'error'
                }
                return render(request,'error.html', context)
            else:
                messages.success(request, msg)
                form = ProductForm(request.POST)
                context = {
                    'form': form,
                    'category': ddCategory,
                    'subCategory': ddSubCategory,
                    'userPending': countUserPending(request),
                    'reportUser': countReport(request),
                }
                return render(request,'addProduct.html', context)

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def addEditProduct (request,context,productName,brand):
    error = 0
    error = None
    msg = None
    try:
        getProduct = Product.objects.select_related('brandId').get(
            brandId__brandName=brand,
            productName=productName)
        ddCategory = Category.objects.all()
        ddSubCategory = SubCategory.objects.all()
        product = getProduct

        if request.method != 'POST':
            form = ProductForm()
            context = {
                'form':form,
                'product': product,
                'category': ddCategory,
                'subCategory': ddSubCategory,
                'context': context,
                'userPending': countUserPending(request),
                'reportUser': countReport(request),
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

            if productName == '':
                raise Exception("required field Empty")
            if brand == '':
                raise Exception("required field Empty")
            if category == '':
                raise Exception("required field Empty")
            if subCategory == '':
                raise Exception("required field Empty")
            if description == '':
                raise Exception("required field Empty")
            if videoUrl == '':
                raise Exception("required field Empty")

            checkUsr = request.user
            if checkUsr.groups.filter(name='Brand').exists():
                if brand != checkUsr.username:
                    raise Exception("forbidden")
            else:
                pass
            
            error = 2
            if len(productName) > 70:
                msg = 'Product Name has tobe less than or equal 70 characters'
                raise Exception ("error")

            if checkChar (productName) == False:
                msg = 'Name cannot contain / , # , ?, \", and \' '
                raise Exception ("error")

            if checkYoutubeUrl (videoUrl) == False:
                msg = 'url not valid'
                raise Exception ("error")
            
            if len(description) < 75:
                msg = 'description need to be equal or more than 75 character'
                raise Exception ("error")
                

            getProduct.categoryId=category_Id
            getProduct.subCategoryId = subCategory_Id
            getProduct.brandId = brand_Id
            getProduct.productName = productName
            getProduct.description = description
            getProduct.videoUrl = videoUrl
            getProduct.dtm_upd = datetime.now()
            getProduct.save()

            if (context == "editAddProduct"):
                return redirect ('addProductPicture', brand=brand_Id.brandName, productName=getProduct.productName)
            elif (context == "editProductRating"):
                return redirect ('showProduct', brand=brand_Id.brandName, productName=getProduct.productName)
            elif (context == "editProductBrand"):
                return redirect ('brandPage', brandName=brand_Id.brandName, sort="By Date")
            
    except Exception as e:
        print(e)
        context = None
        if error == 0:            
            context = {
                'message': "product "+productName+" Not Found"
            }
        elif error == 1:
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)
        else:
            messages.success(request, msg)
            form = ProductForm(request.POST)
            context = {
                'form':form,
                'product': product,
                'category': ddCategory,
                'subCategory': ddSubCategory,
                'context': context,
                'userPending': countUserPending(request),
                'reportUser': countReport(request),
            }
            return render(request,'addProductEdit.html', context)

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def getJsonCategoryData (request):
    catValue = list(Category.objects.values().order_by('categoryName'))
    return JsonResponse ({
        'data':catValue 
    })

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def getJsonCategoryDataEdit (request,context,brand,productName):
    catValue = list(Category.objects.values().order_by('categoryName'))
    return JsonResponse ({
        'data':catValue 
    })

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def getJsonSubCategoryDataEdit (request,context,brand,productName, *args, **kwargs):
    selected_category = kwargs.get('cat')

    cat_Id = Category.objects.filter(
                    categoryName = selected_category
            ).values_list('categoryId', flat=True
            ).first()

    print(cat_Id)

    subCat_models = list(
        SubCategory.objects.filter(categoryId=cat_Id).values().order_by('subCategoryName')
    )

    return JsonResponse ({
        'data':subCat_models 
    })

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def getJsonSubCategoryData (request, *args, **kwargs):
    selected_category = kwargs.get('cat')

    cat_Id = Category.objects.filter(
                    categoryName = selected_category
            ).values_list('categoryId', flat=True
            ).first()

    print(cat_Id)

    subCat_models = list(
        SubCategory.objects.filter(categoryId=cat_Id).values().order_by('subCategoryName')
    )

    return JsonResponse ({
        'data':subCat_models 
    }) 

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def addEditPicture (request,productName,brand):
    web_direct = ''
    if request.method != 'POST':
        context = {
            'brand': brand,
            'productName': productName,
            'context':'',
            'title': 'Add Product Picture',
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
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

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def addEditPictureContext (request,productName,brand,context):
    web_direct = ''
    if request.method != 'POST':
        context = {
            'brand': brand,
            'productName': productName,
            'context':context,
            'title': 'Edit Product Picture: ' + productName,
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
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

@login_required
@allowed_users(allowed_roles=['Admin','Brand'])
def deleteProduct (request,productName,brand,context):
    error = 0
    try:
        product = Product.objects.select_related('brandId').get(productName=productName,brandId__brandName=brand) #
        userAuth = request.user
        
        if userAuth.groups.filter(name='Brand').exists():
            if userAuth.username != product.brandId.brandName:
                return HttpResponse('You are not allowed to view this page')
            else:
                pass

        if os.path.exists(product.productIMG.name):
            os.remove(product.productIMG.name)
        else:
            pass
    
        product.delete()

        if (context == "editProductRating"):
            return redirect ('dashboard')
        elif (context == "editProductBrand"):
            return redirect ('brandPage', brandName=brand, sort="By Date")

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
@allowed_users(allowed_roles=['Admin'])
def editorChoice(request):
    if request.method != 'POST':
        topList = []
        with connection.cursor() as cursor:
            raw_sql ="""            
                        SELECT
                            r.productId_id, FORMAT(AVG(r.rating), 1)'avg_score'
                        FROM review_review as r
                        GROUP BY r.productId_id
                        ORDER BY avg_score DESC;
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                topList.append(qux[0])
        
        productList = Product.objects.select_related('brandId').filter(productId__in=topList)[:10]
        precontext = []
        for i in range(len(productList)):
            precontext.append([productList[i],EditorForm(initial={'imageActive':productList[i].editorChoice},prefix=productList[i].productId)])
        context = {
            'data': precontext,
            'userPending': countUserPending(request),
            'reportUser': countReport(request)
        }
        return render(request,'editorChoice.html',context)
    else:
        
        oldChoice = Product.objects.filter(editorChoice=True)
        for choice in oldChoice:
            choice.editorChoice = False
            choice.save()

        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue
            id = key.split('-')
            product = Product.objects.get(productId=int(id[0]))
            product.editorChoice = True
            product.save()
        messages.success(request, 'Editor choice(s) successfully saved!')
        return redirect('editorchoice')

def showProduct (request, productName, brand):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    error = 1
    try:
        user_review = Review.objects.select_related('userID','productId').order_by('-helpful').filter(userID__roleId="Reg_User",productId__productName=productName)[:4]
        ms_review = Review.objects.select_related('userID','productId').order_by('-helpful').filter(userID__roleId="Mus_Store",productId__productName=productName)[:4]
        obj = Product.objects.select_related('brandId').get(productName = productName, brandId__brandName=brand)

        error = 2
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

        otherProduct = Product.objects.order_by('-avgScore')[:10]

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
            'reportUser': countReport(request),
            'otherProduct': otherProduct,
            'showMore': ''
        }

        return render(request,'rating.html', context)
    except Exception as e:
        print(e)
        context = None

        if error == 1:
            context = {
                'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
            }
        else:
            context = {
                'message': "error"
            }

        return render(request,'error.html', context)

def showMoreReview (request, productName, brand, showMore):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    error = 1
    try:

        obj = Product.objects.select_related('brandId').get(productName = productName, brandId__brandName=brand)

        error = 2
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
            reviewList = Review.objects.select_related('userID','productId').order_by('-helpful').filter(userID__roleId="Mus_Store",productId__productName=productName) 
        else:
            reviewList = Review.objects.select_related('userID','productId').order_by('-helpful').filter(userID__roleId="Reg_User",productId__productName=productName)
        
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
            'reportUser': countReport(request),
            'otherProduct': otherProduct,
            'showMore': showMore,
            'next_page_url': next_url,
            'prev_page_url': prev_url
        }

        return render(request,'rating.html', context)
    except Exception as e:
        print(e)
        context = None
        if error == 1:
            context = {
                'message': "Product \""+ productName +"\" from brand \""+ brand +"\" Not Found"
            }
        else:
            context = {
                'message': "error"
            }

        return render(request,'error.html', context)

def viewProductByCategory(request, categoryName):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    productList = None    
    sort = request.GET.get('sort', 'rate')
    if sort == 'rate':
        productList = Product.objects.order_by('-avgScore').select_related('categoryId','brandId').filter(categoryId__categoryName=categoryName)
    else:
        productList = Product.objects.order_by('-dtm_crt').select_related('categoryId','brandId').filter(categoryId__categoryName=categoryName)

    getProductListByPage = None
    if productList:
        paginator = Paginator(productList,12)
        page_number = request.GET.get('page', 1)
        getProductListByPage = paginator.get_page(page_number)

        if getProductListByPage.has_next():
            next_url = getProductListByPage.next_page_number()
        else:
            next_url = ''

        if getProductListByPage.has_previous():
            prev_url = getProductListByPage.previous_page_number()
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
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }
    return render(request,'productListByCategory.html', context)

def hotItems(request):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    productList = Product.objects.select_related('brandId').order_by('-visitCount')[:16]   

    getProductListByPage = None
    if productList:
        paginator = Paginator(productList,12)
        page_number = request.GET.get('page', 1)
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
        
    context={
        'productList': getProductListByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }
    return render(request,'hotProducts.html', context)

def viewProductBySubCategory(request, categoryName, subCategoryName):
    error = 0
    try:

        productList = None    
        sort = request.GET.get('sort', 'rate')
        if sort == 'rate':
            productList = Product.objects.order_by('-avgScore').select_related('subCategoryId','brandId').filter(subCategoryId__subCategoryName=subCategoryName,categoryId__categoryName=categoryName)
        else:
            productList = Product.objects.order_by('-dtm_crt').select_related('subCategoryId','brandId').filter(subCategoryId__subCategoryName=subCategoryName,categoryId__categoryName=categoryName)

        
        SubCategory.objects.select_related('categoryId').get(subCategoryName=subCategoryName,categoryId__categoryName=categoryName)
        error = 1
        
        getProductListByPage = None
        if productList:
            paginator = Paginator(productList,12)
            page_number = request.GET.get('page', 1)
            getProductListByPage = paginator.get_page(page_number)

            if getProductListByPage.has_next():
                next_url = getProductListByPage.next_page_number()
            else:
                next_url = ''

            if getProductListByPage.has_previous():
                prev_url = getProductListByPage.previous_page_number()
            else:
                prev_url = ''
        else: 
            getProductListByPage = Product.objects.none()
            next_url = ''
            prev_url = ''        
        
        
        context={
            'productList': getProductListByPage,
            'categoryName': categoryName,
            'subCategoryName': subCategoryName,
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
            'next_page_url': next_url,
            'prev_page_url': prev_url
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

def checkYoutubeUrl (videoUrl):
    url1 = "youtube"
    url2 = "youtu.be"
    url3 = "watch"

    value = False

    if url1 in videoUrl:
        value = True
    if url2 in videoUrl:
        value = True
    if url3 in videoUrl:
        value = True
    
    return value

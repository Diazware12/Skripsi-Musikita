from register.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from profileBrand.forms import AddBrandForm, InviteBrandForm, registerBrandForm
from Skripsi.decorator import allowed_users
from django.contrib.auth.decorators import login_required
from product.models import Category, Product, Brand
from django.shortcuts import redirect, render
from Skripsi.views import countReport, loginAccount, countUserPending, forgotPassword, numIndicator, sendMailAfterRegis, weakPassword
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User as auth_user
import requests
import uuid

# Create your views here.

def brandPage (request,brandName,sort):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)

    error = 0
    try:
        getBrand = Brand.objects.get(brandName = brandName)
        brandStatsData = []
        error = 1
        with connection.cursor() as cursor:
            raw_sql =""" 
							with  
                                stats as(
                                    select 
                                        (	
											select count(*) from product_product as p
											join product_brand as b on p.brandId_id = b.brandId
											where b.brandId = """+str(getBrand.brandId)+""" and p.avgScore <= 10 and p.avgScore >=8
                                        ) as positive,
                                        (
											select count(*) from product_product as p
											join product_brand as b on p.brandId_id = b.brandId
											where b.brandId = """+str(getBrand.brandId)+""" and p.avgScore < 8 and p.avgScore >=5
                                        ) as mixed,
                                        (
											select count(*) from product_product as p
											join product_brand as b on p.brandId_id = b.brandId
											where b.brandId = """+str(getBrand.brandId)+""" and p.avgScore < 5 and p.avgScore > 0
                                        ) as negative
                                        , b.brandName
										from product_product as p
										join product_brand as b on p.brandId_id = b.brandId
										where b.brandId = """+str(getBrand.brandId)+"""
                                ),
                                maxMin as( 
                                    select (select max(p.avgScore) from product_product as p
                                    join product_brand as b on p.brandId_id = b.brandId
                                    where b.brandId = """+str(getBrand.brandId)+"""
                                    having max(p.avgScore) > 0
                                    order by p.dtm_upd desc) as highRate,
                                    (
                                        select p.productName from product_product as p
										join product_brand as b on p.brandId_id = b.brandId
                                        where p.avgScore = (
											select max(p.avgScore) from product_product as p
											join product_brand as b on p.brandId_id = b.brandId
											where b.brandId = """+str(getBrand.brandId)+"""
											having max(p.avgScore) > 0
                                        ) and b.brandId = """+str(getBrand.brandId)+"""
                                        order by p.dtm_upd desc
                                        limit 1
                                    ) as highRateName,
                                    
									(select min(p.avgScore) from product_product as p
                                    join product_brand as b on p.brandId_id = b.brandId
                                    where b.brandId = """+str(getBrand.brandId)+"""
                                    having min(p.avgScore) > 0
                                    order by p.dtm_upd desc
                                    ) as minRate,
                                    (
                                        select p.productName from product_product as p
										join product_brand as b on p.brandId_id = b.brandId
                                        where p.avgScore = (
											select min(p.avgScore) from product_product as p
											join product_brand as b on p.brandId_id = b.brandId
											where b.brandId = """+str(getBrand.brandId)+"""
                                            having min(p.avgScore) > 0
                                        ) and b.brandId = """+str(getBrand.brandId)+"""
                                        order by p.dtm_upd desc
                                        limit 1
                                    ) as minRateName,
                                    b.brandName as brandName
									from product_product as p
									join product_brand as b on p.brandId_id = b.brandId
									where b.brandId = """+str(getBrand.brandId)+"""
                                )
                                select distinct (positive), mixed, negative, highRate, highRateName, minRate, minRateName
                                from stats join maxMin using (brandName)
                        """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                brandStatsData.append({
                    "positive": qux[0],
                    "mixed": qux[1],
                    "negative": qux[2],
                    "highestRate":numIndicator(str(qux[3])),
                    "highestRateName":qux[4],
                    "lowestRate":numIndicator(str(qux[5])),
                    "lowestRateName":qux[6]
                })    

        categoryList = []
        categoryList.append({"category": "By Date"})
        categoryList.append({"category": "By Rate"})

        error = 1
        with connection.cursor() as cursor:
            raw_sql =""" 
                        select distinct(c.categoryName) from product_product as p
                        join product_brand as b on p.brandId_id = b.brandId
                        join product_category as c on p.categoryId_id = c.categoryId
                        where b.brandId = """+str(getBrand.brandId)+"""
                    """            
            cursor.execute(raw_sql)

            for qux in cursor.fetchall():
                categoryList.append({
                    "category": qux[0]
                })    

        getProductFromSort = None
        if sort == "By Date":
            getProductFromSort = Product.objects.order_by('-dtm_crt').filter(brandId=getBrand)
        elif sort == "By Rate":
            getProductFromSort = Product.objects.order_by('-avgScore').filter(brandId=getBrand)
        else:
            getCategory = Category.objects.get(categoryName = sort)
            getProductFromSort = Product.objects.order_by('productName').filter(brandId=getBrand, categoryId=getCategory)

        getProductByPage = None
        if getProductFromSort:
            paginator = Paginator(getProductFromSort,4)
            page_number = request.GET.get('page', 1)
            getProductByPage = paginator.get_page(page_number)

            if getProductByPage.has_next():
                next_url = f'?page={getProductByPage.next_page_number()}'
            else:
                next_url = ''

            if getProductByPage.has_previous():
                prev_url = f'?page={getProductByPage.previous_page_number()}'
            else:
                prev_url = ''
        else:
            getProductByPage = Product.objects.none()
            next_url = ''
            prev_url = ''
        
        context = {
            'brandData': brandStatsData,
            'brand':getBrand,
            'userPending': countUserPending(request),
            'reportUser': countReport(request),
            'sortObj':getProductByPage,
            'categoryList': categoryList,
            'sort':sort,
            'next_page_url': next_url,
            'prev_page_url': prev_url
        }

        return render(request,'brandPage.html', context)

    except Exception as e:
        print(e)
        context = None
        if error == 0:
            context = {
                'message': "Brand "+ brandName +" Not Found"
            }
        else:
            context = {
                'message': 'error'
            }
        return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def brandControl (request):
    getAllBrand = Brand.objects.all()
    getAllBrandByPage = None
    if getAllBrand:
        paginator = Paginator(getAllBrand,4)
        page_number = request.GET.get('page', 1)
        getAllBrandByPage = paginator.get_page(page_number)

        if getAllBrandByPage.has_next():
            next_url = f'?page={getAllBrandByPage.next_page_number()}'
        else:
            next_url = ''

        if getAllBrandByPage.has_previous():
            prev_url = f'?page={getAllBrandByPage.previous_page_number()}'
        else:
            prev_url = ''
    else:
        getAllUsersByPage = Brand.objects.none()
        next_url = ''
        prev_url = ''

    context = {
        'obj':getAllBrandByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }

    return render(request,'brandcontrol.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def addBrand (request):
    if request.method != 'POST':
        regis_form = AddBrandForm()
        context = {
            'form': regis_form,
            'context': 'Add Brand'
        }
        return render(request,'addInviteRegisterBrand.html', context)
    else:
        brandName = request.POST.get('brandName')
        try:
            if brandName == '':
                raise Exception("required field Empty")
            if Brand.objects.filter(brandName = brandName).first():
                messages.success(request, 'Brand Name is Taken')
                return redirect ('addBrand')
            
            brand_obj = Brand.objects.create(
                brandName = brandName,
                status = 'No_User'
            )
            brand_obj.save()

            return redirect ('brandcontrol')
        except Exception as e:
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def inviteBrand (request):
    if request.method != 'POST':
        inviteForm = InviteBrandForm()
        context = {
            'form': inviteForm,
            'context': 'Invite Brand'
        }
        return render(request,'addInviteRegisterBrand.html', context)
    else:
        brandName = request.POST.get('brandName')
        email = request.POST.get('email')
        message = request.POST.get('message')
        brandData = []
        try:
            if brandName == '':
                raise Exception("required field Empty")
            if email == '':
                raise Exception("required field Empty")
            if message == '':
                raise Exception("required field Empty")

            brand_obj = Brand.objects.get(brandName = brandName)
            if brand_obj.status != 'No_User':
                messages.success(request, 'Brand is Already receive email / have account ')
                return redirect ('inviteBrand')
            
            token = str (uuid.uuid4())
            brandData.append(email)
            brandData.append(token)

            domain = get_current_site(request).domain
            sendMailAfterRegis (domain, brandData, 'brand_invitation',message)

            brand_obj.status = 'user_verif'
            brand_obj.auth_token = token
            brand_obj.save()
            

            return redirect ('brandcontrol')
        except Exception as e:
            context = {
                'message': 'error'
            }
            return render(request,'error.html', context)


def registerBrand (request,auth_token):
    try:
        getBrand = Brand.objects.get(auth_token = auth_token)
        if request.method != 'POST':
            registerForm = registerBrandForm()
            context = {
                'form': registerForm,
                'context': "Register Brand :"+getBrand.brandName+""
            }
            return render(request,'addInviteRegisterBrand.html', context)
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_pass = request.POST.get('confirm_pass')
            brandWebsiteUrl = request.POST.get('brandWebsiteUrl')
            description = request.POST.get('description')

            if email == '':
                raise Exception("required field Empty")
            if password == '':
                raise Exception("required field Empty")
            if confirm_pass == '':
                raise Exception("required field Empty")

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is Taken')
                return redirect ('registerBrand', auth_token=auth_token)
            check_pass = weakPassword (password)
            if check_pass != 'True':
                messages.success(request, check_pass)
                return redirect ('registerBrand', auth_token=auth_token)

            if (confirm_pass != password):
                messages.success(request, 'confirm password should be same as password')
                return redirect ('registerBrand', auth_token=auth_token)

            req = requests.head(brandWebsiteUrl)
            if req.status_code == 404:
                messages.success(request, 'Url\'s not valid')
                return redirect ('registerBrand', auth_token=auth_token)

            getBrand.brandURL = brandWebsiteUrl
            getBrand.description = description
            getBrand.brandEmail = email
            getBrand.status = 'Verified'
            getBrand.save()

            userAuth = auth_user.objects.create(
                username = getBrand.brandName,
                email = getBrand.brandEmail,
                password = make_password(password) 
            )
            
            userAuth.save()

            getgroupId = Group.objects.get(name = 'Brand')

            userAuth.groups.add(getgroupId)

            return redirect ('dashboard')

    except Exception as e:
        context = {
            'message': 'error'
        }
        return render(request,'error.html', context)

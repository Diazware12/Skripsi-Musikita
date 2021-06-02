from product.models import Category, Product, Brand
from django.shortcuts import render
from Skripsi.views import loginAccount, countUserPending, forgotPassword, numIndicator
from django.db import connection
from django.core.paginator import Paginator

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

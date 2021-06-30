from advancesearch.filters import productFilters
from advancesearch.forms import ProductFilterForm
from django.http.response import JsonResponse
from django.shortcuts import render
from product.models import Category, Product, SubCategory
from django.core.paginator import Paginator
from Skripsi.views import countReport, loginAccount, countUserPending, forgotPassword

def advanceSearch (request):
    isLogin = request.POST.get('isLogin')
    isForgotPass = request.POST.get('isForgotPassword')
    # isFilter = request.POST.get('IsFilter')

    new_var = None
    if request.method == 'POST' and isLogin == "1":
        loginAccount (request)
    elif request.method == 'POST' and isForgotPass == "1":
        forgotPassword (request)


    new_var = productFilters(
        request.GET,
        Product.objects.all()
    )

    productName = None

    if 'productName' in request.GET:
        productName = request.GET['productName']
    else:
        productName = ''    

    if new_var:
        paginator = Paginator(new_var.qs,8)
        page_number = request.GET.get('page',1)
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
        'productName': productName,
        'filter': new_var,
        'productList': getProductListByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }

    return render (request,'productList.html',context)


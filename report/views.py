from register.forms import RejectionReason
from review.views import updateReviewAvg
from register.models import User
from django.contrib.sites.shortcuts import get_current_site
from product.models import Product
from Skripsi.decorator import allowed_users
from django.contrib.auth.decorators import login_required
from Skripsi.views import countReport, countUserPending, sendMail
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from review.models import Report, Review
from django.db import connection
from django.core.paginator import Paginator

@login_required
@allowed_users(allowed_roles=['Admin'])
def reportList (request):
    reportUserList = []
    with connection.cursor() as cursor:
        raw_sql =""" 
                    select u.userName, rev.title, p.productName, b.brandName, rev.dtm_crt, rev.rating from review_report as rep
                    join review_review as rev on rev.reviewId = rep.reviewId_id
                    join product_product as p on rev.productId_id = p.productId
                    join product_brand as b on p.brandId_id = b.brandId
                    join register_user as u on rev.userID_id = u.userID
                    group by rep.reviewId_id
                """            
        cursor.execute(raw_sql)

        for qux in cursor.fetchall():
            reportUserList.append({
                'userName': qux[0],
                'reviewTitle': qux[1],
                'productName': qux[2],
                'productBrand': qux[3],
                'dtm_crt': qux[4],
                'ratingReview': qux[5]
            })
    
    getReportListByPage = None
    if reportUserList:
        paginator = Paginator(reportUserList,4)
        page_number = request.GET.get('page', 1)
        getReportListByPage = paginator.get_page(page_number)

        if getReportListByPage.has_next():
            next_url = f'?page={getReportListByPage.next_page_number()}'
        else:
            next_url = ''

            if getReportListByPage.has_previous():
                prev_url = f'?page={getReportListByPage.previous_page_number()}'
            else:
                prev_url = ''
    else:
        getReportListByPage = None
        next_url = ''
        prev_url = ''

    context = {
        'obj':getReportListByPage,
        'userPending': countUserPending(request),
        'reportUser': countReport(request),
        'next_page_url': next_url,
        'prev_page_url': prev_url
    }

    return render(request,'reportList.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def reportListView (request, user_select, brand, productName):
    try:
        getProduct = Product.objects.select_related(
                            'brandId').get(
                            productName = productName,
                            brandId__brandName = brand)

        obj = Review.objects.select_related('userID').get(
                    productId = getProduct.productId,
                    userID__userName = user_select
                )

        getReportReason = Report.objects.select_related('reviewId').filter(
                            reviewId__reviewId = obj.reviewId
                          ).values('reason').distinct()

        getReportData = Report.objects.select_related('reviewId','userID').filter(
                            reviewId__reviewId = obj.reviewId)
        
        context = { 
            'obj': obj,
            'brand': brand,
            'productName': productName,
            'reportReasonList': getReportReason,
            'reportData':getReportData,
            'reportUser': countReport(request),
            'userPending': countUserPending(request)
        }   

        return render(request,'reportListView.html', context)

    except Exception as e:
        print(e)
        context = { 
            'message': 'error'
        }   
        return render(request,'error.html', context)

def approveReport (request, user_select, brand, productName):
    try:
        getProduct = Product.objects.select_related(
                            'brandId').get(
                            productName = productName,
                            brandId__brandName = brand)

        obj = Review.objects.select_related('userID').get(
                    productId = getProduct.productId,
                    userID__userName = user_select
                )
        
        getReportReason = Report.objects.select_related('reviewId').filter(
                            reviewId__reviewId = obj.reviewId
                          ).values('reason').distinct()

        getReasonArray = []

        i = 0
        while i < len(getReportReason):
            getReasonArray.append(getReportReason[i]['reason'])
            i += 1
        
        reason = ""
        for item in getReasonArray:
            reason += '- ' + item +'\n'
        
        domain = get_current_site(request).domain
        message =""" 
                    hi """+user_select+""",
                    we like to inform you about your review with a title \" """+obj.title+""" \"
                    in """+getProduct.productName+""", has been reported due to: \n
                    """+reason+"""
                    \n
                    thank you
                    http://"""+domain+"""
                """    
        getUser = User.objects.get(userName = user_select)
        sendMail (domain, getUser, 'approve_report',message)

        obj.delete()
        updateReviewAvg(getProduct)

        return redirect('reportList')
    except Exception as e:
        print(e)
        context = { 
            'message': 'error'
        }   
        return render(request,'error.html', context)

def rejectReport (request, user_select, brand, productName):
    try:
        if request.method != 'POST':
            rejectionForm = RejectionReason()
            context = {
                'form': rejectionForm,
                'userPending': countUserPending(request)
            }
            return render(request,'rejectionReason.html', context)
        else :
            rejectionReason = request.POST.get('reason')

            getProduct = Product.objects.select_related(
                            'brandId').get(
                            productName = productName,
                            brandId__brandName = brand)

            obj = Review.objects.select_related('userID').get(
                        productId = getProduct.productId,
                        userID__userName = user_select
                    )
        
            getReportReviewData = Report.objects.select_related('reviewId','userID').filter(
                                reviewId__reviewId = obj.reviewId
                            )

            getUserEmailList = []

            for email in getReportReviewData:
                getUserEmailList.append(email.userID.email)


            domain = get_current_site(request).domain
            message =""" 
                        Hello Users!!,
                        Unfortunately your review report about \" """+obj.title+""" \" from """+user_select+"""
                        in """+getProduct.productName+""", has been rejected by admin because:\n\n
                        """+rejectionReason+"""
                        \n\n
                        thank you
                        http://"""+domain+"""
                    """    
            getUser = User.objects.get(userName = user_select)
            sendMail (domain, getUserEmailList, 'reject_report',message)

            getReportReviewData.delete()
            
            return redirect('reportList')

    except Exception as e:
        print(e)
        context = { 
            'message': 'error'
        }   
        return render(request,'error.html', context)

    return 'success'
        









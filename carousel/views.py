from django.contrib import messages
from carousel.forms import CarouselForm
from carousel.models import CarouselImage
from Skripsi.decorator import allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
@allowed_users(allowed_roles=['Admin'])
def manageCarousel(request):
    if request.method != 'POST':
        carousels = CarouselImage.objects.all()
        precontext = []
        for i in range(len(carousels)):
            precontext.append([carousels[i],CarouselForm(initial={'imageActive':carousels[i].status}, prefix=i+1)])
        context = {
            'data': precontext,
        }
        return render(request,'manageCarousel.html',context)
    else:
        carousels = CarouselImage.objects.all()
        checkCount = 0
        for i in range(len(carousels)):
            name = str(i+1)+"-imageActive"
            if request.POST.get(name) != None:
                checkCount += 1
                if checkCount > 3:
                    messages.success(request, 'cannot put more than 3 carousels')
                    return redirect('managecarousel')
                carousels[i].status = True
            else:
                carousels[i].status = False
        for i in range(len(carousels)):
            carousels[i].save()
        return redirect('managecarousel')
        
@login_required
@allowed_users(allowed_roles=['Admin'])
def addCarousel(request):
    carouselForm = [CarouselForm(initial={'imageActive':var.status}) for var in carousels]

    context = {
        'carouselForm': carouselForm
    }
    return render(request,'manageCarousel.html',context)

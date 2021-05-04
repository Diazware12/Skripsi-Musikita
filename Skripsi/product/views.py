from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm

def addProduct (request):
    cum = ProductForm()
    context = {
        'form': cum
    }
    return render(request,'addProduct.html', context)

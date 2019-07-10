from django.http import HttpResponse
from pal_app.models import Product
from django.shortcuts import render

# Create your views here.


def show_products(request):
    product_list = Product.objects.all()
    context = {'product_list': product_list}
    return render(request, 'pal_app/index.html', context)


def add_product(request):
    try:
        product_name = request.POST['product_name']
        calories = request.POST['calories']
        pn = Product(name=product_name, calories=calories)
        pn.save()
    except KeyError:
        return render(request, 'pal_app/add_product.html')
    return render(request, 'pal_app/add_product.html', {
        'debug': "dodawanie przebieglo pomyslnie"
    })

from pal_app.models import Product, User
from django.shortcuts import render, redirect


def show_products(request):
    product_list = Product.objects.all()
    context = {'product_list': product_list}
    return render(request, 'pal_app/products-list.html', context)


def add_product(request):
    try:
        product_name = request.POST['product_name']
        calories = request.POST['calories']
        pn = Product(name=product_name, calories=calories)
        pn.save()
    except KeyError:
        return render(request, 'pal_app/add-product.html')
    return render(request, 'pal_app/add-product.html', {
        'debug': "dodawanie przebieglo pomyslnie"
    })


def main(request):
    if User.objects.count() == 0:
        response = redirect('/user-data')
    else:
        response = render(request, 'pal_app/fitness-app.html')
    return response


def user_data(request):
    try:
        user_name = request.POST['user_name']
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        sex = request.POST['sex'] == 'm'
        ud = User(user_name=user_name, height=height, weight=weight, age=age, sex=sex)
        ud.save()
    except KeyError:
        return render(request, 'pal_app/user-data.html')
    return render(request, 'pal_app/user-data.html', {
        'debug': "dodawanie przebieglo pomyslnie"
    })

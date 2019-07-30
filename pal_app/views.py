import datetime

from django.db.models import DateField

from pal_app.models import Product, User, MealChoice, Meal
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


def meal_data(request, meal_type):
    context = {}
    product_list = Product.objects.all()
    context['product_list'] = product_list

    try:
        result = MealChoice(meal_type)
        context['meal_name'] = result.name
        context['meal_id'] = meal_type
    except ValueError:
        return redirect('/')
    try:
        if request.method == "POST":
            selected = request.POST.getlist("products")
            meal = Meal.objects.create(meal_type=meal_type)
            for product in selected:
                meal.products.add(product)
    except KeyError:
        return render(request, 'pal_app/meal-data.html', context)
    return render(request, 'pal_app/meal-data.html', context)

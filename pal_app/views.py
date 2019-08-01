import datetime

from django.core.exceptions import ObjectDoesNotExist
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


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def calc_intake():
    pass


def calc_meal(meal_type):
    value = 0
    try:
        meal = Meal.objects.get(meal_type=meal_type.value, day=today())
        for product in meal.products.all():
            value += product.calories
    except ObjectDoesNotExist:
        pass
    return value


def main(request):
    if User.objects.count() == 0:
        response = redirect('/user-data')
    else:
        obj = User.objects.first()
        goal = 0
        calories_left = 0
        todays_intake = 0
        meal_cal = {}
        for meal_type in MealChoice:
            meal_cal[meal_type] = calc_meal(meal_type)
            todays_intake += meal_cal[meal_type]
        print(meal_cal)
        context = {'user': obj,
                   'date': today(),
                   'goal': goal,
                   'calories_left': goal - todays_intake,
                   'cal_of_meals': meal_cal
                   }
        response = render(request, 'pal_app/fitness-app.html', context)
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
        meal = Meal.objects.get(meal_type=meal_type, day=today())
        context['selected'] = meal.products.all()
        print(context['selected'])
        print(product_list)
    except ObjectDoesNotExist:
        try:
            meal = Meal.objects.create(meal_type=meal_type)
            meal.save()
        except ValueError:
            return redirect('/')
    try:
        result = MealChoice(meal_type)
        context['meal_name'] = result.name
        context['meal_id'] = meal_type
        if request.method == "POST":
            selected = request.POST.getlist("products")
            meal.products.set([])
            for product in selected:
                meal.products.add(product)
            return redirect('/')
    except KeyError:
        return render(request, 'pal_app/meal-data.html', context)
    return render(request, 'pal_app/meal-data.html', context)

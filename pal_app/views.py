import datetime
from django.core.exceptions import ObjectDoesNotExist
from pal_app.models import Product, User, MealChoice, Meal, MealProducts
from django.shortcuts import render, redirect
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def show_products(request):
    product_list = Product.objects.all().order_by('name')
    context = {'product_list': product_list}
    return render(request, 'pal_app/products-list.html', context)


def add_product(request):
    try:
        product_name = request.POST['product_name']
        calories = request.POST['calories']
        Product(name=product_name, calories=calories).save()
    except KeyError:
        return render(request, 'pal_app/add-product.html')
    return render(request, 'pal_app/add-product.html', {
        'debug': "Successfully added to database."
    })


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def age(born):
    current_date = datetime.date.today()
    return current_date.year - born.year - ((current_date.month, current_date.day) < (born.month, born.day))


def calc_intake():
    user = User.objects.first()
    if user.sex:
        BMR = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * age(user.age))
    else:
        BMR = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * age(user.age))
    cal = BMR
    return int(cal)


def calc_meal(meal_type):
    value = 0
    try:
        meal = Meal.objects.get(meal_type=meal_type.value, day=today())
        for product in meal.products.all():
            a = MealProducts.objects.get(meal=meal, product=product)
            value += product.calories * a.amount / 100
    except ObjectDoesNotExist:
        pass
    return int(value)


def delete_user(request):
    User.objects.first().delete()
    Meal.objects.filter(day=today()).delete()
    return redirect('/')


def main(request):
    if User.objects.count() == 0:
        response = redirect('/user-data')
    else:
        obj = User.objects.first()
        goal = calc_intake()
        today_intake = 0
        meal_cal = {}
        for meal_type in MealChoice:
            meal_cal[meal_type] = calc_meal(meal_type)
            today_intake += meal_cal[meal_type]
        context = {'user': obj,
                   'date': today(),
                   'goal': goal,
                   'calories_left': int(goal - today_intake),
                   'cal_of_meals': meal_cal,
                   'intake': today_intake
                   }
        response = render(request, 'pal_app/fitness-app.html', context)
    return response


def remove_product(request, product_id):
    Product.objects.get(id=product_id).delete()
    return redirect('/products')


def user_data(request):
    msg = ""
    try:
        user_name = request.POST['user_name']
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        sex = request.POST['sex'] == 'm'
        if User.objects.count() == 0:
            ud = User(user_name=user_name, height=height, weight=weight, age=age, sex=sex)
            msg = "Welcome to FitnessApp!"
        else:
            ud = User.objects.first()
            ud.user_name = user_name
            ud.height = height
            ud.weight = weight
            ud.age = age
            ud.sex = sex
            msg = "Successfully updated your data."
        ud.save()
    except KeyError:
        if User.objects.count() > 0:
            ud = User.objects.first()
            return render(request, 'pal_app/user-data.html', {
                'user': ud})
    return render(request, 'pal_app/user-data.html', {
        'debug': msg
    })


def meal_data(request, meal_type):
    context = {}
    product_list = Product.objects.all()
    context['product_list'] = product_list
    try:
        meal = Meal.objects.get(meal_type=meal_type, day=today())
        context['selected'] = meal.products.all()

        amount_dict = {}
        for meal_product in MealProducts.objects.filter(meal=meal):
            amount_dict[meal_product.product.id] = str(meal_product.amount)
        context['amounts'] = amount_dict
    except ObjectDoesNotExist:
        try:
            meal = Meal.objects.create(meal_type=meal_type)
            meal.save()
        except ValueError:
            return redirect('/')
    try:
        result = MealChoice(meal_type)
        # FIXME: Pass only result, on template side get result.name / result.value?
        context['meal_name'] = result.name
        context['meal_id'] = meal_type
        if request.method == "POST":
            selected = request.POST.getlist("products")
            meal = Meal.objects.get(meal_type=meal_type, day=today())
            MealProducts.objects.filter(meal=meal).delete()
            for product in selected:
                amount = request.POST['input_calories_' + str(product)]
                if not amount:
                    amount = 100
                MealProducts.objects.create(product=next(x for x in product_list if x.id == int(product)),
                                            meal=meal,
                                            amount=amount)
            return redirect('/')
    except KeyError:
        return render(request, 'pal_app/meal-data.html', context)
    return render(request, 'pal_app/meal-data.html', context)

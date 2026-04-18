from http.cookiejar import debug
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from unicodedata import category
from django.utils.crypto import get_random_string
from .models import *
from django.http import HttpResponse, request
from django.core.mail import send_mail
from .forms import *
from .forms import CategoryForm
from sampleapp.models import Category, SubCategory
from django.db.models import Sum, Q
import razorpay
from django.contrib import messages
from django.db.models import F



def index(request):
    categories = Category.objects.all()
    sub_categories=SubCategory.objects.all()
    subsubcategories = Subsubcategory.objects.all()
    total_quantity = 0
    user = request.session.get('user')
    if user:
        u = get_object_or_404(signup, username=user)
        total_quantity = cart.objects.filter(user_details=u).aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'index.html', {'categories': categories, 'total_quantity': total_quantity, 'sub_categories':sub_categories, 'subsubcategories':subsubcategories})


def users(request):
    if request.method == 'POST':
        a=request.POST['n1']
        b=request.POST['n2']
        c=request.POST['n3']
        d=request.POST['n4']
        e=request.POST['n5']
        f=request.POST['n6']
        if signup.objects.filter(username=d).exists():
           return HttpResponse("Username already exists")
        if e==f:
           signup.objects.create(name=a,phone=b,email=c,username=d,password=e).save()
           return HttpResponse('Saved')
        else:
           return HttpResponse('Passwords do not match')
    else:
        return render(request, 'register.html')


def login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['n4']
        password = request.POST['n5']
        try:
            data=signup.objects.get(username=username)
            if data.password == password:
                request.session['user']=username
                return redirect(user)
            else:
                return HttpResponse('wrong password')
        except Exception as e:
            if 'admin' == username and password == '1234':

                request.session['admin']=username
                return redirect(adminhome)
            else:
                return HttpResponse('Incorrect username and wrong password')

    return render(request, 'login.html', {'categories':categories})


def delivery_login(request):
    if request.method =='POST':
        a = request.POST['n1']
        b = request.POST['n2']
        data=signup.objects.get(username=a)
        if data.password==b:
            if data.status == 'Accepted':
                request.session['delivery']=a
                messages.success(request,'Login success')
                return redirect(delivery_home)
            else:
                messages.error(request,'Request Pending')
                return redirect(login)
        else:
            messages.error(request, 'Incorect password')
            return redirect(login)
    return render(request, 'delivery_boy_login.html')


def logout(request):
    if 'user' in request.session or 'admin' in request.session  or 'delivery' in request.session:
        request.session.flush()

        return redirect(login)


def adminhome(request):
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    subsubcategories = Subsubcategory.objects.all()

    admin = request.session.get('admin')
    if not admin:
        return redirect('login')


    out_stock_products = product.objects.filter(product_quantity=0)
    low_stock_products = product.objects.filter(
        product_quantity__lte=5,
        product_quantity__gt=0
    )

    return render(request, 'adminhome.html', {
        'categories': categories,
        'sub_categories': sub_categories,
        'subsubcategories': subsubcategories,
        'out_stock_products': out_stock_products,
        'low_stock_products': low_stock_products,
    })


def user(request):
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    subsubcategories=Subsubcategory.objects.all()
    if 'user' in request.session:
        username = request.session.get('user')

        return render(request, 'userhome.html', {'categories': categories, 'sub_categories':sub_categories, 'subsubcategories':subsubcategories})
    else:
        return redirect(login)

# def Add_Product(request):
#     p = normal()
#     categories = Category.objects.all()
#     subcategories = SubCategory.objects.all()
#     if request.method == 'POST':
#        p = normal(request.POST, request.FILES)
#        if p.is_valid():
#           a = p.cleaned_data['product_name']
#           b = p.cleaned_data['product_price']
#           c = p.cleaned_data['product_quantity']
#           d = p.cleaned_data['product_image']
#           cat_id = request.POST.get('categories')
#           sub_id = request.POST.get('subcategories')
#           e = Category.objects.get(id=cat_id)
#           subcategory_obj = SubCategory.objects.get(id=sub_id)
#
#           product.objects.create(product_name=a, product_price=b, product_quantity=c, image=d, category=e,sub_category=subcategory_obj).save()
#           print(e)
#           return HttpResponse("saved")
#     else:
#           return render(request, 'Add_Product.html', {'categories':categories,'subcategories': subcategories,'data':p})
#     return render(request, 'Add_Product.html')

# def Add_Product(request):
#     username = request.session.get('user')
#
#     if not username:
#       return redirect(login)
#     p = normal()
#     category = Category.objects.all()
#     subcategory = SubCategory.objects.all()
#
#     if request.method == 'POST':
#         p = normal(request.POST, request.FILES)
#         if p.is_valid():
#             a = p.cleaned_data['product_name']
#             b = p.cleaned_data['product_price']
#             c = p.cleaned_data['product_quantity']
#             d = p.cleaned_data['product_image']
#
#             hair_type = p.cleaned_data.get('hair_type')
#             hair_color = p.cleaned_data.get('hair_color')
#             skin_type = p.cleaned_data.get('skin_type')
#
#             cat_id = request.POST.get('category')
#             sub_id = request.POST.get('subcategory')
#
#             if not cat_id or not sub_id:
#                 return HttpResponse("Please select both category and subcategory!")
#
#             try:
#                 category_obj = Category.objects.get(id=cat_id)
#             except Category.DoesNotExist:
#                 return HttpResponse("Selected category does not exist!")
#
#             try:
#                 subcategory_obj = SubCategory.objects.get(id=sub_id)
#             except SubCategory.DoesNotExist:
#                 return HttpResponse("Selected subcategory does not exist!")
#
#             product.objects.create(
#                 product_name=a,
#                 product_price=b,
#                 product_quantity=c,
#                 image=d,
#                 category=category_obj,
#                 sub_category=subcategory_obj,
#                 hair_type = hair_type,
#                 hair_color = hair_color,
#                 skin_type = skin_type
#
#             )
#             return HttpResponse("Product saved!")
#
#     return render(request, 'Add_Product.html', {
#         'category': category,
#         'subcategory': subcategory,
#         'data': p
#     })




def Add_Product(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    subsubcategories = Subsubcategory.objects.all()
    p = normal()

    if request.method == 'POST':
        p = normal(request.POST, request.FILES)
        if p.is_valid():

            product_name = p.cleaned_data['product_name']
            product_price = p.cleaned_data['product_price']
            product_quantity = p.cleaned_data['product_quantity']
            product_image = p.cleaned_data['product_image']
            hair_type = p.cleaned_data.get('hair_type')
            hair_color = p.cleaned_data.get('hair_color')
            description = p.cleaned_data.get('description')


            cat_id = request.POST.get('category')
            sub_id = request.POST.get('subcategory')
            sub_sub_id = request.POST.get('subsubcategory')

            if not cat_id or not sub_id:
                return HttpResponse("Please select both category and subcategory!")

            try:
                category_obj = Category.objects.get(id=cat_id)
            except Category.DoesNotExist:
                return HttpResponse("Selected category does not exist!")

            try:
                subcategory_obj = SubCategory.objects.get(id=sub_id)
            except SubCategory.DoesNotExist:
                return HttpResponse("Selected subcategory does not exist!")
            try:
                subsubcategory_obj = Subsubcategory.objects.get(id=sub_sub_id)
            except SubCategory.DoesNotExist:
                return HttpResponse("Selected subsubcategory does not exit")

            product.objects.create(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity,
                image=product_image,
                category=category_obj,
                sub_category=subcategory_obj,
                sub_sub_category=subsubcategory_obj,
                hair_type=hair_type,
                hair_color=hair_color,
                description=description
            )
            return HttpResponse("Product saved successfully!")

        else:

            print(p.errors)
            return HttpResponse(f"Form errors: {p.errors}")

    return render(request, 'Add_Product.html', {
        'category': categories,
        'subcategory': subcategories,
        'subsubcategory':subsubcategories,
        'data': p,
        'categories':categories,
        'subcategories':subcategories,
        'subsubcategories':subsubcategories,
    })


def normalform(request):
    n=normal()
    if request.method == 'POST':
        n=normal(request.POST, request.FILES)
        if n.is_valid():
            a=n.cleaned_data['product_name']
            b=n.cleaned_data['product_price']
            c=n.cleaned_data['product_quantity']
            d=n.cleaned_data['product_image']
            product.objects.create(product_name=a,product_price=b,product_quantity=c,image=d).save()
            return HttpResponse("saved")
    else:
        return render(request, 'forms.html', {'data':n})


def modelform(request):
    m=modelform()
    if request.method == 'POST':
        m=modelform(request.POST,request.FILES)
        if m.is_valid():
            m.save()
            return HttpResponse("saved")
    return render(request, 'forms.html', {'data':m})


# def products(request, category_id=None):
#     username = request.session.get('user')
#     if not username:
#         return redirect('login')
#     categories = Category.objects.all()
#     if category_id:
#         category = get_object_or_404(Category, id=category_id)
#         if category:
#
#            data = product.objects.filter(category=category)
#         else:
#            sub=SubCategory.objects.filter(id=category_id).first()
#            if sub:
#               data=product.objects.filter(subcategory=sub)
#     else:
#         data = product.objects.all()
#         category = None
#
#     return render(request, 'product.html', {'data': data, 'category': category, 'categories':categories})

# def products(request, category_id=None):
#     username=request.session.get('user')
#     if not username:
#         return redirect('login')
#     categories = Category.objects.all()
#     query = request.GET.get('q')
#     data=product.objects.all()
#     category = None
#
#     if category_id:
#         category = Category.objects.filter(id=category_id).first()
#         if category:
#             data=data.filter(category=category)
#         else:
#             sub=SubCategory.objects.filter(id=category_id).first()
#             if sub:
#                 data.filter(subcategory=sub)
#
#
#     if query:
#         data=data.filter(Q(product_name__icontains=query) |
#     Q(description__icontains=query) | Q(product_price__icontains=query))
#     return render(request, 'product.html', {
#         'data': data,
#         'category': category,
#         'categories': categories,
#         'query': query
#     })

from django.db.models import Q, F
from django.shortcuts import render, redirect

def products(request, category_id=None):
    username = request.session.get('user')
    if not username:
        return redirect('login')

    categories = Category.objects.all()
    query = request.GET.get('q')
    data = product.objects.all()
    category = None


    if request.method == "POST":
        product_id = request.POST.get('product_id')
        qty = int(request.POST.get('quantity', 1))

        if product_id:
            updated = product.objects.filter(
                id=product_id,
                product_quantity__gte=qty
            ).update(
                product_quantity=F('product_quantity') - qty
            )

            if updated:
                return redirect(request.path)
            else:
                return render(request, 'product.html', {
                    'data': data,
                    'categories': categories,
                    'error': "Not enough stock"
                })


    if category_id:
        category = Category.objects.filter(id=category_id).first()
        if category:
            data = data.filter(category=category)
        else:
            sub = SubCategory.objects.filter(id=category_id).first()
            if sub:
                data = data.filter(subcategory=sub)


    if query:
        data = data.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'product.html', {
        'data': data,
        'category': category,
        'categories': categories,
        'query': query
    })

def search(request):
    query = request.GET.get('q')
    results = product.objects.filter(product_name__icontains=query)
    return render(request, 'search.html', {'results': results})


# def product_detail(request, pk):
#     item = get_object_or_404(product, pk=pk)
#     return render(request, 'product_detail.html', {'item': item})





def product_detail(request, pk):
    item = get_object_or_404(product, pk=pk)
    message = None

    if request.method == "POST":
        qty = int(request.POST.get("quantity"))

        updated = product.objects.filter(
            pk=pk,
            product_quantity__gte=qty
        ).update(product_quantity=F('product_quantity') - qty)

        if updated:
            item.refresh_from_db()
            message = "Purchase successful"
        else:
            message = "Not enough stock"

    return render(request, 'product_detail.html', {
        'item': item,
        'message': message
    })
def category(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Category.objects.filter(name=name).exists():
                return HttpResponse("Category already exists!")
            else:
                form.save()
                return redirect('category')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(request, 'category.html', {'form': form, 'categories': categories})

def sub_category(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    if request.method == 'POST':
        n = sub_categoryForm(request.POST)
        if n.is_valid():
            name = n.cleaned_data['name']

            if SubCategory.objects.filter(name=name).exists():
                return HttpResponse("sub_category already exists!")
            else:
                n.save()
                return redirect('sub_category')
    else:
        n = sub_categoryForm()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, 'Sub_category.html', {'n': n, 'categories': categories,'sub_categories': subcategories})

# def sub_sub_category(request):
#     if request.method == 'POST':
#         m=sub_sub_categoryForm(request.POST)
#         if m.is_valid():
#             name = m.cleaned_data['name']
#             if Subsubcategory.category.filter(name=name, subcategory=n.cleaned_data['subcategory']):
#                 return  HttpResponse("Subsubcategory already exists!")
#             else:
#                 m.save()
#     else:
#         m=sub_sub_categoryForm()
#     categories = Category.objects.all()
#     subcategories = SubCategory.objects.all()
#     subsubcategories = Subsubcategory.objects.all()
#     return render(request, 'sub_sub_category.html', {'m': m, 'categories': categories, 'sub_categories':subcategories, 'sub_sub_category': subsubcategories})

def sub_sub_category(request, d):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    if request.method == 'POST':
        form = sub_sub_categoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subcategory = form.cleaned_data['subcategory']

            if Subsubcategory.objects.filter(name=name, subcategory=subcategory).exists():
                return HttpResponse("Subsubcategory already exists!")
            else:
                form.save()
                return redirect('sub_sub_category', d=d)
        else:

            categories = Category.objects.all()
            subcategories = SubCategory.objects.all()
            subsubcategories = Subsubcategory.objects.all()

            return render(request, 'sub_sub_category.html', {
                'm': form,
                'categories': categories,
                'sub_categories': subcategories,
                'sub_sub_category': subsubcategories
            })

    else:
        form = sub_sub_categoryForm()

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    subsubcategories = Subsubcategory.objects.all()

    return render(request, 'sub_sub_category.html', {
        'm': form,
        'categories': categories,
        'sub_categories': subcategories,
        'sub_sub_category': subsubcategories
    })


def products_by_sub(request, sub_id):
    username = request.session.get('user')
    if not username:
        return redirect('login')

    categories = Category.objects.all()
    subcategory = get_object_or_404(SubCategory, id=sub_id)
    data = product.objects.filter(sub_category=subcategory)

    return render(request, 'product.html', {
        'data': data,
        'subcategory': subcategory,
        'categories': categories
    })

def product_by_subsub(request,d):
    username=request.session.get('user')
    if not username:
        return redirect('login')

    subcategories = SubCategory.objects.all()
    subsubcategories = get_object_or_404(Subsubcategory, id=d)
    data = product.objects.filter(sub_sub_category=subsubcategories)
    return render(request, 'product.html', {'subcategories':subcategories, 'subsubcategories':subsubcategories, 'data': data})
def Manage_Product(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    data=product.objects.all()
    return render(request,'Manage_Product.html', {'data':data})

def update(request, d):
    p=product.objects.get(pk=d)
    data=model_form(instance=p)
    if request.method == 'POST':
        m = model_form(request.POST, request.FILES, instance=p)
        if m.is_valid():
            m.save()
            return redirect(Manage_Product)
    return render(request, 'update.html', {'data':data})

def delete(request, d):
    product.objects.get(pk=d).delete()
    return redirect(Manage_Product)


# def add_cart(request, d):
#     if 'user' in request.session:
#         prod=product.objects.get(pk=d)
#         u=signup.objects.get(username=request.session['user'])
#         if cart.objects.filter(product_details=prod).exists():
#             p=cart.objects.get(product_details=prod)
#             p.quantity+=1
#             p.total_price = p.product_details.product_price * p.quantity
#             p.save()
#             return redirect(view_cart)
#         else:
#             cart.objects.create(product_details=prod, user_details=u, total_price=prod.product_price).save()
#             return redirect(view_cart)
#     else:
#         return redirect(view_cart)


def add_cart(request, d):
    if 'user' not in request.session:
        return redirect(login)

    prod = product.objects.get(pk=d)
    u = signup.objects.get(username=request.session['user'])

    item, created = cart.objects.get_or_create(
        product_details=prod,
        user_details=u,
        defaults={
            'quantity': 1,
            'total_price': prod.product_price
        }
    )

    if not created:
        item.quantity += 1
        item.total_price = item.quantity * prod.product_price
        item.save()

    return redirect(view_cart)


# def view_cart(request):
#     print("view_cart")
#     user = request.session.get('user')
#     if not user:
#         return redirect(login)
#
#     u=signup.objects.get(username=request.session['user'])
#     data=cart.objects.filter(user_details=u)
#     print(data)
#     total=0
#     total_quantity=0
#     for i in data:
#         if i.product_details.product_quantity < i.quantity:
#             return HttpResponse("Not enough stock")
#         total_quantity += i.quantity
#         total += i.total_price
#     return render(request,'cart.html',{'data':data, 'total':total, 'total_quantity':total_quantity})

def view_cart(request):
    user = request.session.get('user')
    if not user:
        return redirect(login)

    u = get_object_or_404(signup, username=user)
    data = cart.objects.filter(user_details=u).select_related('product_details')

    total = 0
    total_quantity = 0
    messages = []

    for i in data:
        stock = i.product_details.product_quantity
        if i.quantity > stock:
            i.quantity = stock
            i.total_price = stock * i.product_details.product_price
            i.save()
            messages.append(f"{i.product_details.product_name} quantity adjusted to available stock")

        total_quantity += i.quantity
        total += i.quantity * i.product_details.product_price

    return render(request, 'cart.html', {
        'data': data,
        'total': total,
        'total_quantity': total_quantity,
        'messages': messages
    })


    for i in data:
        a = i.product_details

        if a.product_quantity < i.quantity:
            return HttpResponse("Not enough stock")

        a.product_quantity -= i.product_quantity
        print(a.product_quantity)
        a.save()



# def decrement(request, d):
#     p=cart.objects.get(pk=d)
#     p.quantity-=1
#     if p.quantity < 1:
#         p.delete()
#     else:
#         p.total_price = p.product_details.product_price * p.quantity
#         p.save()
#     return redirect(view_cart)


def decrement(request, d):
    u = signup.objects.get(username=request.session['user'])
    p = cart.objects.get(pk=d, user_details=u)
    if p.quantity > 1:
        p.quantity -= 1
        p.total_price = p.quantity * p.product_details.product_price
        p.save()
    else:
        p.delete()
    return redirect(view_cart)

def increment(request,d):
    p=cart.objects.get(pk=d)
    p.quantity+=1
    p.total_price = p.product_details.product_price * p.quantity
    p.save()
    return redirect(view_cart)

# def payment(request, d):
#     amount = d*100
#     order_currency = 'INR'
#     client = razorpay.Client(
#     auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
#     # cursor = connection.cursor()
#     # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")
#     payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#     return render(request, "payment.html",{'amount':amount,'d':d, 'order': order,
#     'user': user})
def payment(request, d):
    amount = int(d) * 100  # convert to paise

    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM")
    )

    order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1
    })

    # If you are using session user
    username = request.session.get('user')
    user = signup.objects.get(username=username)

    return render(request, "payment.html", {
        'amount': amount,
        'd': d,
        'order': order,
        'user': user
    })

# def address(request):
#
#     user=signup.objects.get(username=request.session['user'])
#     if request.method=='POST':
#        a=request.POST['n1']
#        b=request.POST['n2']
#        c=request.POST['n3']
#        d=request.POST['n4']
#        e=request.POST['n5']
#        f=request.POST['n6']
#        g=request.POST['n7']
#        a(username=a,phone=b,email=c,pin=d,state=e,city=f,building_name=f,road_name=g).save()
#        messages.success(request, 'Address Added successfully')
#        return redirect(order_sum)
#     return render(request, 'address.html', {'user': user})




# def address(request):
#     user = signup.objects.get(username=request.session['user'])
#     if not user:
#         return redirect(login)
#     if request.method == 'POST':
#         x=request.POST['x1']
#         y=request.POST['x2']
#         z=request.POST['x3']
#         a = request.POST['x4']
#         b = request.POST['x5']
#         c = request.POST['x6']
#         d = request.POST['x7']
#         e = request.POST['x8']
#         user.name=x
#         user.email=y
#         user.phone=z
#         user.pincode=a
#         user.state=b
#         user.city=c
#         user.building_name=d
#         user.road_name=e
#         user.save()
#         messages.success(request,'Address Added successfully')
#         return redirect('login')
#     re
#     turn render(request,'address.html',{'user':user})

def address(request):
    try:
        user = signup.objects.get(username=request.session.get('user'))

    except signup.DoesNotExist:
        return redirect(login)

    if request.method == 'POST':
        user.name = request.POST.get('x1')
        user.email = request.POST.get('x2')
        user.phone = request.POST.get('x3')
        user.pincode = request.POST.get('x4')
        user.state = request.POST.get('x5')
        user.city = request.POST.get('x6')
        user.building_name = request.POST.get('x7')
        user.road_name = request.POST.get('x8')

        user.save()
        return redirect(order_sum)


    return render(request, 'address.html', {'user': user})

def order_sum(request):
    try:
        user = signup.objects.get(username=request.session.get('user'))
    except signup.DoesNotExist:
        return redirect(login)
    data=cart.objects.filter(user_details=user)
    total = 0
    quantity = 0
    for i in data:
        total += i.total_price
        quantity += 1
    return render(request, 'order_summary.html', {'data': data, 'total': total, 'quantity': quantity,'user':user })


# def order(request):
#     username = request.session.get('user')
#
#     if not username:
#         return redirect(login)  # prevent crash
#
#     user = signup.objects.get(username=username)
#     data = cart.objects.filter(user_details=user)
#     import datetime
#     import datetime
#     d = datetime.datetime.now()
#     for i in data:
#         a = i.product_details
#         a.quantity=a.product_quantity-i.quantity
#         print(a.quantity)
#         a.save()
#         orders.objects.create(user_details=user,product_details=a,quantity=i.quantity,amount=i.total_price,order_date=d).save()
#     data.delete()
#     return render(request,"success.html")

# def order(request):
#     username = request.session.get('user')
#
#     if not username:
#         return redirect(login)
#
#     user = signup.objects.get(username=username)
#     data = cart.objects.filter(user_details=user)
#
#     from django.utils import timezone
#     d = timezone.now()
#
#
#
#     orders.objects.create(user_details=user,product_details=i.product,quantity=i.product_quantity,amount=i.total_price,order_date=d)
#
#     data.delete()
#
#     return render(request, "success.html")
#

def profile(request):
    data = delivery_boy_register.objects.get(username=request.session['delivery'])
    return render(request,'profile.html',{'data':data})



def order(request):

    username = request.session.get('user')
    if not username:
        return redirect('login')

    user = signup.objects.get(username=username)
    cart_items = cart.objects.filter(user_details=user)

    if not cart_items.exists():
        return render(request, "payment.html")

    current_time = timezone.now()


    order_list = [
        orders(
            user_details=user,
            product_details=item.product_details,
            quantity=item.quantity,
            amount=item.total_price,
            order_date=current_time
        )
        for item in cart_items
    ]


    orders.objects.bulk_create(order_list)
    cart_items.delete()

    return render(request, "success.html")




def myorder(request):
    username = request.session.get('user')
    if not username:
        return redirect('login')
    user = signup.objects.get(username=username)
    data = orders.objects.filter(user_details=user)
    return render(request,'myorders.html',{'data':data})

def wish(request,d):
    pro = product.objects.get(pk=d)
    if wishlist.objects.filter(product_details=pro).exists():
        messages.error(request,'Item Already Added To Wishlist')
        return redirect(products)
    else:
        user=signup.objects.get(username=request.session['user'])
        wishlist.objects.create(user_details=user,product_details=pro).save()
        messages.success(request,'Item Added To Your Wishlist')
        return redirect(products)
def wish_view(request):
    user=request.session.get('user')
    if not user:
        return redirect(login)
    user = signup.objects.get(username=request.session['user'])
    data = wishlist.objects.filter(user_details=user)
    return render(request,'wishlist.html',{'data':data})

def delivery_reg(request):
    if request.method == 'POST':
        a = request.POST['z1']
        b = request.POST['z2']
        c = request.POST['z3']
        d = request.POST['z4']
        e = request.POST['z5']
        f = request.POST['z6']
        g = request.POST['z7']

        if delivery_boy_register.objects.filter(username=e).exists():
            return HttpResponse('Username Already Exist')
        elif delivery_boy_register.objects.filter(email=b).exists():
            return HttpResponse('Email Already Exist')
        else:
            delivery_boy_register.objects.create(name=a, email=b, phone=c, driving_license_no=d, username=e, password=f).save()
            return HttpResponse('Register Successfully')
            return render(request,'delivery_boy_register.html')
    return render(request,'delivery_boy_register.html')

def delivery_login(request):
    if request.method =='POST':
        a = request.POST['z5']
        b = request.POST['z6']
        data=delivery_boy_register.objects.get(username=a)
        if data.password==b:
            if data.status == 'Accepted':
                request.session['delivery']=a
                return redirect(delivery_home)

            else:
                return HttpResponse(request,'Request Pending')

        else:
            return HttpResponse('Incorect password')

    return render(request, 'delivery_boy_login.html')

def delivery_home(request):

    return render(request, 'delivery_home.html',)



def booking(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    data = orders.objects.all()
    deliver=delivery_boy_register.objects.filter(work_status='Free',status='Accepted')
    return render(request,'booking.html',{'data':data,'deliver':deliver})


def delivery_view(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    data = delivery_boy_register.objects.all()
    return render(request, 'delivery_views.html', {'data': data})
def reject(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status='Rejected'
    data.save()
    return redirect(delivery_view)
def accept(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status = 'Accepted'
    data.save()
    return redirect(delivery_view)
def delivered(request,a):
    data = orders.objects.get(pk=a)
    data.product_status ='Delivered'
    data.save()
    delivery=delivery_boy_register.objects.get(username=request.session['delivery'])
    delivery.work_status='Free'
    delivery.save()
    messages.success(request,'You Have delivered the order.now you are Free')
    return redirect(delivery_order)


def choose(request,a):
    if request.method =='POST':
        b = request.POST['x1']
        data = orders.objects.get(pk=a)
        data.delivery_boy=b
        data.product_status='Out for delivery'
        data.save()
        try:
            d=delivery_boy_register.objects.get(username=b)
            d.work_status='Busy'
            d.save()
            # return redirect(booking)
        except Exception as e:
            print(e)
            messages.error(request,'Delivery Boy Doesnot Exist')
            return redirect(booking)
        messages.success(request,f'The order has been assigned for {b}')
        return redirect(booking)

def delivery_order(request):
    if 'delivery' in request.session:
        data=orders.objects.filter(delivery_boy=request.session['delivery'])
        return render(request,'delivery_orders.html',{'data':data})
    else:
        return redirect(login)




#
# def category_products(request, id):
#
#     category = get_object_or_404(Category, id=id)
#
#
#     products = product.objects.filter(category=category)
#
#     context = {
#         'category': category,
#         'products': products
#     }
#     return render(request, 'product.html', context)



def rem(request,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cart_view)


# def remo(request,d):
#     data=wishlist.objects.get(pk=d)
#     data.delete()
#     return redirect(wish_view)

def remo(request, d):
    username = request.session.get('user')
    if not username:
        messages.error(request, "You need to log in first!")
        return redirect('login')

    user = get_object_or_404(signup, username=username)
    item = get_object_or_404(wishlist, pk=d, user_details=user)
    item.delete()
    messages.success(request, "Item removed from your wishlist.")
    return redirect(wish_view)

def history(request):
    user = delivery_boy_register.objects.get(username=request.session['delivery'])
    data = orders.objects.filter(product_status='Delivered',delivery_boy=user.username)
    return render(request,'order_history.html',{'data':data})

from django.conf import settings
from django.utils.crypto import get_random_string

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()

        print("Entered:", email)
        print("DB emails:", list(signup.objects.values_list('email', flat=True)))

        users = signup.objects.filter(email__iexact=email)

        if not users.exists():
            messages.info(request, "Email id not registered")
            return redirect('forgot_password')

        user = users.first()

        token = get_random_string(length=32)   # ✅ strong token

        PasswordReset.objects.create(user_details=user, token=token)

        reset_link = f'http://127.0.0.1:8000/reset/{token}/'

        try:
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,   # ✅ FIXED
                [user.email],               # better than [email]
                fail_silently=False
            )
        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.info(request, f"Error: {e}")
            return redirect('forgot_password')
            return redirect('forgot_password')

        messages.success(request, "Reset link sent successfully")

    return render(request, 'forgot.html')

def reset_password(request, token):
    print("RESET VIEW CALLED")

    try:
        password_reset = PasswordReset.objects.get(token=token)
        user = password_reset.user_details
        print("USER FOUND:", user)
    except PasswordReset.DoesNotExist:
        print("INVALID TOKEN")
        return redirect('forgot_password')

    if request.method == 'POST':
        print("POST REQUEST RECEIVED")

        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')

        print("New:", new_password)
        print("Confirm:", repeat_password)

        if not new_password or not repeat_password:
            print("EMPTY PASSWORD FIELD")
            return HttpResponse("Empty password")

        if new_password != repeat_password:
            print("PASSWORD MISMATCH")
            return HttpResponse("Passwords do not match")

        # ✅ SAVE PASSWORD (your model = plain text)
        user.password = new_password
        user.save()

        print("PASSWORD SAVED IN DATABASE")

        return redirect('login')

    return render(request, 'reset.html')


# def reset_password(request, token):
#     try:
#         password_reset = PasswordReset.objects.get(token=token)
#         user = password_reset.user_details
#     except PasswordReset.DoesNotExist:
#         return redirect('forgot_password')
#
#     if request.method == 'POST':
#         new_password = request.POST.get('newpassword')
#         repeat_password = request.POST.get('cpassword')
#
#         if new_password != repeat_password:
#             return HttpResponse("Passwords do not match")
#
#         # ✅ FIX HERE
#         user.password = new_password
#         user.save()
#
#         return redirect('login')
#
#     return render(request, 'reset.html')

# def reset_password(request,token):
#     print(token)
#     password_reset = PasswordReset.objects.get(token=token)
#     if request.method == 'POST':
#         new_password = request.POST.get('newpassword')
#         repeat_password = request.POST.get('cpassword')
#         if repeat_password == new_password:
#
#             return redirect(login)
#     return render(request, 'reset.html', {'token': token})
def alert(request):
    low_stock_products = product.objects.filter(product_quantity__lt=5)
    return render(request, "alert.html", {'low_stock_products':low_stock_products})
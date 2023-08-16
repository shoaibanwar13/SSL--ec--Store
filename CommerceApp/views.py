from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from CommerceApp.models import Products,category,OrderItem,Order,Review,Contact,User
from CommerceApp.cart import Cart
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.conf import settings
import stripe
from django.core.mail import EmailMessage
from django.http import JsonResponse
import json
import requests
from django.template.loader import render_to_string

def frontpage(request):
    products=Products.objects.all()
    ip_address=request.META.get('REMOTE_ADDR', '')
    print(ip_address)
    url=f'https://vpnapi.io/api/64.145.93.117?key=7552caea9d4344f6aeb5dccbe6418f69'
    res=requests.get(url)
    result=res.json()
    vpn_value=result["security"]["vpn"]
    city=result["location"]["city"]
    country=result["location"]["country"]
    continent=result["location"]["continent"]
    network=result["network"]["network"]
    autonomous_system_organization=result["network"]["autonomous_system_organization"]
    print(vpn_value)
    print(city)
    print(continent)
    print(country)
    print(network)
    print(autonomous_system_organization)
    context={
        'products':products,
        'city':city,
        'country':country,
        'continent':continent,
        'network':network,
        'autonomous_system_organization':autonomous_system_organization



    }
    #if vpn_value==True:
            
            #return redirect('Thankyou')

   
    return render(request,'frontpage.html',context)
def product(request,id):
    
    products=Products.objects.filter(id=id).first()
    views=Review.objects.all()
    

    context={'products':products,'views':views}
   
    
    

    
    return render(request,'product.html',context)
def feedback(request):
    return render(request,'feedback.html')
def Reviews(request):
    if request.method=="GET":
        product_name=request.GET.get("product_name")
        name=request.GET.get("name")
        rat=request.GET.get("rating")
        comment=request.GET.get("content")
        query=Review( product_name= product_name,rating=rat,content=comment,name=name)
        query.save()
        return redirect('feedback')

    return render(request,'product.html')

def shop(request):
    categories = category.objects.all()
    products = Products.objects.all()
    


    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }
    return render(request,'shop.html',context)
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return render(request, 'menu_cart.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})
@login_required
def cart(request):
    return render(request,'cart.html')

def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)
    
    product = Products.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    
    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response

def hx_menu_cart(request):
    return render(request, 'menu_cart.html')
def hx_cart_total(request):
    return render(request, 'total_cart.html')
@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE 
    return render(request,'checkout.html',{'pub_key':pub_key})
@login_required
def myaccount(request):
    return render(request,'myaccount.html')
@login_required
def edit_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('myaccount')
    return render(request,'edit_myaccount.html')
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")
        phone=request.POST.get("phone")
        myquery=Contact(name=name,email=email,message=message,phone=phone)
        myquery.save()
        return redirect('Thankyou')
       
    
    return render(request,"Contact.html")

def Thankyou(request):
    return render(request,'Thankyou.html')
def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        obj = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': total_price,
            },
            'quantity': item['quantity']
        }

        items.append(obj)
    
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/fail'
    )
    payment_intent = session.payment_intent

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    phone = data['phone']

    order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, zipcode=zipcode, place=place)
    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.paid = True
    order.save()
    email_subject=" SSL Tec Store Order Conformation"
    message=render_to_string('SendEmail.html',{
            'first_name':first_name,
            'total_bill':total_price,
            'Thanks':'Thanks for Purchasing! Your Product Have been delivered Within 5Working Days',

        })
    email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
    email_message.send()

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity
        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})

def success(request):
    return render(request,'success.html')

def fail(request):
    return render(request,'fail.html')
def SendEmail(request):
    return render(request,'Invoice.html')






# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .cart import Cart
from django.urls import reverse
from main.models import Product, Order, OrderItem
from django.http import JsonResponse
import uuid
from decimal import Decimal
from django.http import JsonResponse
# Create your views here.
from .telegram import main
import asyncio
from telegram import Bot
import requests


from django.http import HttpResponse, FileResponse
import tempfile
def cart_summary(request):
    cart = Cart(request)
    cart_prods = cart.get_product()
    prod_count = cart.get_quantity()
    product_count = request.POST.get('prod_count')
    product_id = request.POST.get('product_id')
    get_product_total = cart.get_total_price()
    total = cart.get_total()
    data = {
        'cart_prods': cart_prods,
        'prod_count': prod_count,
        'total': total,
    }
    return render(request,'main/shopping-cart.html', context=data)

def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action')=='post':
        product_id = request.POST.get('product_id')
        
        product_count = int(request.POST.get('prod_count'))
        
        product = get_object_or_404(Product, id=product_id)
        
        
        
        cart.add(product=product, quantity=product_count)
        cart_items = cart.__len__()
     
        
        return JsonResponse({"cart_items": cart_items, 'Quantity': cart_items})
    return render(request,'main/index.html')

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        cart.delete(product_id= product_id)
        
        return JsonResponse({"status": 'success'})
def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_count = int(request.POST.get('prod_count'))
        
        cart.update(product=product_id, quantity=product_count)
        
        
        return JsonResponse({'quantity':product_count})
    
    
    

def order_details(request):
    cart = Cart(request)
    all_info = cart.get_all_info()

    if request.user.id is None:
        return HttpResponseRedirect(reverse('login'))
        
    else:
        order = Order()
        order.user_id = request.user
        order.order_id = uuid.uuid4()
        order.total_price = cart.get_total()
        
        order.save()
        
        for info in all_info:
            order_item = OrderItem(
                order = order, 
                product_id = info['id'],
                name = info['name'],
                price = Decimal(info['price']),
                quantity = int(info['quantity']),
                
            )    
            order_item.save()
        
        
        cart.cart_clear()
        
        
        message = "Новый заказ:\n"
        for info in all_info:
            message += f"Id: {info['id']}\n"
            message += f"Имя: {info['name']}\n"
            message += f"Цена: {info['price']}\n"
            message += f"Количество: {info['quantity']}\n\n"
        asyncio.run(main(message))
        # return HttpResponseRedirect(reverse('index'))
        cart.cart_clear()
        
        receipt_file = create_receipt(all_info)
        with open(receipt_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=order_receipt.txt'
            return response
    

def create_receipt(order_info):
    with tempfile.NamedTemporaryFile(delete=False, mode='w+') as file:
        file.write("Новый заказ:\n")
        for info in order_info:
            file.write(f"Id: {info['id']}\n")
            file.write(f"Имя: {info['name']}\n")
            file.write(f"Цена: {info['price']}\n")
            file.write(f"Количество: {info['quantity']}\n\n")
        file_path = file.name
    print("Receipt created successfully!")
    return file_path
    
    




@login_required
def order_info(request):
    orders = Order.objects.filter(user_id=request.user)
    total = 0
    result = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        order_total = sum(item.price * item.quantity for item in order_items)
        total += order_total
        data = {'order':order.order_id, 'items':order_items, 'order_total':order_total}
        result.append(data)
    data = {
        'orders': result,
        'total': total

    }
        
    
    return render(request, 'main/checkout.html', context=data)






from django.shortcuts import render
from .models import *
from math import ceil
import json
from django.http import HttpResponse
# Create your views here.
def main(request):
    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds }
    return render(request,"app/main.html", params)


def store(request):
    return render(request, 'app/store.html')

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()

        update= OrderUpdate(order_id= order.order_id, update_desc="The order has been placed")
        update.save()

        thank=True
        id=order.order_id
        return render(request, 'app/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'app/checkout.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        desc= request.POST.get('desc','')
        print(name,email,phone, desc )
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'app/contact.html')

def about(request):
    if request.method == 'POST':
        
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        return HttpResponse(f"{orderId} and {email}")


    return render(request, 'app/about.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'app/tracker.html')


    return render(request, 'app/tracker.html')

def search(request):
    return render(request, 'app/search.html')

def basic(request):
    return render(request, 'app/basic.html')

def productView(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "app/productView.html", {'product':product[0]})


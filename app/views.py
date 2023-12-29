from django.shortcuts import render
from .models import *
from math import ceil
import json
from django.http import HttpResponse

# Create your views here.
def main(request):
    # products= Product.objects.all()
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
        amount = request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
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
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'app/tracker.html')

def searchMatch(query, item):
     if query in item.desc.lower() or query in item.product_name or query in item.category:
        return True
     else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request,"app/main.html", params)

def basic(request):
    return render(request, 'app/basic.html')

def productView(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "app/productView.html", {'product':product[0]})


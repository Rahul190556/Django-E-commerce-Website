from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from app.models import Customer,Product,Cart,OrderPlaced,CATEGORY_CHOICES
from app.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q 
from django.http import JsonResponse

# for current user use simply request.user


def SearchView(request):
    query = request.GET['query']
    if len(query) > 78 or len(query) == 0:
        allProduct = Product.objects.none()
    else:
        allProduct_title = Product.objects.filter(title__icontains=query)
        allProduct_brand = Product.objects.filter(brand__icontains=query)
        allProduct_category = Product.objects.filter(category__in=[category[0]
        for category in CATEGORY_CHOICES if query.lower() in category[1].lower()])

        allProduct = allProduct_title.union(allProduct_brand).union(allProduct_category)

    if allProduct.count() == 0:
        messages.error(request, "No products found for the given query.")

    parameter = {'allProduct': allProduct, 'query': query}
    return render(request, 'app/search.html', parameter)




class ProductView(View):
    def get(self,request):
     total_item=0
     topwears=Product.objects.filter(category='TW')
     bottomwears=Product.objects.filter(category='BW')
     mobiles=Product.objects.filter(category='M')
     if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
     return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears ,'mobiles':mobiles ,'total_item':total_item})


class ProductDetailView(View):
    def get(self,request,pk):
     total_item=0
     product=Product.objects.get(pk=pk)
     item_already_in_cart=False
     if request.user.is_authenticated:
      item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
      total_item=len(Cart.objects.filter(user=request.user))
     return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,
                                                     'total_item':total_item})

@login_required
def add_to_cart(request):
  user=request.user
  product_id=request.GET.get('prod_id')
  product=Product.objects.get(id=product_id)
  Cart(user=user,product=product).save()
  return redirect('/cart')

@login_required
def show_cart(request):
   if request.user.is_authenticated:
      total_item=0
      user=request.user
      carts=Cart.objects.filter(user=user)
      amount=0.0
      shipping_amount=75.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user == request.user]
      if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
      if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
        totalamount=amount + shipping_amount
        return render(request,'app/addtocart.html',{'carts':carts,'totalamount':totalamount,'amount':amount
                                                    ,'total_item':total_item})
      else:
         return render(request,'app/emptycart.html')
      
def Plus_cart(request):
   if request.method == 'GET':
      prod_id=request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount=0.0
      shipping_amount=75.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
      totalamount=amount + shipping_amount

      data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

      }
      return JsonResponse(data)
def Minus_cart(request):
   if request.method == 'GET':
      prod_id=request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      if(c.quantity > 0):
        c.quantity-=1
      c.save()
      amount=0.0
      shipping_amount=75.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
      totalamount=amount + shipping_amount

      data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

      }
      return JsonResponse(data)

def Remove_cart(request):
   if request.method == 'GET':
      total_item=0
      prod_id=request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount=0.0
      shipping_amount=75.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
      totalamount=amount + shipping_amount
      if request.user.is_authenticated:
       total_item=len(Cart.objects.filter(user=request.user))

      data={
            'amount':amount,
            'totalamount':totalamount,
            'total_item':total_item

      }
      return JsonResponse(data)
   
   

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 total_item=0
 add=Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
  total_item=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','total_item':total_item})



def mobile(request,data=None):
    total_item=0
    if data == None:
        mobiles=Product.objects.filter(category='M')
        active='btn-primary'
    elif data=='Samsung' or data=='Redmi':
      mobiles=Product.objects.filter(category='M').filter(brand=data)
      active='btn-primary'
    elif data=='below':
      mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=12000)
      active='btn-primary'
    elif data=='above':
          mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=12000)
          active='btn-primary'
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))

    return render(request, 'app/mobile.html',{'mobiles':mobiles, 'total_item':total_item ,'active':active ,'data': data})

def laptop(request,data=None):
    total_item=0
    if data == None:
        laptops=Product.objects.filter(category='L')
        active='btn-primary'
    elif data=='ASUS' or data=='LENOVO':
      laptops=Product.objects.filter(category='L').filter(brand=data)
      active='btn-primary'
    elif data=='below':
      laptops=Product.objects.filter(category='L').filter(discounted_price__lt=60000)
      active='btn-primary'
    elif data=='above':
          laptops=Product.objects.filter(category='L').filter(discounted_price__gt=70000)
          active='btn-primary'
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))

    return render(request, 'app/laptop.html',{'laptops':laptops, 'total_item':total_item,'active':active,"data":data})

def topwear(request,data=None):
    total_item=0
    if data == None:
        topwears=Product.objects.filter(category='TW')
        active='btn-primary'
    elif data=='Duke' or data=='Levin':
      topwears=Product.objects.filter(category='TW').filter(brand=data)
      active='btn-primary'
    elif data=='below':
      topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=400)
      active='btn-primary'
    elif data=='above':
          topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=500)
          active='btn-primary'
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))

    return render(request, 'app/topwear.html',{'topwears':topwears, 'total_item':total_item,'active':active,"data":data})

def bottomwear(request,data=None):
    total_item=0
    if data == None:
        bottomwears=Product.objects.filter(category='BW')
        active='btn-primary'
    elif data=='Duke' or data=='Levin':
      bottomwears=Product.objects.filter(category='BW').filter(brand=data)
      active='btn-primary'
    elif data=='below':
      bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=300)
      active='btn-primary'
    elif data=='above':
          bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=400)
          active='btn-primary'
    if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
        

    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears, 'total_item':total_item,'active':active,"data":data})





class CustomerRegistrationView(View):
  def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
           messages.success(request,"Congratulation!! Registered Sucessfully")
           form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
  total_item=0
  user=request.user
  add= Customer.objects.filter(user=user)
  cart_items=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=75.0
  total_amount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
      tempamount=(p.quantity * p.product.discounted_price)
      amount+=tempamount
  totalamount=amount + shipping_amount
  if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
  return render(request,'app/checkout.html',
                {'totalamount':totalamount,'add':add,'cart_items':cart_items,'total_item':total_item})

@login_required
def payment_done(request):
   user=request.user
   custid=request.GET.get('custid')
   customer=Customer.objects.get(id=custid)
   cart=Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user,customer=customer,
      product=c.product,quantity=c.quantity).save()
      c.delete()
   return redirect('orders')

@login_required
def orders(request):
 total_item=0
 order_placed=OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'order_placed':order_placed,'total_item':total_item})

@method_decorator(login_required,name="dispatch")
class ProfileView(View):
   def get(self, request):
     total_item=0
     form=CustomerProfileForm()
     if request.user.is_authenticated:
        total_item=len(Cart.objects.filter(user=request.user))
     return render(request, 'app/profile.html',{'form':form ,'active':'btn-primary','total_item':total_item})
  #  post using cleaned_data
   def post(self,request):
      form=CustomerProfileForm(request.POST)
      if form.is_valid():
         usr=request.user
         name=form.cleaned_data['name']
         locality=form.cleaned_data['locality']
         city=form.cleaned_data['city']
         state=form.cleaned_data['state']
         zipcode=form.cleaned_data['zipcode']
         reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
         reg.save()
         messages.success(request,"Congratulation!! Profile Updated Successfully")
         return render(request, 'app/profile.html', {'form': form,'active':'btn-primary'})
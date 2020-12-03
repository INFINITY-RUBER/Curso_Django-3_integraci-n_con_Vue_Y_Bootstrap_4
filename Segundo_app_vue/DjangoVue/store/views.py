from django.http import request
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseNotFound

from taggit.models import Tag


import paypalrestsdk
# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersCreateRequest
# from paypalhttp import HttpError
import logging

from listelement.models import Element, Category
from .models import Payment, Coupon
from .forms import MessageForm, CouponForm


# Create your views here.

def index(request):

    search = request.GET.get('search') if request.GET.get('search') else ''
    category_id = request.GET.get('category_id')
    category_id = int(category_id) if category_id else ''

    tag_id = request.GET.get('tag_id')
    tag_id = int(tag_id) if tag_id else ''
 

    if search:
        elements = Element.objects.prefetch_related('elementimages_set').filter(title__contains=search)# __contains: para genera busqueda similar a SQL
        # print(search)
    else:
        elements = Element.objects.prefetch_related('elementimages_set')

    if category_id:
        elements = elements.filter(category_id = category_id)
        
    if tag_id:
        tag = get_object_or_404(Tag,id=tag_id)
        elements = elements.filter(tags__in = [tag])

        
    elements = elements.filter(type = 1)   
    paginator = Paginator(elements, 4)
    categories = Category.objects.all() # trae todas las categorias
    tags = Tag.objects.all() # trae todas las etiquetas



    page_number = request.GET.get('page')
    elements_page = paginator.get_page(page_number)

    return render(request, 'store/index.html', {'elements':elements_page, 
                                                'categories':categories, 
                                                'tags':tags,
                                                'search':search, 
                                                'category_id':category_id,
                                                'tag_id':tag_id
                                                })


def detail(request, url_clean, code=None):    
    # print(code)   
    # coupon = None
    # if code:
    #     coupon = get_valid_coupon(code)
    coupon = get_valid_coupon(code) if code else None
    msj_coupon = ''
    if (code == 'None' or coupon is None) and code is not None: # si el cupon es invalido
        msj_coupon = 'El cupón es inválido'
        code = ''           

    element = get_object_or_404(Element, url_clean=url_clean)
    messages = element.element_comments.filter(active=True)
    message_form = MessageForm(user=request.user)
    Coupon_form = CouponForm(initial={'element_id':element.id,'code':code})
    messages_new = None

       
    if request.method == 'POST':
        message_form = MessageForm(user=request.user,data=request.POST)
        if message_form.is_valid():
            messages_new = message_form.save(commit=False)
            messages_new.element = element
            if request.user.is_authenticated:
                messages_new.name = request.user.first_name
                messages_new.lastname = request.user.last_name
                messages_new.email = request.user.email
                messages_new.user = request.user
            messages_new.save()
            message_form = MessageForm(user=request.user)

                    

    return render(request, 'store/detail.html',{'element':element,
                                                'message_form': message_form ,
                                                'messages_new': messages_new,
                                                'messages': messages,
                                                'Coupon_form': Coupon_form,
                                                'coupon': coupon,
                                                'msj_coupon': msj_coupon                                                
                                                })



@require_POST
def coupon_apply(request):

    form = CouponForm(request.POST)
    coupon=None
    
    if form.is_valid():
        code = form.cleaned_data['code']
        elementId = form.cleaned_data['element_id']

    try:
        couponModel = get_valid_coupon(code)
        if couponModel:
            coupon = couponModel.code
    except Coupon.DoesNotExist:
        pass

    try:
        element = Element.objects.get(id=elementId)
    except Element.DoesNotExist:
        coupon = None

    return redirect('store:detail',url_clean=element.url_clean, code=coupon)



class DetailView(generic.DeleteView): 
    model = Element
    template_name = 'store/detail.html'
    slug_field = 'url_clean'
    slug_url_kwarg = 'url_clean'


# def make_pay_paypal(request, pk):
    
#     element = get_object_or_404(Element,pk = pk)

#     # Creating Access Token for Sandbox
#     client_id = settings.PAYPAL_CLIENT_ID
#     client_secret = settings.PAYPAL_CLIENT_SECRET
#     # Creating an environment
#     environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
#     client = PayPalHttpClient(environment)

#     requestPaypal = OrdersCreateRequest()

#     requestPaypal.prefer('return=representation')

#     requestPaypal.request_body (
#         {
#             "intent": "CAPTURE",
#             "purchase_units": [
#                 {
#                     "amount": {
#                         "currency_code": "USD",
#                         "value": str(element.price)
#                     }
#                 }
#             ],
#             "application_context":{
#                 "return_url": "http://localhost:8000/product/paypal/success/%s"%element.id,
#                 "cancel_url": "http://localhost:8000/product/paypal/cancel"},
#             }
#         }
#     )   
     
#     try:
#         # Call API with your client and get a response for your call
#         response = client.execute(requestPaypal)

#         if response.result.status == "CREATED":
#             approval_url = str(response.result.links[1].href)
#             print(approval_url)
#             return render(request, 'store/paypal/buy.html', {'element': element,'approval_url': approval_url})

#         print ('Order With Complete Payload:')
#         print ('Status Code:', response.status_code)
#         print ('Status:', response.result.status)
#         print ('Order ID:', response.result.id)
#         print ('Intent:', response.result.intent)
#         print ('Links:')
#         # for link in response.result.links:
#         #     print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
#         #     print ('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
#         #     response.result.purchase_units[0].amount.value))
#         #     # If call returns body in response, you can get the deserialized version from the result attribute of the response
#         #     order = response.result
#         #     print (order)
#     except IOError as ioe:
#         print (ioe)
#         if isinstance(ioe, HttpError):
#             # Something went wrong server-side
#             print (ioe.status_code)    


# @login_required
# def paypal_success(request,pk):

#     paypalrestsdk.configure({
#     "mode": settings.PAYPAL_CLIENT_MODO, # sandbox or live
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_CLIENT_SECRET})
    
#     element = get_object_or_404(Element, pk = pk)

#     paymentId = request.GET.get('paymentId')
#     payerId = request.GET.get('PayerID')

#     payment = paypalrestsdk.Payment.find(paymentId)

#     try:
#         if payment.execute({"payer_id": payerId}):
        
#             paymentModel = Payment(payment_id=paymentId,
#             payer_id=payerId,
#             price=element.price,
#             element_id=element,
#             user_id=request.user
#             )
            
#             paymentModel.save()

#             print("Payment execute successfully")
#         else:
#             print(payment.error) # Error Hash
#     except paypalrestsdk.exceptions.ResourceNotFound as e:
#         print("Se produjo un error %s"%type(e).__name__ )

    
#     return render(request, 'store/paypal/success.html')


# ********** PRIMERA SDK PAYPAL*********************
@login_required
def make_pay_paypal(request, pk, code=None):

    coupon = get_valid_coupon(code) if code else None

    # Caso del cupon Invalido
    if coupon is None and code is not None:
        return HttpResponseNotFound()
            
    element = get_object_or_404(Element,pk = pk)

    if coupon:
        return_url = "http://localhost:8000/product/paypal/success/%s/%s"%(element.id, coupon.code)
        price = round(element.get_price_after_discount(coupon),2)
    else:
        return_url = "http://localhost:8000/product/paypal/success/%s"%element.id
        price = element.price


    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO, # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET})

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": "http://localhost:8000/product/paypal/cancel"},
        "transactions": [{
            #"item_list": {
                # "items": [{
                #     "name": "item",
                #     "sku": "item",
                #     "price": str(element.price),
                #     "currency": "USD",
                #     "quantity": 1}]},
            "amount": {
                "total": str(price),
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))

    return render(request, 'store/paypal/buy.html', {'element': element,'approval_url': approval_url})

# ********** PRIMERA SDK PAYPAL*********************
@login_required
def paypal_success(request,pk, code=None):

    coupon = get_valid_coupon(code) if code else None

    paypalrestsdk.configure({
    "mode": settings.PAYPAL_CLIENT_MODO, # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET})
    
    element = get_object_or_404(Element, pk = pk)

    paymentId = request.GET.get('paymentId')
    payerId = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(paymentId)

    try:
        if payment.execute({"payer_id": payerId}):
        
            paymentModel = Payment.create(payment_id=paymentId,
                payer_id=payerId,
                price=element.price,
                element_id=element.id,
                user_id=request.user.id
            )

            if coupon:
                paymentModel.coupon = coupon
                paymentModel.discount = element.get_price_after_discount(coupon)
                paymentModel.price_discount = element.get_discount(coupon)
                coupon.active = 0 # desactiva cupom
                coupon.save() # guarda datos de cupones

            paymentModel.save()
            print("Payment execute successfully")

            return redirect(reverse('store:detail_pay', args=[paymentModel.id]))
            
        else:
            print(payment.error) # Error Hash
    except paypalrestsdk.exceptions.ResourceNotFound as e:
        print("Se produjo un error %s"%type(e).__name__ )

    
    return render(request, 'store/paypal/success.html')

@login_required
def detail_pay(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'store/payment/detail.html',{'payment':payment})
    
@login_required
def bought(request):
    return render(request, 'store/payment/bought.html',{'payments':Payment.objects.select_related('element').filter(user = request.user)})


@login_required
def paypal_cancel(request):
    return render(request, 'store/paypal/cancel.html' )



### OTRAS FUNCIONES :

def get_valid_coupon(code):

    now = timezone.now()

    coupon = None
    try:
        couponModel = Coupon.objects.get(code__iexact=code,
            valid_from__lte=now, # less than or equel to
            valid_to__gte=now, # great than or equel to
            active = True
        )

        coupon = couponModel
    except Coupon.DoesNotExist:
        pass

    return coupon

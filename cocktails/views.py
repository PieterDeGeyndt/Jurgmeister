from django.shortcuts import render,get_object_or_404,redirect

from jurgmeister.settings import MOLLIE_CLIENT_ID, MOLLIE_CLIENT_SECRET, MOLLIE_PUBLIC_URL, MOLLIE_SECRET_KEY
from .models import Cocktails, Order, OrderItem, BillingAddress, Payment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from mollie.api.client import Client
from django.conf import settings
import requests


#COCKTAILS
def allcocktails(request):
    cocktails=Cocktails.objects
    return render(request,'cocktails/allcocktails.html',{'cocktails': cocktails})

def detail(request, cocktail_id):
    detailcocktail = get_object_or_404(Cocktails, pk=cocktail_id)
    return render(request,'cocktails/detail.html', {'cocktail': detailcocktail})


@login_required(login_url="/accounts/login")
def add_to_cart(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item's quantity was updated.")
            return redirect("allcocktails")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("allcocktails")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("allcocktails")

@login_required(login_url="/accounts/login")
def remove_from_cart(request,cocktail_id):
    item=get_object_or_404(Cocktails,pk=cocktail_id)
    order_qs= Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # if more than one item in cart remove just one 
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, "One cocktail of this type was removed.")
                return redirect("allcocktails")
            #if only 1, then delete the item from the cart.    
            else:
                order_item.delete()
                messages.info(request, "This cocktail was removed from your cart.")
                return redirect("allcocktails")

        else:
            #add a message saying the order does not contain the item
            messages.info(request, "This cocktail is not in your cart.")
            return redirect("allcocktails")
    else:
        #add a message saying the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("allcocktails")

#ORDER-SUMMARY
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'cocktails/order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("cocktails/allcocktails.html")

@login_required(login_url="/accounts/login")
def add_to_cart_summary(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item's quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")

@login_required(login_url="/accounts/login")
def remove_from_cart_summary(request,cocktail_id):
    item=get_object_or_404(Cocktails,pk=cocktail_id)
    order_qs= Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # if more than one item in cart remove just one 
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, "One cocktail of this type was removed.")
                return redirect("order-summary")
            #if only 1, then delete the item from the cart.    
            else:
                order_item.delete()
                messages.info(request, "This cocktail was removed from your cart.")
                return redirect("order-summary")

        else:
            #add a message saying the order does not contain the item
            messages.info(request, "This cocktail is not in your cart.")
            return redirect("order-summary")
    else:
        #add a message saying the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")

@login_required(login_url="/accounts/login")
def empty_cart(request,cocktail_id):
    item=get_object_or_404(Cocktails,pk=cocktail_id)
    order_qs= Order.objects.filter(
        user=request.user,
        ordered=False
    )
    order_item=OrderItem.objects.filter(
    item=item,
    user=request.user,
    ordered=False
    )[0]
    if order_qs.exists():
        order_item.delete()
        messages.info(request, "This cocktail was removed from your cart.")
        return redirect("order-summary")
    else:
        #add a message saying the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")

#CheckoutForm
class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args,**kwargs):
        #orders + form
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context={
                'object':order,
                'form':form
            }
            return render(self.request,'cocktails/checkout.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("cocktails/allcocktails.html")
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                delivery_method = form.cleaned_data.get('delivery_method')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                zip = form.cleaned_data.get('zip')
                #TODO: add functionality for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                billing_address = BillingAddress(
                    user=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    street_address=street_address,
                    appartment_address=appartment_address,
                    zip = zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                #TODO: add redirect to the selected payment option
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request,"Failed checkout")
            return redirect("order-summary")

class PaymentView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context={
                    'object':order
                    }
            return render (self.request,"cocktails/payment.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("cocktails/checkout.html")   

    def post(self, *args, **kwargs):
        order=Order.objects.get(user=self.request.user, ordered=False)
        value = order.get_total()
        # Define new payment
        mollie_client = Client()
        is_authorized, authorization_url = mollie_client.setup_oauth(
            client_id = MOLLIE_CLIENT_ID,
            client_secret= MOLLIE_CLIENT_SECRET,
            redirect_uri = MOLLIE_PUBLIC_URL,
            token = self.request.POST.get(MOLLIE_SECRET_KEY),
        )
        mollie_client.setup_oauth_authorization_response(authorization_response)
        mollie_client.organizations.get('me')
        charge = mollie_client.payments.create({
            'amount': {
                'currency': 'EUR',
                'value': value 
                },
            'description': "My 1st payment with Mollie",
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
            })

        #create the payment
        payment = Payment()
        payment.mollie_payment_id = charge['id']
        payment.user = self.request.user
        payment.amount = value
        payment.save()
        #assign the payment to the order
        order.ordered=True
        order.payment = payment
        order.save() 

        messages.succes(self.request, "Payment opgeslagen")
        return redirect('/')

def your_account(request):
    return redirect('/cocktails')
from asyncio.windows_events import NULL
from datetime import datetime
from distutils.command.clean import clean
from logging import NullHandler
from tkinter.messagebox import NO
from django.shortcuts import render, get_object_or_404, redirect
from jurgmeister.settings import MOLLIE_SECRET_KEY
from .models import Cocktails, Order, OrderItem, BillingAddress, Payment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpRequest
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from mollie.api.client import Client
from django.conf import settings
from django.core.mail import send_mail


# COCKTAILS
def allcocktails(request):
    cocktails = Cocktails.objects
    return render(request, 'cocktails/allcocktails.html', {'cocktails': cocktails})
    
def detail(request, cocktail_id):
    detailcocktail = get_object_or_404(Cocktails, pk=cocktail_id)
    return render(request, 'cocktails/detail.html', {'cocktail': detailcocktail})


@login_required(login_url="/accounts/login")
def add_to_cart(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    #get all unordered items for that users from OrderItem db
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False,
    )
    #get all unordered orders of that user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        #if it exists take top order
        order = order_qs[0]
        # check if the item is already in the order
        if order.items.filter(item__pk=item.pk).exists():
            #if it is than augment the quantity with 1
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "1 " + item.title + " is aan je wagentje toegevoegd. Je hebt nu " + str(order_item.quantity) + " " + item.title + "'s in je wagentje.")
            return redirect("allcocktails")
        #if the item is not yet in the order than add the item to the order
        else:
            order.items.add(order_item)
            messages.success(request, "1 " + item.title + " is aan je wagentje toegevoegd. Je hebt nu " + str(order_item.quantity) + " " + item.title + "'s in je wagentje.")
            return redirect("allcocktails")
    #if there's no unordered order for that user
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, start_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "1 " + item.title + " werd aan je wagentje toegevoegd.")
        return redirect("allcocktails")


@login_required(login_url="/accounts/login")
def remove_from_cart(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # if more than one item in cart remove just one
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.warning(request, "1 " + item.title + " werd verwijderd. Je hebt nu " + str(order_item.quantity) + " " + item.title + "'s in je wagentje.")
                return redirect("allcocktails")
            # if only 1, then delete the item from the cart.
            else:
                order_item.delete()
                messages.info(request, "De laatste " + item.title + " werd verwijderd uit je wagentje.")
                return redirect("allcocktails")

        else:
            # add a message saying the order does not contain the item
            messages.warning(request, "Er is geen "+ item.title +" in je wagentje.")
            return redirect("allcocktails")
    else:
        # add a message saying the user does not have an order
        messages.warning(request, "Je hebt geen actieve bestelling. Voeg aub eerst cocktails toe aan je wagentje.")
        return redirect("allcocktails")

# ORDER-SUMMARY
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request,'cocktails/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Je hebt nog geen actieve bestelling. Voeg hieronder eerst cocktails toe aan je wagentje aub.")
            return redirect("allcocktails")


@login_required(login_url="/accounts/login")
def add_to_cart_summary(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "1 " + item.title + " werd aan je wagentje toegevoegd.")
            return redirect("order-summary")
        else:
            messages.info(request, "1 " + item.title + " werd aan je wagentje toegevoegd.")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, start_date=ordered_date)
        order.items.delete(all)
        order.items.add(order_item)
        messages.info(request, "1 " + item.title + " werd aan je wagentje toegevoegd.")
        return redirect("order-summary")


@login_required(login_url="/accounts/login")
def remove_from_cart_summary(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # if more than one item in cart remove just one
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, "1 " + item.title + " werd uit je wagentje verwijderd.")
                return redirect("order-summary")
            # if only 1, then delete the item from the cart.
            else:
                order_item.delete()
                messages.info(
                    request, "De laatste " + item.title + " werd uit je wagentje verwijderd.")
                return redirect("order-summary")

        else:
            # add a message saying the order does not contain the item
            messages.info(request, "Geen " + item.title + " in je wagentje of je hebt nog geen actieve bestelling.")
            return redirect("order-summary")
    else:
        # add a message saying the user does not have an order
        messages.info(request, "Je hebt geen actieve bestelling. Voeg aub eerst cocktails toe aan je wagentje.")
        return redirect("order-summary")


@login_required(login_url="/accounts/login")
def empty_cart(request, cocktail_id):
    item = get_object_or_404(Cocktails, pk=cocktail_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    if order_qs.exists():
        order_item.delete()
        messages.info(request, "De laatste " + item.title + " werd uit je wagentje verwijderd.")
        return redirect("order-summary")
    else:
        # add a message saying the user does not have an order
        messages.info(request, "Je hebt geen actieve bestelling. Voeg aub eerst cocktails toe aan je wagentje.")
        return redirect("order-summary")

# CheckoutForm
class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        #orders + form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'object': order,
                'form': form
            }
            return render(self.request, 'cocktails/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Je hebt geen actieve bestelling. Voeg aub eerst cocktails toe aan je wagentje.")
            return redirect("order-summary")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                delivery_method = form.cleaned_data.get('delivery_method')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                billing_address = BillingAddress(
                    user=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    street_address=street_address,
                    phone=phone,
                    appartment_address=appartment_address,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.delivery_method = delivery_method
                if delivery_method == "D":
                    order.total = order.get_total_delivery()
                else:
                    order.total = order.get_total()
                order.save()
                # TODO: create completely new order
                return redirect("payment")
        except ObjectDoesNotExist:
            messages.warning(self.request, "Failed checkout")
            return redirect("order-summary")


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'order': order
            }
            return render(self.request, "cocktails/payment.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Je hebt geen actieve bestelling. Voeg aub eerst cocktails toe aan je wagentje.")
            return redirect("cocktails/checkout.html")

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            value = str(order.total) + '0'
            # Define new payment
            mollie_client = Client()
            mollie_client.set_api_key(MOLLIE_SECRET_KEY)
            charge = mollie_client.payments.create({
                'amount': {
                    'currency': 'EUR',
                    'value': value
                },
                'description': "My 1st payment with Mollie",
                'redirectUrl': 'https://www.jurgmeister.be/cocktails/confirmation',
                'webhookUrl': '',
            })
            # create the payment
            payment = Payment()
            payment.mollie_payment_id = charge.id
            payment.user = self.request.user
            payment.amount = order.total
            payment.timestamp = timezone.now()
            payment.save()
            # assign the payment to the order
            order_items=order.items.all()
            order_items.update(ordered = True)
            order_items.update(ordered_timestamp = payment.timestamp)
            for item in order_items:
                item.save()
            order.charge = payment
            order.ordered = True
            order.ordered_date = payment.timestamp
            order.save()
            messages.success(self.request, "Je order was succesvol!")
            return redirect(charge.checkout_url)

        except ObjectDoesNotExist:
            messages.error(self.request, "Je hebt geen actieve bestelling.")
            return redirect("order-summary")
        #excepts toevoegen voor mollie errors + back in browser

def your_account(request):
    return redirect('/cocktails')

class ConfirmationView(LoginRequiredMixin,View):    
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=True)
            context = {
                'order': order
            }
            return render(self.request, "cocktails/confirmation.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Er liep iets fout bij de bestelling. Stuur ons een mailtje op info@jurgmeister.be en we brengen het zo snel mogelijk in orde.")
            return redirect("cocktails/confirmation.html")

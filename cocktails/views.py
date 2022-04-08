from django.shortcuts import render, get_object_or_404, redirect
import cocktails

from jurgmeister.settings import MOLLIE_SECRET_KEY
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
            messages.success(request, "1 " + item.title + " was added to your cart. You now have " + str(order_item.quantity) + " " + item.title + "'s in your cart")
            return redirect("allcocktails")
        else:
            order.items.add(order_item)
            messages.success(request, "1 " + item.title + " was added to your cart. You now have " + str(order_item.quantity) + " " + item.title + "'s in your cart")
            return redirect("allcocktails")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "1 " + item.title + " was added to your cart.")
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
                messages.warning(request, "1 " + item.title + " was removed. You now have " + str(order_item.quantity) + " " + item.title + "'s in your cart")
                return redirect("allcocktails")
            # if only 1, then delete the item from the cart.
            else:
                order_item.delete()
                messages.info(request, "The last " + item.title + " was removed from your cart.")
                return redirect("allcocktails")

        else:
            # add a message saying the order does not contain the item
            messages.warning(request, "There is no "+ item.title +" in your cart.")
            return redirect("allcocktails")
    else:
        # add a message saying the user does not have an order
        messages.warning(request, "You do not have an active order. Please add cocktails to your cart firs.")
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
            messages.warning(self.request, "You do not have an active order yet, please add cocktails to your cart first.")
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
            messages.info(request, "1 " + item.title + " was added to your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "1 " + item.title + " was added to your cart.")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "1 " + item.title + " was added to your cart.")
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
                    request, "1 " + item.title + " was added to your cart.")
                return redirect("order-summary")
            # if only 1, then delete the item from the cart.
            else:
                order_item.delete()
                messages.info(
                    request, "The last " + item.title + " was removed from your cart.")
                return redirect("order-summary")

        else:
            # add a message saying the order does not contain the item
            messages.info(request, "A " + item.title + " is not in your cart or you don't have an active order yet, so it can't be removed.")
            return redirect("order-summary")
    else:
        # add a message saying the user does not have an order
        messages.info(request, "You do not have an active order. Please add cocktails to your cart first.")
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
        messages.info(request, "The last " + item.title + " was removed from your cart.")
        return redirect("order-summary")
    else:
        # add a message saying the user does not have an order
        messages.info(request, "You do not have an active order. Please add cocktails to your cart first.")
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
            messages.warning(self.request, "You do not have an active order. Please return to Cocktails and add cocktails to your cart first.")
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
                appartment_address = form.cleaned_data.get(
                    'appartment_address')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                # TODO: add functionality for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
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
            messages.warning(self.request, "You do not have an active order. Please return to the site and add cocktails to your cart first.")
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
                'redirectUrl': 'https://www.test2impress.be',
                'webhookUrl': '',
            })
            # create the payment
            payment = Payment()
            payment.mollie_payment_id = charge.id
            payment.user = self.request.user
            payment.amount = order.total
            payment.save()
            # assign the payment to the order
            order_items=order.items.all()
            order_items.update(ordered = True)
            for item in order_items:
                item.save()
            order.charge = payment
            order.ordered = True
            order.items.delete()
            order.save()
            messages.success(self.request, "Your order was succesful!")
            return redirect(charge.checkout_url)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order-summary")
        #excepts toevoegen voor mollie errors + back in browser

def your_account(request):
    return redirect('/cocktails')


def confirmation(request):
    return redirect("confirmation")

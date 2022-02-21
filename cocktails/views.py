from django.shortcuts import render,get_object_or_404,redirect
from .models import Cocktails, Order, OrderItem
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

def allcocktails(request):
    cocktails=Cocktails.objects
    return render(request,'cocktails/allcocktails.html',{'cocktails': cocktails})

def detail(request, cocktail_id):
    detailcocktail = get_object_or_404(Cocktails, pk=cocktail_id)
    return render(request,'cocktails/detail.html', {'cocktail': detailcocktail})

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

# FOR ORDER-SUMMARY
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

def checkout(request):
    return render(request,"cocktails/checkout.html")

def your_account(request):
    return redirect('/cocktails')

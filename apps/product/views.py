from django.shortcuts import render,get_object_or_404,redirect
from .models import Item
from django.views.generic import ListView, DetailView, View
from ..order.models import Order, OrderItem
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ipstack import GeoLookup
import requests
import json


def checkout(request):
    geo_lookup = GeoLookup("581858e87c3628991ff44ae8ff6ddd1e")
    location = geo_lookup.get_own_location()
    lat = location["latitude"]
    lng = location["longitude"]
    country = location["country_name"]
    region = location["region_name"]
    city = location["city"]
    print(location)
    return render(request, "checkout-page.html",{"country": country,"region": region, "city":city})

class ListItem(ListView):
    model = Item
    paginate_by = 9
    template_name = "home-page.html"
    context_object_name = "items"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            context = {
                "object": order
            }
            return render(self.request, "order-summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an active order")
            return redirect("/")
        











@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(items=item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    # print(order_item)
    # print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
        else:
            messages.info(request, "This item was added to your cart")
            order_item.quantity += 1
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        print(order.items)
        order.items.add(order_item)
        print(order)
        print(order.items)
        messages.info(request, "This item was added to ur cart")

    return redirect("product", slug=slug)

@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(items=item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was added to ur cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to ur cart")

    return redirect("product", slug=slug)

@login_required
def remove_from_card(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(items=item, user = request.user, ordered = False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from ur cart")
            return redirect("product", slug=slug)
        else:
            messages.info(request, "This item was not in ur cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You dont have an active order")
        return redirect("product", slug=slug)
    return redirect("product", slug=slug)
    

@login_required
def remove_from_card_in(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(items=item, user = request.user, ordered = False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from ur cart")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in ur cart")
            return redirect("order-summary")
    else:
        messages.info(request, "You dont have an active order")
        return redirect("order-summary")
    return redirect("order-summary")


@login_required
def remove_single_item_from_card(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(items=item, user = request.user, ordered = False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            
            messages.info(request, "This item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in ur cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You dont have an active order")
        return redirect("product", slug=slug)
    return redirect("product", slug=slug)

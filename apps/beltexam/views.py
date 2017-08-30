# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from models import * 
from django.contrib import messages
# the index function is called when root is visited
def index(request):
    return render(request, "beltexam/index.html")

def create(request ):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/success')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'items': User.objects.get(id=request.session['user_id']).wishlist_items.all(),
        'all_items': Item.objects.exclude(added=request.session['user_id'])
    }
    return render(request, 'beltexam/success.html', context)

def addproduct(request):
    if len(request.POST['item']) == 0:
        messages.error(request, "item entry should not be empty")
        return redirect("/addcreate")
    elif len(request.POST['item']) < 3:
        messages.error(request, "item should be more than 3 characters")
        return redirect("/addcreate")
    else:
        Item.objects.create(item=request.POST['item'],added=User.objects.get(id=request.session['user_id']))
        User.objects.get(id = request.session['user_id']).wishlist_items.add(Item.objects.get(item=request.POST['item']))
        return redirect('/success')

def addcreate(request):
    return render(request, 'beltexam/create.html')

def join_wish_items(request, id):
    Item.objects.get(id=id).wishlist_by.add(User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def wishlist(request, id):
    context = {
        'item': Item.objects.get(id=id),
        'users': Item.objects.get(id=id).wishlist_by.all()
    }
    return render(request,'beltexam/wishlist.html', context)



def delete(request, id):
    Item.objects.get(id=id).delete()
    return redirect("/success")

def remove(request, id):
    Item.objects.get(id=id).wishlist_by.remove(User.objects.get(id = request.session['user_id']))
    return redirect("/success")
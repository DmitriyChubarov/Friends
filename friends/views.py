#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Users, Prop, Friends
from django.db.models import Q

def login_view(request):
    if request.method=='POST':
        name = request.POST['name']
        password = request.POST['password']

        user = authenticate(request, username=name,password=password)

        if user:
            login(request, user)
            return redirect('profile')
    return render(request, 'friends/login.html')

def register_view(request):
    if request.method=='POST':
        name = request.POST['name']
        password = request.POST['password']

        user = Users.objects.create_user(username=name, password=password)

        return redirect('login')
    return render(request, 'friends/register.html')

@login_required
def profile_view(request):
    user = request.user 
    sent_props = Prop.objects.filter(out_id=request.user.id)
    received_props = Prop.objects.filter(in_id=request.user.id)
    friends_list = Friends.objects.filter(Q(first_id=request.user.id) | Q(second_id=request.user.id))

    friends = []
    for friend in friends_list:
        if (friend.first_id_id == request.user.id):
            friends.append(friend.second_id)
        else:
            friends.append(friend.first_id)
    
    context = {
            'user': user,
            'sent_props': sent_props,
            'received_props': received_props,
            'friends': friends,
            }

    return render(request, 'profile.html', context)

class main_view(TemplateView):
    template_name = 'main.html'

@login_required
def possible_view(request):
    users = Users.objects.exclude(id=request.user.id)
    friends = Friends.objects.filter(Q(first_id_id=request.user.id) | Q(second_id_id=request.user.id))
    props = Prop.objects.filter(Q(in_id_id=request.user.id) | Q(out_id_id=request.user.id))

    main_friends = []
    out_props = []
    in_props = []
    for user in users:
        for friend in friends:
            if (user.id == friend.first_id_id):
                main_friends.append(friend.first_id_id)
            elif (user.id == friend.second_id_id):
                main_friends.append(friend.second_id_id)
        for prop in props:
            if (user.id == prop.in_id_id):
                out_props.append(prop.in_id_id)
            if (user.id == prop.out_id_id):
                in_props.append(prop.out_id_id)

    context = {
            'users': users,
            'main_friends': main_friends,
            'out_props': out_props,
            'in_props': in_props,
            }

    return render(request, 'friends/possible.html', context)

def send_prop(request, user_id):
    if request.method == 'POST':
        in_user = Users.objects.get(id=user_id)
        Prop.objects.get_or_create(out_id=request.user, in_id=in_user, status=0)
    return redirect('possible')

def accept_req(request, user_id):
    if request.method == 'POST':
        second_user = Users.objects.get(id=user_id)
        Friends.objects.get_or_create(first_id=request.user, second_id=second_user)
        Prop.objects.filter(in_id=request.user, out_id=second_user).delete()
    return redirect('profile')

def reject_req(request, user_id):
    if request.method  == 'POST':
        out_user = Users.objects.get(id=user_id)
        Prop.objects.filter(in_id=request.user.id, out_id=out_user).delete()
    return redirect('profile')

def delete_friend(request, user_id):
    if request.method == 'POST':
        user = Users.objects.get(id=user_id)
        Friends.objects.filter(Q(Q(first_id_id=request.user.id) & Q(second_id_id=user.id)) | Q(Q(second_id_id=request.user.id) & Q(first_id_id=user.id))).delete()
        return redirect('profile')

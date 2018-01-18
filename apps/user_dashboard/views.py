# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import bcrypt

# Create your views here.
def index(request):
	if "user" in request.session:
		return redirect('/dashboard')
	return render(request, "user_dashboard/index.html")

def gosignin(request):
	return render(request, "user_dashboard/signin.html")

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/gosignin')
	else:
		user = User.objects.get(email=request.POST['email'])
		if user:
			if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
				messages.error(request, 'Account with those credentials could not be found.')
				return redirect('/gosignin')
			else:
				if user:
					request.session['user'] = user.id
					messages.success(request, 'Currently Logged in as ' + user.first_name + "!")
					return	redirect('/dashboard')
					# return redirect(reverse('success',kwargs ={'user_id':user.id}))

def logout(request):
	del request.session['user']
	return redirect('/')

def goregister(request):
	return render(request, "user_dashboard/register.html")

def addnewuser(request):
	return render(request, "user_dashboard/addnew.html")

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags= tag)
		return redirect('/goregister')
	else:
		user = User.objects.create()
		user.first_name = request.POST['first_name']
		user.last_name = request.POST['last_name']
		user.email =request.POST['email']
		user.userlevel = "normal"
		user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user.save()
		messages.success(request, 'User created. Please login!')
		return redirect('/gosignin')

def dashboard(request):
	theuser = User.objects.get(id=request.session['user'])
	context = {
		"users": User.objects.all()
	}
	if theuser.userlevel == "normal":
		return render(request, "user_dashboard/normaldashboard.html", context)
	if theuser.userlevel == "admin":
		return render(request,"user_dashboard/admindashboard.html", context)

def show(request, user_id):
	context = {
		'user' : User.objects.get(id=user_id),
		'themessages': Message.objects.filter(where_id = user_id),
		'comments': Comment.objects.all(),
		'prof_pics': Document.objects.filter(owner_id = user_id),
	}
	return	render(request, "user_dashboard/user.html", context)

def edit_user(request, user_id):
	context = {
		'user' : User.objects.get(id=user_id),
	}
	return render(request, 'user_dashboard/edit_user.html', context)

def save_edits(request, user_id):
	print(request.POST)
	user = User.objects.get(id=user_id)
	if request.POST['first_name'] != "":
		user.first_name = request.POST['first_name']
	if request.POST['last_name']!= "":
		user.last_name = request.POST['last_name']
	if request.POST['email']!= "":
		user.email = request.POST['email']
	if request.POST['password']!= "":
		if request.POST['password'] == request.POST['passconf']:
			user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
	user.save()
	messages.success(request, 'User edited successfully!')
	return redirect('/')

def post_message(request, user_id):
	user1 = User.objects.get(id=request.session['user'])
	message = Message.objects.create(message =request.POST['message'], user_id = user1.id, where_id=user_id)
	message.save()
	return redirect(reverse('show_user',kwargs ={'user_id':user_id}))

def comments(request, user_id):
	comment = Comment.objects.create(comment=request.POST['comment'], user= User.objects.get(id=request.session['user']), message = Message.objects.get(id=request.POST['message_id']))
	return redirect(reverse('users',kwargs ={'user_id':user_id}))

def removeuser(request, user_id):
	user = User.objects.get(id=user_id)
	user.delete()
	return redirect("/")

def upload_file(request, user_id):
	print("Request.file data is here:")
	print(request.FILES['pic_upload'])
	return redirect("/users/" + user_id)
	

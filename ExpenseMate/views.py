from django.shortcuts import render,redirect
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User


from .models import *
# Create your views here.

#Yeh login ka logic hai
def login_page(request):
  if request.method=="POST":
    data=request.POST
    username=data.get('username')
    password=data.get('password')
    print(username)

    if not User.objects.filter(username=username).exists():
      messages.info(request,"User does not exist")
      return redirect('/')
    
    user=authenticate(username=username ,password=password)

    if user is None:
      messages.error(request,"Password mismatch")
      return redirect('/')
    else:
      login(request,user)
      return redirect('dashboard/')
  last_message = messages.get_messages(request)
  last_message = list(last_message)[-1] if last_message else None
  
  return render(request,'login.html',{'last_message': last_message})


#Yaha sai register ka logic hai 
def register(request):
  if request.method=="POST":
    data=request.POST
    first_name=data.get('first_name')
    last_name=data.get('last_name')
    username=data.get('username')
    password=data.get('password')

    user=User.objects.filter(username=username) 
    if user.exists():
      messages.warning(request, "User Already Exists")
      return redirect('/register')
    
    user=User.objects.create(
      first_name=first_name,
      last_name=last_name,
      username=username
    )
    user.set_password(password)
    user.save()

    messages.info(request, "User registered successfully")

    return redirect('/register/')
  
  return render(request,'register.html')


#Yaha hai dashboard ka logic
def dashboard(request):
  users=request.user
  u_name=users.username
  
  user = User.objects.get(username=u_name)
  tot_amount=Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total']
  food=Expense.objects.filter(category='food').aggregate(total=Sum('amount'))['total']
  health=Expense.objects.filter(category='health').aggregate(total=Sum('amount'))['total']
  bills=Expense.objects.filter(category='bills').aggregate(total=Sum('amount'))['total']
  other=Expense.objects.filter(category='other').aggregate(total=Sum('amount'))['total']
  stationary=Expense.objects.filter(category='stationary').aggregate(total=Sum('amount'))['total']
  print(type(object))

  return render(request,'dashboard.html',context={'amount':tot_amount,'food':food,'health':health,'bills':bills,'other':other,'stationary':stationary,'title':'dashboard'})


def logout_user(request):
  messages.info(request,"Logged out successfully")
  logout(request)
  return redirect('/')



@login_required
def add_expense(request,id=None):
  if request.method=="POST":
    data=request.POST
    amount=data.get('amount')
    description=data.get('description')
    category=data.get('category')
    category=category.lower()

    Expense.objects.create(
      user=request.user,
      description=description,
      category=category,
      amount=amount
    )

    return redirect('/dashboard')
  if id:
    queryset=Expense.objects.get(id=id)
    amount=queryset.amount
    category=queryset.category
    description=queryset.description
    return render(request,'addexpense.html',context={'amount':amount,'category':category,'description':description})

  return render(request,'addexpense.html',)



def view_page(request):
  return render(request,'view.html')


def history_view(request):
  query=Expense.objects.all()
  return render(request,'history.html',{'expenses':query,'title':'history'})

def delete_rec(request,id):
  queryset=Expense.objects.get(id=id)
  queryset.delete()
  messages.info(request,"Record Deleted successfully")
  return redirect('/history')



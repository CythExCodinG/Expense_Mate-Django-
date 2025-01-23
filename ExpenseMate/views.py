from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from decimal import Decimal
import matplotlib.pyplot as plt


from .models import *

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
@login_required(login_url='/')
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

  
  # *recurring expense extract
  recurring = Recurringexpense.objects.aggregate(Sum('amount'))['amount__sum']

  if recurring is None: #Handles the case where there are no Recurringexpense objects
    recurring = 0
  
  budget = request.session.get('budget', None)
  if budget:
    amount=Decimal(budget)
  else:
    amount=0
  flag=0
  compare=0
  if tot_amount:
    if tot_amount>amount:
      compare=tot_amount-amount
      flag=1
    else:
      compare=amount-tot_amount
      flag=0
  return render(request,'dashboard.html',context={'amount':tot_amount,'food':food,'health':health,'bills':bills,'other':other,'stationary':stationary,'title':'dashboard','budget':amount,'flag':flag,'compare':compare,'recurring':recurring})

def logout_user(request):
  messages.info(request,"Logged out successfully")
  logout(request)
  return redirect('/')


@login_required(login_url='/')
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
    queryset.delete()

    messages.info(request,"Data Updated Successfully")
    return render(request,'addexpense.html',context={'amount':amount,'category':category,'description':description})

  return render(request,'addexpense.html',)

def add_recurring(request,id):
  if request.method=="POST":
    data=request.POST
    amount=data.get('amount')
    description=data.get('description')

    Recurringexpense.objects.create(
      user=request.user,
      description=description,
      amount=amount
    )
    return redirect('/dashboard')
  if id:
    queryset=Recurringexpense.objects.get(id=id)
    amount=queryset.amount
    description=queryset.description
    queryset.delete()
    return render(request,'addRecurringExpense.html',context={'amount':amount,'description':description})
  return render(request,'addRecurringExpense.html')

@login_required(login_url='/')
def history_view(request):
  query=Expense.objects.all()
  return render(request,'history.html',{'expenses':query,'title':'history'})

def delete_rec(request,id):
  queryset=Expense.objects.get(id=id)
  queryset.delete()
  messages.info(request,"Record Deleted successfully")
  return redirect('/history')

def delete_recurring(request,id):
  queryset=Recurringexpense.objects.get(id=id)
  queryset.delete()
  messages.info(request,"Record Deleted successfully")
  return redirect('/dashboard/editrecurring/')

def setbudget(request):
  if request.method=="POST":
    data=request.POST
    amount=data.get('amount')
    # date=data.get('date')

    request.session['budget'] = amount
    return redirect('/dashboard')
  # if id:
  #   queryset=Budget.objects.get(id=id)

  #   queryset.amount
  context = {
        'current_budget': request.session.get('budget', None),
    }
  return render(request,'addbudget.html',context)

def aboutpage(request):
  return render(request,'about.html',{'title':'about'})

def graph(request):


  food=Expense.objects.filter(category='food').aggregate(total=Sum('amount'))['total']
  health=Expense.objects.filter(category='health').aggregate(total=Sum('amount'))['total']
  bills=Expense.objects.filter(category='bills').aggregate(total=Sum('amount'))['total']
  other=Expense.objects.filter(category='other').aggregate(total=Sum('amount'))['total']
  stationary=Expense.objects.filter(category='stationary').aggregate(total=Sum('amount'))['total']
    
  categories = ['Food', 'Health', 'bills', 'stationary','other']
  expenses = [food, health, bills, stationary, other]
  print(len(expenses))
  if expenses[0] and expenses[1] and expenses[2] and expenses[3] and expenses[4]==None:
    messages.info(request,"First Add expenses")
    return redirect('/dashboard')
  else:
    plt.bar(categories, expenses, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Expenses (in ₹)')
    plt.title('Monthly Expense Distribution')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
  return redirect('/dashboard')


def editrecurring_expenses(request):
  recurring=Recurringexpense.objects.all()
  return render(request,'recurring_expense_history.html',context={'recurring':recurring})
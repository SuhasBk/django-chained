from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TodoForm
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,"todo/home.html")

def loginuser(request):
    if request.method == 'GET':
        return render(request, "todo/loginuser.html", {'form': AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if not user:
            return render(request, "todo/loginuser.html", {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

def signupuser(request):
    if request.method == 'GET':
        return render(request, "todo/signupuser.html", {'form': UserCreationForm()})
    else:
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(request.POST.get('username'),password=request.POST.get('password1'))
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'Username already exists. Please choose another'})
        else:
            return render(request, "todo/signupuser.html", {'form': UserCreationForm(),'error':'Passwords do not match'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user,date_completed__isnull=True)
    return render(request,"todo/currenttodos.html",{'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user,date_completed__isnull=False).order_by('-date_completed')
    return render(request,"todo/completedtodos.html",{'todos':todos})

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,"todo/viewtodo.html",{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, "todo/viewtodo.html", {'todo': todo, 'form': form, 'error':'Bad info!'})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, "todo/createtodo.html", {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, "todo/createtodo.html", {'form': TodoForm(),'error':"You cannot break my website, bitch ;)"})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

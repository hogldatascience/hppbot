from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def registerUser(request):

    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username_html')
        password = request.POST.get('password_html')

        if username and password:

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)

                return redirect('site')

                # print("Login.........")

                #return render(request, 'home.html', {})

            else:
                messages.error(request, 'Username or Password is Incorrect!')
                
        else:
            messages.error(request, 'Fill out all the fields!')

    #return render(request, 'accounts/login.html', {})

    return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    return redirect('index')

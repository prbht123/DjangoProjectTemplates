from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages 

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for user {username}')
            return redirect('account:login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    
class Logout(LogoutView):
    template_name = 'logout.html'
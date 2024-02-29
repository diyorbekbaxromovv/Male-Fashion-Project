from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import Hero, Banner, Product, Category, Team
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy 
from django.views.generic import UpdateView
# Create your views here.
def index(request):
    heros = Hero.objects.all()
    banners = Banner.objects.all()
    products = Product.objects.all()
    data = {
        'heros':heros,
        'banners':banners,
        'products':products
        
    }
    return render(request, 'main/index.html', context=data)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data["username"], password=cleaned_data["password"])

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, ('Вы успешно вошли в свой аккаунт!'))
                return HttpResponseRedirect(reverse('index'))
            
    form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))




def category(request,id):
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    products = category.products.all()
    data = {
        'products': products,
        'category': category,
        'categories': categories    
    }
    
    return render(request,'main/shop.html', context=data)
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    data = {
        'categories': categories,
        'products': products,
        
    }
    return render(request, 'main/shop.html', context=data)


def details(request, id):
    products = Product.objects.all()
    product = Product.objects.get(id=id)    
    data = {
        'product': product,
        'products': products
    }
    return  render(request, 'main/shop-details.html', context=data)


def register(request):
    
    
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()
    
    return render(request,'main/register.html', context={'form':form})

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'main/password_change_form.html'
    success_url = reverse_lazy('index')
    
    
class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'main/profile_form.html'
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def get_object(self):
        return self.request.user
    
    
def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams
    }
    return render(request,'main/about.html', context=data)

def checkout(request):
        
    return render(request, 'main/checkout.html')
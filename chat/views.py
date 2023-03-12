from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import Chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def top_func(request):
    if request.user.is_authenticated:
        return redirect('list')
    else:
        return render(request, 'chat/top.html')

def signup_func(request):
    if request.user.is_authenticated:
        return redirect('list')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if len(password) < 8:
                return render(request, 'chat/signup.html', {'context': 'パスワードは８文字以上で入力してください'})
            else:
                try:
                    user = User.objects.create_user(username, '', password)
                    user = authenticate(request, username=username, password=password)
                    login(request, user)
                    return redirect('list')
                except IntegrityError:
                    return render(request, 'chat/signup.html', {'context': 'このユーザー名はすでに登録されています'})
        else:
            return render(request, 'chat/signup.html')
    
def signin_func(request):
    if request.user.is_authenticated:
        return redirect('list')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list')
            else:
                return render(request, 'chat/signin.html', {'context': 'サインインできませんでした'})
        else:
            return render(request, 'chat/signin.html')

@login_required(login_url='/signin/')
def listview_func(request):
    object_list = Chat.objects.all().order_by('created_at').reverse()
    return render(request, 'chat/listview.html', {'object_list': object_list})

def signout_func(request):
    logout(request)
    return redirect('signin')

@login_required
def detail_func(request, pk):
    object = get_object_or_404(Chat, pk=pk)
    return render(request, 'chat/detail.html', {'object': object})

@login_required
def good_func(request, pk):
    object = get_object_or_404(Chat, pk=pk)
    object.good += 1
    object.save()
    return redirect('list')

class ChatCreate(LoginRequiredMixin, CreateView):
    template_name = 'chat/create.html'
    model = Chat
    fields = ('message', 'poster', 'picture')
    success_url = reverse_lazy('list')
    redirect_field_name = 'redirect_to'

class ChatDelete(LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = reverse_lazy('list')
    redirect_field_name = 'redirect_to'
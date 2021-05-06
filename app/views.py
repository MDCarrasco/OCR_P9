from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from app import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index_view(request):
    context = {}
    return render(request, 'index.html', context)

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    def form_valid(self, form):
        self.request.session['email'] = self.request.POST.get('email')
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)

class Login(LoginView):
    form_class = forms.UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'
    fields = '__all__'

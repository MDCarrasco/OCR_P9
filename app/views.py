from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views.generic import RedirectView
from django.shortcuts import render
from django.urls import reverse_lazy

from app import forms


# Create your views here.
@login_required(login_url='login')
def index_view(request):
    context = {}
    return render(request, 'index.html', context)


@login_required(login_url='feed')
def feed_view(request):
    context = {}
    return render(request, 'feed.html', context)


class NewReview(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review.html'

    # TODO: 2 forms via le membre form
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class NewReviewRequest(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewRequestForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_request.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class SignUp(CreateView):

    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        self.request.session['email'] = self.request.POST.get('email')
        form.save()
        return super().form_valid(form)


class Login(LoginView):

    form_class = forms.UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'
    fields = '__all__'


class Logout(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(Logout, self).get_redirect_url(*args, **kwargs)

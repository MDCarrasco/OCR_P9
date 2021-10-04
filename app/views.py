from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
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


class NewReviewWithoutTicket(TemplateView):

    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    new_review_request_form = forms.NewReviewRequestForm
    new_review_form = forms.NewReviewForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_without_ticket.html'

    def post(self, request):
        post_data = request.POST or None
        new_review_request_form = self.new_review_request_form(
            post_data, prefix="newreviewrequest"
        )
        new_review_form = self.new_review_form(
            post_data, prefix="newreview"
        )

        context = self.get_context_data(
            new_review_request_form=new_review_request_form,
            new_review_form=new_review_form
        )

        if new_review_request_form.is_valid() and new_review_form.is_valid():
            review_request = self.form_save(new_review_request_form)
            print("id is:", review_request.id)
            self.form_save(new_review_form)

        return self.render_to_response(context)

    def form_save(self, form, ticket):
        form.instance.user = self.request.user
        obj = form.save()
        return obj

    def get(self, request, *args, **kwargs):
        return self.post(request)


class NewReviewWithTicket(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    form_class = forms.NewReviewForm
    success_url = reverse_lazy('feed')
    template_name = 'new_review_with_ticket.html'

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
